from django.db import models
from django.contrib.auth.models import User
# Create your models here.
Account_type=(
    ('Savings','Savings'),
    ('Current','Current'),
)
Gender_type=(
    ('Male','Male'),
    ('Female','Female'),
)
class UserBankAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    account_type=models.CharField(max_length=10,choices=Account_type)
    account_no=models.IntegerField(unique=True)
    birth_date=models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=10,choices=Gender_type)
    initial_deposit_date=models.DateField(auto_now_add=True)#Account opening date
    balance=models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)#Integer and other number forms not allowed

class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.user.email)