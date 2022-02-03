from django.db import models
from django.forms import TextInput, EmailInput

class HelpCenter(models.Model):
	username=models.CharField(max_length=100,blank=False)
	qry=(('Regarding Tips and Suggestions','Regarding Tips and Suggestions'),('Regarding Transaction Alerts','Regarding Transaction Alerts'),('Regarding Profile Updation','Regarding Profile Updation'),('Other than above','Other than above'))
	query=models.CharField(max_length=100,blank=False,choices=qry)
	problem=models.TextField(blank=False)

class Transaction(models.Model):
    username=models.CharField(max_length=100,blank=False)
    tran_date = models.DateField("Transaction Date")
    tran_category = models.CharField("Transaction Category", max_length = 50)
    credit_amount = models.DecimalField("Credit Amount",max_digits=10, decimal_places = 5, default = 0)
    debit_amount = models.DecimalField("Debit Amount",max_digits=10, decimal_places = 5, default = 0)
    description = models.CharField("Transaction Description", max_length = 100)
    class Meta:
        db_table = "transactions"

    @property
    def is_credit_amount(self):
        return self.credit_amount>=0
        
