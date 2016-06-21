from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, RedirectView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

from bank_app.models import AccountTransaction

def balance(self):
    trans_list = AccountTransaction.objects.filter(customer__username=self.request.user)
    self.balance = 0
    for trans in trans_list:
        if trans.trans_type == 'Credit':
            self.balance += trans.trans_amount
        elif trans.trans_type == 'Debit':
            self.balance -= trans.trans_amount
    return self.balance


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login/"


class AccountView(ListView):
    model = AccountTransaction
    template_name = 'account.html'

    def get_queryset(self):
        return AccountTransaction.objects.filter(customer__username=self.request.user).filter(trans_time__lte=datetime.datetime.today(),
        trans_time__gt=datetime.datetime.today()-datetime.timedelta(days=30))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = balance(self)
        return context


        # context = super().get_context_data(**kwargs)
        # balance = 0
        # trans_list = AccountTransaction.objects.filter(customer__username=self.request.user)
        # for trans in trans_list:
        #     if trans.trans_type == 'Credit':
        #         balance += trans.trans_amount
        #     elif trans.trans_type == 'Debit':
        #         balance -= trans.trans_amount
        # context['balance']= balance
        # return context


class TransDetailView(DetailView):
    model = AccountTransaction

    def get_queryset(self):
        return AccountTransaction.objects.filter(id=self.kwargs['pk']).filter(customer=self.request.user)  # what is this id syntax?


class CreateTransView(CreateView):
    model = AccountTransaction
    fields = ['trans_amount', 'trans_type', 'trans_note']
    success_url = reverse_lazy('account_view')  # better than /accounts/profile

    def form_valid(self, form):
        trans = form.save(commit=False)  # this half saves it
        trans.customer = self.request.user  # this attaches the user in the DB
        # if trans.trans_type == 'Debit' and 'balance' <= 0:
        return super().form_valid(form)  # this fully creates the transaction
