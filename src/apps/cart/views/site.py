from django.shortcuts import render, get_object_or_404
from apps.cart.cart import Cart

from django.http import JsonResponse
from django.shortcuts import redirect

from apps.cart.forms import CheckOutOrderForm
from apps.catalogs.models import Category, Product



def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")

class CartView():
    def cart_summary(request):
        context = {}
        context["sub_categories"] = sub_category_list()
        cart = Cart(request)
        
        if cart.__len__() == 0:
            return render(request, "carts/cart_empty.html",context)
        else:
            cart_products = cart.get_prods
            context["cart_products"] = cart_products
            quantities = cart.get_quants
            context["quantities"] = quantities
            totals = cart.cart_total()
            context["totals"] = totals
            return render(request, "carts/cart_summary.html",context)
        
        
    def cart_add(request):
        cart = Cart(request)
        if request.POST.get("action")== "post":
            product_id = request.POST.get("product_id")
            product_qty = request.POST.get("qty-to-cart")
            product = get_object_or_404(Product,id=product_id)
            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()
            
            
            # response = JsonResponse({ 'product name :': '{}  {}'.format(product.company_name, product.model)} )
            response = JsonResponse({ 'qty': cart_quantity} )
            
            return response
        
        
        
        
        
    def cart_delete(request):
        cart = Cart(request)
        if request.POST.get("action")== "remove-cart":
            product_id = request.POST.get("product_id")
            
            cart.delete(product=product_id)
            response = JsonResponse({'product':product_id})
            return response
        else:
            pass
    
    
    def cart_update(request):
        cart = Cart(request)
        if request.POST.get("action")== "update-cart":
            product_id = request.POST.get("product_id")
            product_qty = request.POST.get("qty_update")
            
            cart.update(product=product_id, quantity=product_qty)
            response = JsonResponse({'qty':product_qty})
            return response
        
        
class CartCheckOutView():
    def checkout_template_view(request):
        if request.user.is_authenticated:
            context = {}
            context["sub_categories"] = sub_category_list()
            cart = Cart(request)
            if cart.__len__() == 0:
                return render(request, "carts/cart_empty.html",context)
            else:
                cart_products = cart.get_prods
                context["cart_products"] = cart_products
                quantities = cart.get_quants
                context["quantities"] = quantities
                totals = cart.cart_total()
                context["totals"] = totals
            if request.method == "POST":
                form = CheckOutOrderForm(request.POST)
                if form.is_valid:
                    try:
                        order = form.save(commit=False)
                        order.customer = request.user.customer
                        order.save()
                        cart_p = cart_products()
                        cart_q = quantities()
                        
                        for product in cart_p:
                            quantity = cart_q[str(product.id)]
                            op = OrderedProduct.objects.create(
                            order = order,
                            product = product,
                            quantity = quantity,
                            )
                            
                            op.save()
                            cart.delete(product.id)
                        # return redirect("orders-view")
                        return redirect("order-view", pk = order.id)
                    except Exception as error:
                        print(error)
                        return redirect("profile")
                else:
                    return redirect("checkout")
            else:
                return render(request, 'carts/checkout.html', context)
        else:
            return redirect("login")
        
