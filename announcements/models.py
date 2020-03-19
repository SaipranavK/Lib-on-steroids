from django.db import models

class Announcement(models.Model):
	content=models.TextField()
	date_posted=models.DateField(auto_now_add=True)
	attachments=models.FileField(blank=True,upload_to="announcements")
	slug=models.SlugField(unique=True)

	def __str__(self):
		return str(self.content)+" | "+str(self.date_posted)