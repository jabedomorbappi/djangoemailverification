from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address'), max_length=50, unique=True)
    email_is_verified = models.BooleanField(default=False)
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=30)
    mobile_number = models.CharField(_('Mobile Number'), null=True,max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)





from django.db import models

class CustomData(models.Model):
    text_box_1 = models.CharField(max_length=100)
    text_box_2 = models.CharField(max_length=100)
    dropdown_1 = models.CharField(max_length=50)
    dropdown_2 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.text_box_1}, {self.text_box_2}, {self.dropdown_1}, {self.dropdown_2}"




from django.db import models

class ProductFeedback(models.Model):
    product_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)
    feedback = models.TextField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.product_name} by {self.customer_name} - {self.rating} Stars"

