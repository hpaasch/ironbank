from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        return AccountTransaction.objects.filter(user=self.request.user).filter(trans_time__lte=datetime.datetime.today(), trans_time__gt=datetime.datetime.today()-datetime.timedelta(days=30))

    def get_context_data(self):
        context = super().get_context_data()
        balance = 0
        trans_list = AccountTransaction.objects.filter(user=self.request.user)



        context['balance']= balance
        return context
