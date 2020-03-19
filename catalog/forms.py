from django import forms
from .models import Book

class BookForm(forms.ModelForm):
	class Meta:
		model=Book
		exclude=('book_date_added',)

class SearchForm(forms.Form):
	query=forms.CharField(max_length=100)
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['query'].widget.attrs['placeholder'] = self.fields['query'].label or 'Search Book'
		self.fields['query'].help_text = None
		self.fields['query'].label = False
			