from datetime import datetime
from django.shortcuts import render,redirect
from django.http import JsonResponse

from apps.catalogs.infrastructure.models import Category

from .models import *




def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")


class Payment():
    def orders_page(request):
        if request.user.is_authenticated:
            context={}
            context["sub_categories"] = sub_category_list()
            if Order.objects.filter(customer = request.user.customer).exists:
                context["orders"] = Order.objects.filter(customer = request.user.customer).order_by("-id")
                return render(request, "accounts/profile-order.html", context)
            else:
                return render(request, "carts/cart_empty.html",context)
        else:
            return redirect("login")
    
    
    
    
    
    def order_view(request,pk):
        context = {}
        context["sub_categories"] = sub_category_list()
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(id=pk)
                if order.customer == request.user.customer:
                    context["order"] = order
                    total_price = 0
                    for prod in order.ordered_product.all():
                        if prod.product.is_offer:
                            total_price = (prod.product.offer_price * prod.quantity) + total_price
                        else:
                            total_price = (prod.product.price * prod.quantity) + total_price
                            
                    context["total_price"] = total_price
                    return render(request, "payments/order-page.html", context)
                else:
                    return redirect("login")
            except Exception as error:
                print(error)
                return redirect("index")
        else:
            return redirect("login")
        
    def upload_receipt_url(request):
        if request.user.is_authenticated:
            if request.method == "POST" and request.POST.get("action") == "post":
                
                order_id = request.POST.get("order")
                if Order.objects.filter(id=order_id, customer=request.user.customer).exists:
                    order=Order.objects.get(id=order_id)
                    order.receipt = request.FILES.get("img")
                    order.payment_status = True
                    order.order_date_done = datetime.datetime.now()
                    total_price = 0
                    for prod in order.ordered_product.all():
                        if prod.product.is_offer:
                            total_price = (prod.product.offer_price * prod.quantity) + total_price
                        else:
                            total_price = (prod.product.price * prod.quantity) + total_price
                    order.total_price = total_price
                    
                    order.save()
                else:
                    context = {"status":"failed","details":"Order Not Found"}
                    response = JsonResponse(context)
                    return response
                context = {"status":"success"}
                response = JsonResponse(context)
                return response
            else:
                print("get")
        else:
            pass
        
        



# def payment(request):
#     if request.user.is_authenticated:
#         context={}
#         context["sub_categories"] = sub_category_list()
        
#         return render(request, "accounts/payment.html", context)
#     else:
#         return redirect("login")