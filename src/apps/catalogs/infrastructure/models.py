from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from apps.catalogs.managers import CategoryManager

from libs.db.fields import UpperCaseCharField


from libs.db.models import AuditableModel

class Category(MP_Node):
    title = models.CharField(_("title"), max_length=255, db_index=True)
    description = models.CharField(
        _("description"), max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(_("is public"), default=True)
    slug = models.SlugField(_("slug"), max_length=255,
                            unique=True, db_index=True, allow_unicode=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.title


class OptionGroup(models.Model):
    title = models.CharField(_("title"), max_length=255, db_index=True)

    class Meta:
        verbose_name = 'option group'
        verbose_name_plural = 'option groups'

    def __str__(self):
        return self.title


class OptionGroupValue(models.Model):
    title = models.CharField(_("title"), max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE,
                              related_name='values', verbose_name=_("group"))

    class Meta:
        verbose_name = 'option group value'
        verbose_name_plural = 'option group values'

    def __str__(self):
        return self.title


class ProductClass(models.Model):
    title = models.CharField(_("title"), max_length=255, db_index=True)
    description = models.CharField(
        _("description"), max_length=2048, null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=255,
                            unique=True, db_index=True, allow_unicode=True)

    track_stock = models.BooleanField(_("track stock"), default=True)
    require_shipping = models.BooleanField(_("require shipping"), default=True)

    options = models.ManyToManyField(
        'Option', related_name='product_classes', verbose_name=_("options"), blank=True)

    class Meta:
        verbose_name = 'product class'
        verbose_name_plural = 'product classes'

    def __str__(self):
        return self.title

    @property
    def has_attributes(self):
        return self.products_attributes.exists()


class ProductAttribute(models.Model):

    class AttributeTypeChoice(models.TextChoices):
        TEXT = 'text', _("Text")
        BOOLEAN = 'boolean', _("Boolean")
        INTEGER = 'integer', _("Integer")
        FLOAT = 'float', _("Float")
        DATE = 'date', _("Date")
        DATETIME = 'datetime', _("DateTime")
        OPTION_GROUP = 'option_group', _("Option Group")
        OPTION = 'option', _("Option")
        MULTI_OPTION = 'multi_option', _("Multi Option")

    title = models.CharField(_("title"), max_length=255, db_index=True)
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE,
                                      related_name='products_attributes', verbose_name=_("product class"), null=True)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT,
                                     related_name='attributes', verbose_name=_("option group"), null=True, blank=True)
    type = models.CharField(_("type"), max_length=20,
                            choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.TEXT)
    required = models.BooleanField(_("required"), default=False)

    class Meta:
        verbose_name = 'product attribute'
        verbose_name_plural = 'product attributes'

    def __str__(self):
        return self.title


class Option(models.Model):

    class OptionTypeChoice(models.TextChoices):
        TEXT = 'text', _("Text")
        BOOLEAN = 'boolean', _("Boolean")
        INTEGER = 'integer', _("Integer")
        FLOAT = 'float', _("Float")
        DATE = 'date', _("Date")
        DATETIME = 'datetime', _("DateTime")
        OPTION_GROUP = 'option_group', _("Option Group")
        OPTION = 'option', _("Option")
        MULTI_OPTION = 'multi_option', _("Multi Option")

    title = models.CharField(_("title"), max_length=255, db_index=True)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT,
                                     related_name='option_attributes', verbose_name=_("option group"), null=True, blank=True)
    type = models.CharField(_("type"), max_length=20,
                            choices=OptionTypeChoice.choices, default=OptionTypeChoice.TEXT)
    required = models.BooleanField(_("required"), default=False)

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    def __str__(self):
        return self.title


class Product(AuditableModel):
    
    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone', _("Standalone")
        parent = 'parent', _("Parent")
        child = 'child', _("Child")

    structure = models.CharField(_("structure"), max_length=20,
                                 choices=ProductTypeChoice.choices, default=ProductTypeChoice.standalone)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='children', verbose_name=_("parent"), null=True, blank=True)
    is_public = models.BooleanField(_("is public"), default=True)
    title = models.CharField(_("title"), max_length=255, db_index=True)
    upc = UpperCaseCharField(_("upc"), max_length=12,
                             null=True, blank=True, unique=True, help_text="uniq company num")
    description = models.CharField(
        _("description"), max_length=2048, null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=255,
                            unique=True, db_index=True, allow_unicode=True)
    meta_title = models.CharField(
        _("meta title"), max_length=255, null=True, blank=True)
    meta_description = models.TextField(
        _("meta description"), null=True, blank=True)
    meta_keywords = models.CharField(
        _("meta keywords"), max_length=1024, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products', verbose_name=_("category"))

    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT,
                                      related_name='products', verbose_name=_("product class"), blank=True, null=True)
    brand = models.ForeignKey('catalogs.ProductBrand', on_delete=models.PROTECT,
                              related_name='products', verbose_name=_("brand"), blank=True, null=True)
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue',
                                        related_name='products', verbose_name=_("attributes"), blank=True)
    recommended_products = models.ManyToManyField(
        'catalogs.Product', related_name='recommended_by', verbose_name=_("recommended products"), blank=True, through='ProductRecommendation')
    categories = models.ManyToManyField(
        Category, related_name='products_categories', verbose_name=_("categories"), blank=True)
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    @property
    def main_image(self):
        if self.images.exists():
            return self.images.order_by('display_order').first()
        else:
            return None


