
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
    
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    old_cart = models.CharField(_("Shopping cart"), max_length=200, null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' , blank=True, null=True,)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_profiles')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    old_cart = models.CharField(_("Shopping cart"), max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.username if self.user else "Profile without user"
    
    
    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         old_value = TelegramProfile.objects.get(pk=self.pk).referred_by
    #         if old_value != self.referred_by:
    #             raise ValidationError("You cannot change the referred_by field after creation.")
    #     super().save(*args, **kwargs)
    
    
class ProfileAssetType(models.Model):
    type = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64)


    def __str__(self):
        return "{} ({})".format(self.name, self.type)
    
    
    
class ProfileAsset(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assets')
    type = models.ForeignKey(ProfileAssetType, on_delete=models.CASCADE, related_name='assets')
    amount = models.DecimalField(default = 0 ,max_digits=20, decimal_places=8)
    
    
    
    class Meta:
        unique_together = ('user_profile', 'type')
        


    def __str__(self):
        return self.user_profile.username + " - " + self.type.type + " - " + str(self.amount)


class AssetHistoryType(models.Model):
    name = models.CharField(max_length=32 , unique=True)

    def __str__(self):
        return self.name


class ProfileAssetHistory(models.Model):
    profile_asset = models.ForeignKey(ProfileAsset, on_delete=models.CASCADE, related_name='history')
    change_type = models.ForeignKey(AssetHistoryType, on_delete=models.CASCADE, related_name='history')
    change_amount = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
    class Meta:
        verbose_name = 'Profile Asset History'
        verbose_name_plural = 'Profile Asset Histories'

    def __str__(self):
        return f"{self.profile_asset.user_profile.username} - {self.change_type.name} - {self.change_amount} - {self.timestamp}"