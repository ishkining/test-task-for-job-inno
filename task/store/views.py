from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import stripe

from .models import Discount, Item, Order
from .cart import Cart
from django.conf import settings

from django.urls import reverse


def show_all_items(request):
    cart = Cart(request)
    context = {
        'items': Item.objects.all(),
        'cart': cart,
    }
    print([item for item in cart])
    return render(request, 'store/show-all-items.html', context)


def show_one_item(request, id: int):
    stripe_codes = create_coupons()
    print(stripe_codes)
    context = {
        'item': Item.objects.get(id=id),
        'codes': stripe_codes,
    }
    return render(request, 'store/show-one-item.html', context)


def buy_one_item(request, id: int, code: str):
    cart = Cart(request)
    new_item = Item.objects.get(id=id)

    # Если товар другой валюты, то переход на главную
    if cart and new_item.currency.lower() \
            not in [item_cart['currency'] for item_cart in cart]:
        return HttpResponseRedirect(reverse('show-all-items'))

    # Проверка на выбор одного товара несколько раз
    cart.add(new_item)

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': current_item['currency'],
                'product_data': {
                    'name': current_item['name'],
                    'description': current_item['description'],
                },
                'unit_amount': current_item['price'],
                "tax_behavior": "inclusive",
            },
            'quantity': current_item['quantity'],
        } for current_item in cart],
        mode='payment',
        automatic_tax={
            'enabled': True,
        },
        discounts=[{'coupon': code}] if code != 'None' else [],
        success_url=request.build_absolute_uri(reverse('success-transaction', kwargs={'code': code})),
        cancel_url=request.build_absolute_uri(reverse('failed-transaction')),
    )

    context = {
        'item': Item.objects.get(id=id),
        'session_id': session['id'],
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'cart': cart,
    }
    return render(request, 'store/buy-one-item.html', context)


def clear_cart(request):
    cart = Cart(request)
    cart.clear_cart()
    return HttpResponseRedirect(reverse('show-all-items'))


def create_coupons():
    discount_codes = Discount.objects.all()
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    stripe_codes = stripe.Coupon.list()['data']
    result = []
    for code in discount_codes:
        if code.coupon_code not in [dis_code['id'] for dis_code in stripe_codes]:
            stripe.Coupon.create(duration="forever", id=code.coupon_code,
                                 percent_off=(code.discount_percent * 100))
        result.append((code.coupon_code, (code.discount_percent * 100)))

    return result


def success_transaction(request, code):
    our_cart = Cart(request)
    products = set()
    for product in our_cart:
        print(product)
        products.add(Item.objects.get(id=product['id']))
    try:
        discount_code = Discount.objects.get(coupon_code=code)
        new_order = Order.objects.create(discount_id=discount_code.id)
    except Exception:
        new_order = Order.objects.create()

    new_order.items.add(*products)
    new_order.save()
    our_cart.clear_cart()
    return render(request, 'store/success-transaction.html')


def failed_transaction(request):
    return render(request, 'store/failed-transaction.html')
