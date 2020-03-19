from django.db import models
from django.urls import reverse
from accounts.models import User

class Post(models.Model):

	title=models.CharField(max_length=100)
	content=models.TextField()
	date_posted=models.DateTimeField(auto_now_add=True)
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	thumbnail=models.ImageField(blank=True,upload_to='post_media')
	slug=models.SlugField(unique=True)

	def __str__(self):
		return self.title+" | "+str(self.author)+" | "+str(self.date_posted)

