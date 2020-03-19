from django.db import models
from accounts.models import User
from django.urls import reverse

TYPE_CHOICES = (
    ('E-Book Only','E-Book Only'),
    ('Hard Cover Only', 'Hard Cover Only'),
    ('Both Hard Cover and E-Book','Both Hard Cover and E-Book'),
)

class Book(models.Model):

	book_number=models.PositiveIntegerField(default=1,unique=True)
	book_title=models.CharField(max_length=30)
	book_author=models.CharField(max_length=30,default="No Info",blank=True,null=True)
	book_author2=models.CharField(max_length=30,default="No Info",blank=True,null=True)
	book_publisher=models.CharField(max_length=30,default="Information not available")
	book_category=models.CharField(max_length=30,null=True,blank=True)
	book_cost=models.PositiveIntegerField(default=0)
	book_language=models.CharField(max_length=30,default="ENG-US")
	book_type=models.CharField(max_length=26,choices=TYPE_CHOICES,default='Hard Cover Only')
	ebook_attachments=models.FileField(blank=True,upload_to="catalog/ebooks")
	book_quantity=models.PositiveIntegerField(default=100)
	book_shelf=models.CharField(max_length=10,default="1A")
	book_date_added=models.DateField(auto_now_add=True)

	def __str__(self):
		return str(self.book_number)