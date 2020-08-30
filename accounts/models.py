from django.db import models
from users.models import CustomUser
from django.utils import timezone

# Create your models here.
class AccountType(models.Model):
    account_type_name = models.CharField(max_length = 150)
    def __str__(self):
        return self.account_type_name

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    account_name = models.CharField(max_length = 150)
    account_balance = models.DecimalField(max_digits=30, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=15, decimal_places=5)
    compound_periods_per_year = models.IntegerField(help_text = "Use -1 to represent continuous interest")
    account_details = models.TextField()
    account_type = models.ForeignKey(AccountType, on_delete = models.RESTRICT)
    def __str__(self):
        return "Account {}: [{} {} ${:.2f}]".format(self.account_name, self.user, self.account_type, self.account_balance)

    
class AccountEntry(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    change_to_balance = models.DecimalField(max_digits=30, decimal_places=2)
    date = models.DateTimeField( default = timezone.now )
    description = models.TextField(default = "")
    def __str__(self):
        return "Account: {} ${:.2f} {}".format(self.account, self.change_to_balance, self.date.strftime("%m/%d/%Y, %H:%M:%S") )

