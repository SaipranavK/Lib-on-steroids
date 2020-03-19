from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Profile

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model=Profile
		fields=['image','bio']

class LoginForm(AuthenticationForm):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label or 'username'
		self.fields['username'].help_text = None
		self.fields['username'].label = False
		self.fields['password'].widget.attrs['placeholder'] = self.fields['password'].label or 'password'
		self.fields['password'].help_text = None
		self.fields['password'].label = False