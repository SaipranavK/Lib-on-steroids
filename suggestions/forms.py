from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
	class Meta:
		model=Suggestion
		fields=['content']

		def __init__(self, *args, **kwargs):
			super(SuggestionForm, self).__init__(*args, **kwargs)
			self.fields['content'].widget.attrs['placeholder'] = self.fields['content'].label or 'Your Suggestion'
			self.fields['content'].help_text = None
			self.fields['content'].label = False
		