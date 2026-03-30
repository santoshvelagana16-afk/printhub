from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_list, name='services'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('printing/', views.printing_service, name='printing_service'),
    path('binding/', views.binding_service, name='binding_service'),
    path('custom/', views.custom_printing_service, name='custom_service'),
    path('ajax/get-price/', views.get_price, name='get_price'),
    path('ajax/get-custom-price/', views.get_custom_price, name='get_custom_price'),
]
