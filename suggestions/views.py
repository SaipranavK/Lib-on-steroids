from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SuggestionForm

@login_required(login_url="accounts:accounts-login")
def suggestion_create(request):
	if(request.method=="POST"):
		suggForm=SuggestionForm(request.POST)
		if(suggForm.is_valid()):
			instance=suggForm.save(commit=False)
			instance.user=request.user
			instance.save()
			messages.success(request,f'Thanks for your feedback. We will work on it to imporve your experience.')
			return redirect('/controls/')
		
		messages.success(request,f'Validation error - Explicit or invalid data format !')
		return redirect('/controls/')

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/controls/')


