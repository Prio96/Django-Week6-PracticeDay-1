from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django.views import View
from .models import TransactionModel,DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID,MONEY_TRANSFER
from .forms import DepositForm,WithdrawForm,LoanRequestForm,MoneyTransferForm
from django.http import HttpResponse
from datetime import *
from django.db.models import Sum
from django.urls import reverse_lazy
#Ei view ke inherit kore deposit, withdraw, loan request er kaaj
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name='transactions/transaction_form.html'
    model=TransactionModel
    title=''
    success_url=reverse_lazy('Transaction Report')
    
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account, #goes to  __init__ of TransactionForm
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context.update({
            'title' : self.title
        })
        return context
class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Deposit'
    
    def get_initial(self):
        initial={'transaction_type' : DEPOSIT}
        return initial

    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance+=amount
        
        account.save(
            update_fields=['balance']
        )
        
        messages.success(self.request, f"{amount}$ was deposited to your account successfully")
        return super().form_valid(form)
    
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class=WithdrawForm
    title='Withdraw'
    def get_initial(self):
        initial={'transaction_type' : WITHDRAWAL}
        return initial
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request, f"{amount}$ was withdrawn from your account successfully")
        return super().form_valid(form)
    
class LoanRequestView(TransactionCreateMixin):
    form_class=LoanRequestForm
    title='Request For Loan'
    
    def get_initial(self):
        initial={'transaction_type': LOAN}
        return initial
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=TransactionModel.objects.filter(account=self.request.user.account,transaction_type=LOAN, loan_approval=True).count()#Number of loans of user approved by bank
        if current_loan_count>=3:
            return HttpResponse("You have crossed limit")
        messages.success(self.request,f"Loan request for amount {amount}$ has been made to admin")
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin,ListView):
    template_name="transactions/transaction_report.html"
    model=TransactionModel
    balance=0
    context_object_name="report_list"
    
    def get_queryset(self):
        queryset=super().get_queryset().filter(
            account=self.request.user.account
        )
        
        start_date_str=self.request.GET.get('start_date')
        end_date_str=self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date=datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date=datetime.strptime(end_date_str,"%Y-%m-%d").date()
            queryset=queryset.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date)#for filtering through account
            
            self.balance=TransactionModel.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        
        else:
            self.balance=self.request.user.account.balance
            
        return queryset.distinct()#distinct deyao jabe nao deya jabe
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account
        })
        return context
    
class RepayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan=get_object_or_404(TransactionModel, id=loan_id)
        
        if loan.loan_approval:
            user_account=loan.account
            if loan.amount < user_account.balance:
                user_account.balance-=loan.amount
                loan.balance_after_trxn=user_account.balance
                user_account.save()
                loan.transaction_type=LOAN_PAID
                loan.save()
                return redirect("Loan List")
            
            else:
                messages.error(self.request, f"Loan repayment amount is greater than available balance")
                return redirect("Loan List")

class LoanListView(LoginRequiredMixin, ListView):
    model=TransactionModel
    template_name="transactions/loan_request.html"
    context_object_name='loans'
    
    def get_queryset(self):
        user_account=self.request.user.account
        queryset=TransactionModel.objects.filter(account=user_account,transaction_type=LOAN)
        return queryset

class MoneyTransferView(LoginRequiredMixin, CreateView):
    model=TransactionModel
    template_name="transactions/transaction_form.html"
    form_class=MoneyTransferForm
    title='Transfer Money'
    success_url=reverse_lazy('Transaction Report')

    def get_initial(self):
        initial={'transaction_type':MONEY_TRANSFER}
        return initial
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context.update({
            'title' : self.title
        })
        return context
    
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['request']=self.request
        return kwargs
    
    def form_valid(self, form):
        try:
            # self.object=form.save()
            messages.success(self.request,f"${form.cleaned_data.get('amount')} has been transferred successfully to {form.cleaned_data.get('account_number')}.")
            return super().form_valid(form)
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        
                
            
    
        
        