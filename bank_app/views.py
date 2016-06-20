from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login/"


class AccountView(ListView):
    model = User
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['user_pk']= self.request.user.pk
        return context
