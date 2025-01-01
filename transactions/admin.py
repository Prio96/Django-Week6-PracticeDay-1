from django.contrib import admin
from .models import TransactionModel
from .models import LOAN
# Register your models here.
@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['account','amount','balance_after_trxn','transaction_type','loan_approval']
    
    def save_model(self, request, obj, form, change):
        if obj.loan_approval==True and obj.transaction_type==LOAN:
            obj.account.balance+=obj.amount
            obj.balance_after_trxn=obj.account.balance
            
            obj.account.save()
        return super().save_model(request, obj, form, change)
