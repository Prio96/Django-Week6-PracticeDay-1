from django import forms
from .models import TransactionModel
from django.contrib.auth.models import User
from accounts.models import UserBankAccount
from core.models import MamarBank
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
    def __init__(self,*args, **kwargs):
        self.bank=MamarBank.objects.get(name='Mamar Bank')
        super().__init__(*args,**kwargs)
    def clean_amount(self):
        account=self.account
        bank=self.bank
        min_withdraw_amount=500
        max_withdraw_amount=20000
        balance=account.balance
        amount=self.cleaned_data.get('amount')
        if not bank.is_bankrupt:
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
        else:
            raise forms.ValidationError(
                "The bank is bankrupt. You can not withdraw any money currently"
            )
        return amount

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data.get('amount')
        return amount
    
class MoneyTransferForm(forms.ModelForm):
    account_number=forms.CharField(max_length=20,required=True,label="Recipient Account ID")
    class Meta:
        model=TransactionModel
        fields=['amount','transaction_type']

    def __init__(self,*args,**kwargs):
        self.request=kwargs.pop('request',None)
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True #Field will stay disabled
        self.fields['transaction_type'].widget=forms.HiddenInput() #Will be hidden from user
        
    def clean_account_number(self):
        account_number=self.cleaned_data.get('account_number')
        try:
            account=UserBankAccount.objects.get(account_no=account_number)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError("The account number does not exist")
        return account
    def clean_amount(self):
        amount=self.cleaned_data.get('amount')
        if self.request.user.account.balance<amount:
            raise forms.ValidationError("Insufficient balance")
        return amount
    def save(self,commit=True):
        #account,amount,balance_after_trxn,transaction_type
        sender_account=self.request.user.account
        recipient_account=self.cleaned_data.get('account_number')
        # recipient_obj=User.objects.get(pk=recipient_account)
        amount=self.cleaned_data.get('amount')
        transaction_type=self.cleaned_data.get('transaction_type')
        sender_account.balance-=amount
        recipient_account.balance+=amount
        sender_account.save(
            update_fields=['balance']
        )
        recipient_account.save(
            update_fields=['balance']
        )
        sender_transaction=TransactionModel.objects.create(
            account=sender_account,
            amount=amount,
            balance_after_trxn=sender_account.balance,
            transaction_type=transaction_type
        )
        TransactionModel.objects.create(
            account=recipient_account,
            amount=amount,
            balance_after_trxn=recipient_account.balance,
            transaction_type=transaction_type
        )
        return sender_transaction





        
        