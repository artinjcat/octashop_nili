from django.urls import path
from .views import *

urlpatterns = [
    path('',Payment.orders_page, name="orders-view"),
    path("order-view/<int:pk>", Payment.order_view, name="order-view"),
    path('upload-receipt/',Payment.upload_receipt_url, name='upload-receipt'),
    
]
