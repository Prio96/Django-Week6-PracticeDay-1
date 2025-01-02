from django import forms
from .models import TransactionModel
from django.contrib.auth.models import User
class TransactionForm(forms.ModelForm):
    class Meta:
        model=TransactionModel
        fields=['amount','transaction_type']
        
    def __init__(self,*args,**kwargs):
        self.account=kwargs.pop('account')#get can also be used in this regard
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True #Field will stay disabled
        self.fields['transaction_type'].widget=forms.HiddenInput() #Will be hidden from user
        
    def save(self,commit=True):
        self.instance.account=self.account
        self.instance.balance_after_trxn=self.account.balance
        return super().save()
    
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount=100
        amount=self.cleaned_data.get('amount')
        
        if amount<min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}$ '
            )
        return amount
    

class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        min_withdraw_amount=500
        max_withdraw_amount=20000
        balance=account.balance
        amount=self.cleaned_data.get('amount')
        
        if amount<min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount}$ '
            )
        
        if amount>max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount}$ '
            )
            
        if amount>balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
            
        return amount

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data.get('amount')
        return amount
    
class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model=TransactionModel
        fields=['account','amount','transaction_type']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True #Field will stay disabled
        self.fields['transaction_type'].widget=forms.HiddenInput() #Will be hidden from user
        
    def save(self,commit=True):
        #account,amount,balance_after_trxn,transaction_type
        recipient_account=self.cleaned_data.get('account')
        # recipient_obj=User.objects.get(pk=recipient_account)
        amount=self.cleaned_data.get('amount')
        transaction_type=self.cleaned_data.get('transaction_type')
        balance_after_trxn_sender=self.request.user.balance
        balance_after_trxn_recipient=recipient_account.balance
        TransactionModel.objects.create(
            account=self.request.user,
            amount=amount,
            balance_after_trxn=balance_after_trxn_sender,
            transaction_type=transaction_type
        )
        TransactionModel.objects.create(
            account=recipient_account,
            amount=amount,
            balance_after_trxn=balance_after_trxn_recipient,
            transaction_type=transaction_type
        )    





        
        