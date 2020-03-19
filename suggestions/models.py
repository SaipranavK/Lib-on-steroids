from django.db import models
from accounts.models import User

class Suggestion(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.TextField()
	date=models.DateField(auto_now_add=True)

	def __str__(self):
		return str(self.user)

