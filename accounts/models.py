from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image

GENDER_CHOICES = (
    ('male','male'),
    ('female', 'female'),
)

class User(AbstractUser):
    pass
    barcode=models.CharField(max_length=10,default="0000000000")
    gender=models.CharField(max_length=20,default="male",choices=GENDER_CHOICES)
    branch=models.CharField(max_length=50,default="Computer Science & Engineering")
    admission=models.DateField(auto_now_add=True)
    phone=models.CharField(max_length=15,default="+91 1231231231")
    pin=models.CharField(max_length=4,default='0000')

    def __str__(self):
    	return str(self.username)

class Profile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	image=models.ImageField(default="defaults/user.png",upload_to='profile_pics')
	bio=models.TextField(default="Default Bio",max_length=200)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img=Image.open(self.image.path)
		
		if(img.height>400 or img.width>400):
			output_size=(400,400)
			img.thumbnail(output_size)
			img.save(self.image.path)
