import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model



User = get_user_model()


def sub_directory_path_receipt(instance, filename):
    return 'images/receipt/{0}/{1}/{2}'.format(instance.customer.id,instance.id, filename)

class Order(models.Model):
    customer = models.ForeignKey(
        User, verbose_name=_("مشتری"), on_delete=models.CASCADE, null=False)
    national_code = models.CharField(_("کد ملی"), max_length=10)
    first_name = models.CharField(_("نام گیرنده"), max_length=20)
    last_name = models.CharField(_("نام خانوادگی گیرنده"), max_length=20)
    address = models.CharField(
        _("آدرس"), max_length=256, default="", blank=True)
    postal_code = models.CharField(
        _("کد پستی"), max_length=20, default="", blank=True)
    phone_number = models.CharField(_("تلفن"), max_length=24, default="", blank=True)
    description = models.CharField(_("توضیحات"), max_length=256, null=True,blank=True)
    order_date = models.DateField(
        _("تاریخ ثبت سفارش"), default=datetime.datetime.today, auto_now=False, auto_now_add=False)
    order_date_done = models.DateField(
        _("تاریخ تکمیل سفارش"), auto_now=False, auto_now_add=False,null=True, blank=True)
    status = models.BooleanField(_("تایید سفارش"), default=False)
    payment_status = models.BooleanField(_("گزارش پرداخت"), default=False)
    total_price = models.PositiveIntegerField(_("قیمت نهایی"), null=True)
    receipt = models.ImageField(_("تصویر رسید"), upload_to=sub_directory_path_receipt, height_field=None, width_field=None, max_length=None , null=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        # read_only_fields  = ['customer',]

    # def __str__(self):
    #     return str(self.customer.id)
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="240" height="360" />' % (self.receipt.url))

    image_tag.short_description = 'Image'
    
    def order_id(self):
        return str(self.id)
    
    order_id.short_description = 'کد سفارش'


class OrderedProduct(models.Model):
    order = models.ForeignKey("payments.Order",on_delete=models.CASCADE, related_name="ordered_product")
    product = models.ForeignKey("catalogs.Product",on_delete=models.CASCADE, related_name="ordered_product")
    quantity = models.PositiveSmallIntegerField(_("تعداد"), default=1)
    product_price = models.PositiveIntegerField(_("قیمت محصول"),null=True,blank=True)
    product_off_price = models.PositiveIntegerField(_("قیمت با تخفیف"),null=True,blank=True)
    description = models.CharField(_("توضیحات"), max_length=256)
    status = models.BooleanField(_("گزارش"), default=False)
    
    
    # def __str__(self):
    #     return str(self.product)