class ProductAttributeValue(models.Model):
    
    class UnitChoice(models.TextChoices):
        GRAM = 'گرم', _("گرم")
        KILOGRAM = 'کیلوگرم', _("کیلوگرم")
        LITER = 'لیتر', _("لیتر")
        MILLILITER = 'میلی‌لیتر', _("میلی‌لیتر")
        PIECE = 'عدد', _("عدد")
        METER = 'متر', _("متر")
        CENTIMETER = 'سانتی‌متر', _("سانتی‌متر")
        MILLIMETER = 'میلی‌متر', _("میلی‌متر")
    product = models.ForeignKey(
        Product, related_name='attribute_value', on_delete=models.CASCADE)

    attribute = models.ForeignKey(
        ProductAttribute, related_name='attribute_value', on_delete=models.CASCADE)
    
    unit = models.CharField(_("unit"), max_length=20, choices=UnitChoice.choices, blank=True, null=True)

    value_text = models.TextField(_("value text"), blank=True, null=True)
    value_integer = models.IntegerField(
        _("value integer"), blank=True, null=True)
    value_float = models.FloatField(_("value float"), blank=True, null=True)
    value_boolean = models.BooleanField(
        _("value boolean"), blank=True, null=True)
    # value_option_group = models.ForeignKey(
    #     OptionGroup, related_name='attribute_value', on_delete=models.PROTECT, blank=True, null=True)
    value_option = models.ForeignKey(
        OptionGroupValue, related_name='attribute_value', on_delete=models.PROTECT, blank=True, null=True)
    value_multi_option = models.ManyToManyField(
        OptionGroupValue, related_name='attribute_value_multi', blank=True)

    class Meta:
        verbose_name = 'attribute value'
        verbose_name_plural = 'attribute values'
        unique_together = ('product', 'attribute')
        
    def __str__(self):
        return f"{self.product.title} - {self.attribute.title}"
    
    def get_value_display(self):
        match self.attribute.type:
            case ProductAttribute.AttributeTypeChoice.TEXT:
                
                return f"{self.value_text} {self.unit if hasattr(self.attribute, 'unit') else ''}"
            case ProductAttribute.AttributeTypeChoice.BOOLEAN:
                return self.value_boolean
            case ProductAttribute.AttributeTypeChoice.INTEGER:
                return f"{self.value_integer} {self.attribute.unit if hasattr(self.attribute, 'unit') else ''}"
            
            case ProductAttribute.AttributeTypeChoice.FLOAT:
                return f"{self.value_float} {self.unit }"
            case ProductAttribute.AttributeTypeChoice.DATE:
                return self.value_text
            case ProductAttribute.AttributeTypeChoice.DATETIME:
                return self.value_text
            # case ProductAttribute.AttributeTypeChoice.OPTION_GROUP:
            #     return self.value_option_group
            case ProductAttribute.AttributeTypeChoice.MULTI_OPTION:
                return self.value_multi_option
            case ProductAttribute.AttributeTypeChoice.OPTION:
                return self.value_option


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(
        Product, related_name='primary_recommendations', on_delete=models.CASCADE)
    recommendation = models.ForeignKey(
        Product, related_name='recommendations', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(_("rank"), default=0)

    class Meta:
        verbose_name = 'product recommendation'
        verbose_name_plural = 'product recommendations'
        unique_together = ('primary', 'recommendation')
        ordering = ['primary', '-rank']





class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('media.Image', on_delete=models.PROTECT)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('display_order',)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()
            
            

class CategoryImages(models.Model):
    category = models.ForeignKey(Category, verbose_name=_("محصول"), on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("تصویر"),
                              height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = 'تصویر دسته بندی'
        verbose_name_plural = 'تصاویر دسته بندی ها'

    def __str__(self):
        return self.category.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))

    image_tag.short_description = 'Image'



class LastOffer(models.Model):
    product = models.ForeignKey("catalogs.Product", verbose_name=_("آخرین پیشنهاد"), on_delete=models.CASCADE, related_name="last_offer")
    offer_price = models.PositiveIntegerField(_("قیمت با تخفیف"), null=False, blank=False)
    offer_time = models.DateTimeField(_("زمان باقیمانده"), auto_now=False, auto_now_add=False)
    
    
    class Meta:
        verbose_name = 'آخرین پیشنهاد'
        verbose_name_plural = 'آخرین پیشنهاد ها'
        
    def __str__(self):
        return self.product.title
    
    
    
class ProductBrand(models.Model):
    title = models.CharField(_("title"), max_length=255, db_index=True, null=True, blank=True)
    description = models.CharField(
        _("description"), max_length=2048, null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=255,
                            unique=True, db_index=True, allow_unicode=True)

    class Meta:
        verbose_name = 'product brand'
        verbose_name_plural = 'product brands'

    def __str__(self):
        return self.title