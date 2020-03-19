from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from accounts.models import User
from transactions.models import Transaction,TransactionStack

def kiosk_home(request):
	if(request.user.is_authenticated):
		user=request.user
		TransactionStack.objects.filter(user=user).delete()
		logout(request)
	return render(request,'kiosk/kiosk_home.html')

def kiosk_opPicker(request):
	if(request.method=='POST'):
		userBarcode=request.POST['userBarcode']
		userPin=request.POST['userPin']
		if(User.objects.filter(barcode=userBarcode).exists()):
			user=User.objects.get(barcode=userBarcode)
			if(user.pin==userPin):
				login(request,user)
				return render(request,'kiosk/kiosk_opPicker.html')
			else:
				messages.success(request,f'Incorrect PIN!')

		else:
			messages.success(request,f'Invalid User !')

	else:
		messages.success(request,f'Request Error - Action undefined !')

	return redirect('/kiosk')

def kioskClose(request,reciept):
	return render(request,"kiosk/kioskClose.html",{'reciept':reciept})