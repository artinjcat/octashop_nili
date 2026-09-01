from django.urls import path
from apps.cart.views.site import CartView

urlpatterns = [
    path('', CartView.cart_summary, name="cart_summary"),
    path('add/', CartView.cart_add, name="cart_add"),
    path('delete/', CartView.cart_delete, name="cart_delete"),
    path('update/', CartView.cart_update, name="cart_update"),
    
    # checkout and complete buy...
    # path('checkout/', CartCheckOutView.checkout_template_view, name="checkout"),
]
