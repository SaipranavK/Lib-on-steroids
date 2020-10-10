from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileUpdateForm
from .models import User

def login_view(request):
	if(request.method=='POST' and 'setup' not in request.POST):
		authForm=AuthenticationForm(data=request.POST)
		if(authForm.is_valid()):
			user=authForm.get_user()
			login(request,user)
			messages.success(request,f'Welcome Back')
			if(user.email=='' or user.pin=='0000'):
				return redirect("accounts:accounts-setup")
			else:
				return redirect('/core/')
		
		messages.success(request,f'Invalid Credentials!')
		return redirect('/')
	else:
		messages.success(request,f'Request Error - Action undefined !')
		return redirect('/')
		
def logout_view(request):
	logout(request)
	messages.success(request,f'Session Closed - Logged out !')
	return redirect('/')

@login_required(login_url="accounts:accounts-login")
def profile(request):
	if(request.method=='POST'):
		p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if(p_form.is_valid()):
			p_form.save()
			messages.success(request,f'Your Account has been Updated!')
			return redirect('/controls/')

	else:
		messages.success(request,f'Request Error - Action undefined !')
		return redirect('/controls/')
	

@login_required(login_url="accounts:accounts-login")
def setup(request):
	if('email' in request.POST and 'phone' in request.POST and 'password' in request.POST and 'pin' in request.POST and request.method=='POST'):
		email=request.POST['email']
		phone=request.POST['phone']
		password=request.POST['password']
		pin=request.POST['pin']

		user=request.user

		user.set_password(password)
		user.pin=pin
		user.email=email
		user.phone=phone

		user.save()

		logout(request)

		login(request,user)
		
		return redirect('/core/')

	else:
		return render(request, 'accounts/setup.html')

	
