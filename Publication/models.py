
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Vous devez entrer un email.")
        
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True


class Linkedin_Account(models.Model):
    account = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    linkedin_account = models.CharField(max_length=200, blank=True, default="")
    linkedin_password = models.CharField(max_length=100, blank=True, default="")
    campaign = models.BooleanField(default=False)
    active_follow_up_3 = models.BooleanField(default="False")
    active_follow_up_2 = models.BooleanField(default="False")
    active_follow_up_1 = models.BooleanField(default="False")
    message1 = models.TextField(default="", max_length=200)
    follow_up_1 = models.TextField(default="")
    follow_up_2 = models.TextField(default="")
    follow_up_3 = models.TextField(default="")
    proxy_use = models.BooleanField(default=False)
    proxy_host = models.TextField(default="")
    proxy_port = models.TextField(default="")
    proxy_user = models.TextField(default="")
    proxy_pass = models.TextField(default="")
    


class Linkedin_Profile_Info(models.Model):
    associated_account = models.ForeignKey(Linkedin_Account, on_delete=models.SET_NULL, null=True)
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    sales_navigator_link = models.URLField(max_length=300)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    linkedin_link = models.URLField()
    message_sent = models.BooleanField(default=False)
    follow_up_1 = models.BooleanField(default=False)
    follow_up_2 = models.BooleanField(default=False)
    follow_up_3 = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    last_message = models.DateField(blank=True, null=True)
    error = models.BooleanField(default=False)

