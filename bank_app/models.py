from django.db import models
from django.contrib.auth.models import User


class AccountTransaction(models.Model):
    customer = models.ForeignKey(User)
