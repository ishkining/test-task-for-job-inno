from django.db import models

USD = 'USD'
EUR = 'EUR'
CURRENCY_CHOICES = [
    (USD, 'Dollars'),
    (EUR, 'Euros'),
]


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)

    class Meta:
        verbose_name_plural = 'Предметы'

    def get_price(self):
        sign_currency = ''
        if self.currency == USD:
            sign_currency = '$'
        elif self.currency == EUR:
            sign_currency = '€'

        return f'{sign_currency}{self.price}'

    def __str__(self):
        sign_currency = ''
        if self.currency == USD:
            sign_currency = '$'
        elif self.currency == EUR:
            sign_currency = '€'

        return f'{self.name}  - {self.get_price()}'


# class Tax(models.Model):
#     tax_percent = models.FloatField(default=0.1)
#
#     class Meta:
#         verbose_name_plural = 'Налоги'
#
#     def __str__(self):
#         return f'Налог {self.tax_percent * 100}%'


class Discount(models.Model):
    coupon_code = models.CharField(max_length=30, unique=True, blank=True, null=True)
    discount_percent = models.FloatField(default=0.05)

    class Meta:
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'Скидка {self.discount_percent * 100}%'


class Order(models.Model):
    items = models.ManyToManyField(Item)
    # tax = models.ForeignKey(Tax, on_delete=models.PROTECT, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Покупки'

    def get_items(self):
        return ", ".join([i.name.title() for i in self.items.all()])

    def __str__(self):
        return f'Покупка №{self.id}'
