from decimal import Decimal

from store.models import Item


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, new_item: Item):
        # Проверка на выбор одного товара несколько раз
        if new_item.name in self.cart:
            self.cart[new_item.name]['quantity'] += 1
        else:
            self.cart[new_item.name] = {
                'id': new_item.id,
                'currency': new_item.currency.lower(),
                'name': new_item.name.title(),
                'description': new_item.description,
                'price': int(new_item.price * 100),
                'quantity': 1,
            }

        self.session.modified = True

    def clear_cart(self):
        self.cart.clear()

        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
