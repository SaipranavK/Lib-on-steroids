from django.db import models

class Fine(models.Model):
	fine_per_day=models.PositiveIntegerField(default=1)
	fine_threshold=models.PositiveIntegerField(default=10)

	def __str__(self):
		return str(self.fine_per_day)+" | "+str(self.fine_threshold)