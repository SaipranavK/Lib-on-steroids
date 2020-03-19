from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.contrib.auth.decorators import user_passes_test

from accounts.models import User
from catalog.models import Book
from transactions.models import Transaction

from accounts.resources import StudentResource
from catalog.resources import BookResource
from transactions.resources import TransactionResource

@user_passes_test(lambda u: u.is_staff)
def BulkImport(request):
	if(request.method=="POST" and request.FILES['Updfile'] and 'college' in request.POST and 'model' in request.POST):
		data_model=request.POST['model']
		Updfile=request.FILES['Updfile']
		college=request.POST['college']

		default_group="support@owlstack.in"

		from_email=settings.EMAIL_HOST_USER
		to_email=[default_group]

		subject="Bulk Addition to Model - "+data_model
		text_body=render_to_string("additions.txt")
		html_template=render_to_string("additions.html",{'college':college,'data_model':data_model})

		message=EmailMultiAlternatives(subject=subject,body=text_body,from_email=from_email,to=to_email)
		message.attach(Updfile.name,Updfile.read(),Updfile.content_type)
		message.attach_alternative(html_template,'text/html')
		message.send()

		messages.success(request,f'Bulk additions request generated. Turn around in 24 hours')
		return redirect("/core/")

	else:
		messages.success(request,f'Request failed.Please provide valid information or contact support')
		return redirect("/core/")

@user_passes_test(lambda u: u.is_staff)
def DataExports(request):
	if(request.method=="POST"):
		if('Users' in request.POST):
			data_model=StudentResource()

			if('DepartmentName' in request.POST):
			    dept=request.POST['DepartmentName']
			    queryset=User.objects.filter(branch=dept)
			    dataset=data_model.export(queryset)
			else:
				dataset=data_model.export()

			response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
			response['Content-Disposition'] = 'attachment; filename="users.xls"'

		elif('Catalog' in request.POST):
			data_model=BookResource()

			if('filterType' in request.POST):
			    filterType=request.POST['filterType']
			    filterVal=request.POST['filterVal']

			    if(filterType=='category'):
			        queryset=Book.objects.filter(book_category=filterVal)

			    elif(filterType=='title'):
			        queryset=Book.objects.filter(book_title=filterVal)

			    dataset=data_model.export(queryset)

			else:
			    dataset=data_model.export()
			response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
			response['Content-Disposition'] = 'attachment; filename="books.xls"'

		elif('Transactions' in request.POST):

		    data_model=TransactionResource()

		    if('DepartmentName' in request.POST):
		        dept=request.POST['DepartmentName']
		        queryset=User.objects.filter(branch=dept)
		        dataset=data_model.export(queryset)

		    else:
			    dataset=data_model.export()

		    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
		    response['Content-Disposition'] = 'attachment; filename="transactions.xls"'

		return response

		'''except:
			messages.success(request,f'Action undefined')
			return redirect("/core/")'''
	else:
		messages.success(request,f'Action undefined')
		return redirect("/core/")


