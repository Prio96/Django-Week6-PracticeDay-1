from django.urls import path
from .views import DepositMoneyView, WithdrawMoneyView, TransactionReportView, LoanRequestView, LoanListView, RepayLoanView, MoneyTransferView

urlpatterns = [
    path("deposit/",DepositMoneyView.as_view(), name="Deposit"),
    path("report/",TransactionReportView.as_view(), name="Transaction Report"),
    path("withdraw/",WithdrawMoneyView.as_view(), name="Withdraw"),
    path("loan_request/",LoanRequestView.as_view(), name="Loan Request"),
    path("loans/",LoanListView.as_view(), name="Loan List"),
    path("loan/<int:loan_id>/",RepayLoanView.as_view(), name="Loan Repayment"),
    path("money_transfer/",MoneyTransferView.as_view(), name="Transfer Money")
]