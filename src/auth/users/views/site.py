from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login , logout
from django.contrib.auth.models import User
from apps.cart.cart import Cart
from auth.users.forms import SignUpForm,ChangePasswordForm

from django.contrib import messages
from apps.catalogs.models import Category
import json
# from carts.cart import Cart


User = get_user_model()


def sub_category_list():
    return Category.objects.all().order_by("sorted_by")

def login_user(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        if User.objects.filter(phone_number = phone_number).exists():
            requested_user = get_object_or_404(User,phone_number = phone_number)
            
            password = request.POST["password"]
            user = authenticate(request, username=requested_user.username, password=password)
            print("user:",user)
            if user is not None:
                login(request, user)
                
                
                current_user = User.objects.get(id=request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    
                    for key,value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
                return redirect("home-site:home")
            else:
                messages.success(request, "دوباره تلاش کنید 1")
                return redirect("login")
        else:
            messages.success(request, "دوباره تلاش کنید 2")
            return render(request,"accounts/login.html",{})
    else:
        messages.success(request, "دوباره تلاش کنید 3")
        return render(request,"accounts/login.html",{})

def logout_user(request):
    logout(request)
    return redirect("home-site:home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print("form errors:",form.errors)
        if form.is_valid():
            print("form is valid")
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = User.objects.get(username = username)
            # customer = User.objects.create(user = user, phone_number = request.POST.get("phone_number"))
            user_auth = authenticate(username = username, password = password)
            login(request, user_auth)
            return redirect("home-site:home")
        else:
            messages.error(request, form.errors)
            return render(request, "accounts/register.html", {})
    else:
        return render(request, "accounts/register.html", {})
    
def profile_user(request):
    if request.user.is_authenticated:
        context = {}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/profile.html", context)
    else:
        return redirect("login")
    
def edit_profile_user(request):
    if request.user.is_authenticated:
        context = {}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/edit-profile.html", context)
    
    
    
def update_password(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                login(request, current_user)
                return redirect("profile")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect("update-password")
        else:
            context["form"] = ChangePasswordForm(current_user)
            return render(request, "accounts/update-password.html", context)
    else:
        return redirect("login")
    
    
    
def favorites(request):
    if request.user.is_authenticated:
        context={}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/favorites.html", context)
        
    else:
        return redirect("login")
    
    
def rules_page(request):
    context={}
    context["sub_categories"] = sub_category_list()
    return render(request, "accounts/rules.html", context)


