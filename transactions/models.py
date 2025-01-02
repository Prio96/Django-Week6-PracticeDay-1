from django.db import models
from accounts.models import UserBankAccount
# Create your models here.
DEPOSIT=1
WITHDRAWAL=2
LOAN=3
LOAN_PAID=4
MONEY_TRANSFER=5
TRXN_TYPE=(
    (DEPOSIT, 'Deposit'),
    (WITHDRAWAL, 'Withdrawal'),
    (LOAN, 'Loan'),
    (LOAN_PAID, 'Loan Repayment'),
    (MONEY_TRANSFER,'Money Transfer')
)

class TransactionModel(models.Model):
    account=models.ForeignKey(UserBankAccount, related_name='transactions', on_delete=models.CASCADE)#One user multiple trxns
    amount=models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_trxn=models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type=models.IntegerField(choices=TRXN_TYPE, null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    loan_approval=models.BooleanField(default=False)
    is_bankrupt=models.BooleanField(default=False)
    
    class Meta:
        ordering=['timestamp']
        
