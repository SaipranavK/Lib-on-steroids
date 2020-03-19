from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Fine
from .forms import FineForm

@user_passes_test(lambda u: u.is_staff)
def fine_manager(request):
	if(request.method=='POST'):
		fine=Fine.objects.get(pk=1)
		fineForm=FineForm(request.POST,instance=fine)
		if(fineForm.is_valid()):
			fineForm.save()
			messages.success(request,f'Fine updated!')
			return redirect("/core/")
		
		messsages.success(request,f'Validation error - Explicit or invalid data format !')
		return redirect("/core/")

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/core/')	
				