from django import forms
from .models import Fine

class FineForm(forms.ModelForm):
	class Meta:
		model=Fine
		fields=['fine_per_day','fine_threshold']

	
		