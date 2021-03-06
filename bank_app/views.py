from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, RedirectView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

from bank_app.models import AccountTransaction

def balance(user):
    trans_list = AccountTransaction.objects.filter(customer__username=user)
    balance = 0
    for trans in trans_list:
        if trans.trans_type == 'Credit':
            balance += trans.trans_amount
        elif trans.trans_type == 'Debit':
            balance -= trans.trans_amount
    return balance


class IndexView(TemplateView):
    template_name = 'index.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # maybe hard-coded URL pattern would be OK, given it's a Django thing


class AccountView(ListView):
    model = AccountTransaction
    template_name = 'account.html'

    def get_queryset(self):
        thirty_days = datetime.datetime.now() + datetime.timedelta(days=-30)
        return AccountTransaction.objects.filter(customer__username=self.request.user).filter(trans_time__gt=thirty_days)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = balance(self.request.user)
        return context


class TransactionDetailView(DetailView):
    model = AccountTransaction

    def get_queryset(self):
        return AccountTransaction.objects.filter(id=self.kwargs['pk']).filter(customer=self.request.user)  # what is this id syntax?


class TransactionCreateView(CreateView):
    model = AccountTransaction
    fields = ['trans_amount', 'trans_type', 'trans_note']
    success_url = reverse_lazy('account_view')  # better than /accounts/profile

    def form_valid(self, form):
        trans = form.save(commit=False)  #  half saves it
        trans.customer = self.request.user  #  attaches the user in the DB
        if trans.trans_type == 'Debit':
            if balance(self.request.user) < trans.trans_amount:
                form.add_error('trans_amount', 'Transaction failed: You do not have enough in your account to cover this amount')  # field affected, msg to give
                return self.form_invalid(form)
        return super().form_valid(form)  #  fully saves and creates the transaction


class TransferCreateView(CreateView):
    model = AccountTransaction
    fields = ['trans_amount', 'trans_note']
    success_url = reverse_lazy('account_view')

    def form_valid(self, form):
        trans = form.save(commit=False)  # this half saves it
        trans.customer = self.request.user  # this attaches the user in the DB
        recipient = User.objects.get(id=trans.trans_note)
        if balance(self.request.user) < trans.trans_amount:
            form.add_error('trans_amount', 'Transaction failed: You do not have enough in your account to cover this amount')  # field affected, msg to give
            return self.form_invalid(form)
        AccountTransaction.objects.create(customer=recipient, trans_amount=trans.trans_amount, trans_type='Credit', trans_note='')
        return super().form_valid(form)  #  fully saves and creates the transaction
