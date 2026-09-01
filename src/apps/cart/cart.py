from apps.catalogs.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class Cart():
    def __init__(self,request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists:
        cart = self.session.get('session_key')
        
        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available on all pages of site
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
    
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        quantities = self.cart
        total = 0
        for key,value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.stockrecords.all().first().in_offer:
                        total = total + (product.stockrecords.all().first().offer_price * value)
                    else:
                        total = total + (product.stockrecords.all().first().sale_price * value)
                    
        return total
            
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product, quantity):
        product_id = str(product)
        product_qty= int(quantity)
        
        current_cart = self.cart
        
        current_cart[product_id] = product_qty
        
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
        updated_cart = self.cart
        
        return updated_cart
    
    
    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified =  True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))