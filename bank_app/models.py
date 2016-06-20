from django.db import models
from django.contrib.auth.models import User


class AccountTransaction(models.Model):
    TYPE_CHOICES = (('add', 'credit'), ('subtract', 'debit'))
    account_no = models.ForeignKey(User)  # using user.pk as the account ID
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2)
    trans_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='debit')
    trans_time = models.DateTimeField(auto_now_add=True)
    trans_note = models.TextField(max_length=60)

    def __str__(self):
        return self.trans_note
