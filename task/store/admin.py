from django.contrib import admin

from .models import Item, Discount, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'currency']
    list_editable = ['price', 'currency']
    ordering = ['price']
    list_per_page = 5


# class TaxAdmin(admin.ModelAdmin):
#     list_display = ['tax_percent']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'discount_percent']
    list_editable = ['discount_percent']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_items', 'discount')
    filter_horizontal = ['items']


admin.site.register(Item, ItemAdmin)
# admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Order, OrderAdmin)
