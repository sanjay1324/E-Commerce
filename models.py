from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, Username, EmailId, password=None, **extra_fields):
        if not EmailId:
            raise ValueError('The EmailId field must be set')
        email = self.normalize_email(EmailId)
        user = self.model(Username=Username, EmailId=email, **extra_fields)
        user.set_password(password)  # Correctly use set_password method
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, EmailId, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(Username, EmailId, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Other'),
    ]

    UserId = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=150, unique=True)
    EmailId = models.EmailField(unique=True)
    MobileNo = models.CharField(max_length=15)
    Age = models.PositiveIntegerField()
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    CreatedDate = models.DateTimeField(default=timezone.now)
    ModifiedDate = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Use the custom manager

    USERNAME_FIELD = 'Username'  # The unique identifier for login
    REQUIRED_FIELDS = ['EmailId']  # Fields required when creating a superuser

    def __str__(self):
        return self.Username
class Product(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=255, unique=True)
    ProductDescription = models.CharField(max_length=255)
    ProductUnitPrice = models.FloatField()
    ProductStatus = models.CharField(max_length=20)
    InitialLoadStock = models.IntegerField()
    StockLeft = models.IntegerField()
    ProductCategory = models.CharField(max_length=50)
    CreatedDate = models.DateTimeField(default=timezone.now)
    ModifiedDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ProductName

class OrderPurchased(models.Model):
    PurchaseOrderId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    TotalPrice = models.IntegerField()
    PurchasedDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.PurchaseOrderId} by {self.UserId.Username} for {self.ProductId.ProductName}'

class UserLog(models.Model):
    LogId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='UserId')
    Action = models.CharField(max_length=50)
    Timestamp = models.DateTimeField(default=timezone.now)
    AccessToken = models.CharField(max_length=255)
    RefreshToken = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.LogId} - {self.UserId.Username} - {self.Action}"  # Use `UserId.Username` correctly

class Image(models.Model):
    Title = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='images/')
    UploadedAt = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    
    

