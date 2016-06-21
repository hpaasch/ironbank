from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, RedirectView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

from bank_app.models import AccountTransaction


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
        context = super(AccountView, self).get_context_data(**kwargs)
        balance = 0
        trans_list = AccountTransaction.objects.filter(customer__username=self.request.user)
        for trans in trans_list:
            if trans.trans_type == 'Credit':
                balance += trans.trans_amount
            elif trans.trans_type == 'Debit':
                balance -= trans.trans_amount
        context['balance']= balance
        return context


class TransDetailView(ListView):
    template_name = 'detail_view.html'

    def get_queryset(self):
        return AccountTransaction.objects.filter(id=self.kwargs['pk'])

#  Dealing with the form is the time to block an overdraw, so will deal with that Tuesday.
