from django.contrib import admin
from .models import *


class OrderedProductInlineAdmin(admin.StackedInline):
    model = OrderedProduct
    fields = ('product', 'quantity',
            #   'product_price','product_off_price','description',
              )
    extra = 0
    readonly_fields = ['product', 'quantity',
                        # 'product_price','product_off_price','description',
                        ]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','customer','order_date','order_date_done','payment_status','status','total_price')
    readonly_fields = ['order_id','customer','order_date','order_date_done','payment_status','total_price','national_code',
                       'first_name','last_name','address','postal_code','phone_number','description','receipt','image_tag',]
    
    inlines = (OrderedProductInlineAdmin,)
