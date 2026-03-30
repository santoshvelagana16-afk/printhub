from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.payment_view, name='payment'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.order_list, name='order_list'),
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('tracking/<str:order_number>/', views.order_tracking, name='order_tracking'),
]
