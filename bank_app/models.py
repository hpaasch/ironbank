from django.db import models
from django.contrib.auth.models import User

CREDIT = 'Credit'
DEBIT = 'Debit'

class AccountTransaction(models.Model):
    TYPE_CHOICES = ((CREDIT, 'Credit'), (DEBIT, 'Debit'))
    customer = models.ForeignKey(User)  # using user.pk as the account ID
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2)
    trans_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default=DEBIT)
    trans_time = models.DateTimeField(auto_now_add=True)
    trans_note = models.CharField(max_length=30)

    def __str__(self):
        return self.trans_note

    class Meta:
        ordering = ['-trans_time']
