from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from .manager import CustomUserManager
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    photo_user = models.ImageField(default='images/user.png', null=True, upload_to='images/')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(default='Rei Receitas', max_length=100)
    number_of_attempts = models.DecimalField(max_digits=1, decimal_places=0, default=5)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return str(self.email)

    
    def return_the_mount_of_revenue(self):
        self.total_recipes = len(self.revenue_set.all())
        return self.total_recipes