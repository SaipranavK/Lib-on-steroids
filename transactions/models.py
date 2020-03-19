from django.db import models
from accounts.models import User
from catalog.models import Book

class Transaction(models.Model):
	user=models.ForeignKey(User,on_delete=models.PROTECT)
	book=models.ForeignKey(Book,on_delete=models.PROTECT)
	issue_date=models.DateField(auto_now_add=True)
	return_date=models.DateField(blank=True,null=True)
	fine=models.PositiveIntegerField(default=0)
	fine_status=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)+" | "+str(self.book)

class TransactionStack(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	book=models.ForeignKey(Book,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)



