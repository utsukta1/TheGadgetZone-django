from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('verify_payments/',views.verify_payments,name='verify_payments'),
    path('order_complete/',views.order_complete, name='order_complete'),
]
