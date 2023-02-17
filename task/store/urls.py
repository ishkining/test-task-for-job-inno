from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_items, name='show-all-items'),
    path('item/<int:id>', views.show_one_item, name='show-one-item'),
    path('buy/<int:id>/<str:code>', views.buy_one_item, name='buy-one-item'),
    path('clear', views.clear_cart, name='clear-cart'),
    path('success-transaction/<str:code>', views.success_transaction, name='success-transaction'),
    path('failed-transaction', views.failed_transaction, name='failed-transaction'),
]