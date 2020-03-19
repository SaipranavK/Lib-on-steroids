from django.shortcuts import render_to_response,redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string,get_template
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
from accounts.models import User
from catalog.models import Book
from fine.models import Fine
from .models import Transaction,TransactionStack

from django.db.models import Count,Q
import json

import datetime

@user_passes_test(lambda u: u.is_staff)
def transaction_manager(request):
	if('user' in request.POST and 'issue' in request.POST and request.method=='POST'):
		transactionStack=TransactionStack.objects.filter(user=request.user)
		temp=request.POST['user']
		if(User.objects.filter(username=temp).exists()):
			user=User.objects.get(username=temp)
		else:
			messages.success(request,f'Transaction Failed - User/RollNo Doesnt Exist')
			return redirect('/core/')

		for instance in transactionStack:
			if(Book.objects.filter(book_number=instance.book.book_number).exists()):
				book=Book.objects.get(book_number=instance.book.book_number)
				if(Transaction.objects.filter(user=user,book=book,return_date=None).exists()):
					TransactionStack.objects.filter(user=request.user).delete()
					messages.success(request,f'Book Already issued in a previous transaction. Cannot issue same book multiple times.Please return it first to renew/re-issue the book')
					return redirect('/core/')

				Transaction.objects.create(user=user,book=book)
				book.book_quantity-=1
				book.save()

			else:
				TransactionStack.objects.filter(user=request.user).delete()
				messages.success(request,f'Transaction Failed - Please try again')
				return redirect('/core/')

		TransactionStack.objects.filter(user=request.user).delete()
		messages.success(request,f'Transaction created Successfully')
		return redirect('/core/')

	elif('user' in request.POST and 'return' in request.POST and request.method=='POST'):
		transactionStack=TransactionStack.objects.filter(user=request.user)
		temp=request.POST['user']
		if(User.objects.filter(username=temp).exists()):
			user=User.objects.get(username=temp)
		else:
			messages.success(request,f'Return Failed - User/RollNo Doesnt Exist')
			return redirect('/core/')
		for instance in transactionStack:
			if(Transaction.objects.filter(user=user,book=instance.book,return_date=None).exists()):
				return_instance=Transaction.objects.get(user=user,book=instance.book,return_date=None)
				if(Book.objects.filter(book_number=return_instance.book.book_number).exists()):
					book=Book.objects.get(book_number=return_instance.book.book_number)
					return_instance.return_date=datetime.datetime.now().date()
					return_instance.fine_status=True
					return_instance.save()
					book.book_quantity+=1
					book.save()
				else:
					TransactionStack.objects.filter(user=request.user).delete()
					messages.success(request,f'Return Failed - Please try again')
					return redirect('/core/')
			else:
				TransactionStack.objects.filter(user=request.user).delete()
				messages.success(request,f'Return Failed - Please try again')
				return redirect('/core/')

		TransactionStack.objects.filter(user=request.user).delete()
		messages.success(request,f'Return Successful')
		return redirect('/core/')

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/core/')


def transaction_manager_kiosk(request):
	if('user' in request.POST and 'issue' in request.POST and request.method=='POST'):
		transactionStack=TransactionStack.objects.filter(user=request.user)
		temp=request.POST['user']
		books=[]
		if(User.objects.filter(username=temp).exists()):
			user=User.objects.get(username=temp)
		else:
			messages.success(request,f'Transaction Failed - User/RollNo Doesnt Exist')
			return redirect('/kiosk/')

		if(len(transactionStack)==0):
			messages.success(request,f'Transaction Failed - Please try again')
			return redirect('/kiosk/')

		for instance in transactionStack:
			if(Book.objects.filter(book_number=instance.book.book_number).exists()):
				book=Book.objects.get(book_number=instance.book.book_number)
				books.append(book)
				if(Transaction.objects.filter(user=user,book=book,return_date=None).exists()):
					TransactionStack.objects.filter(user=request.user).delete()
					messages.success(request,f'Book Already issued in a previous transaction. Cannot issue same book multiple times.Please return it first to renew/re-issue the book')
					return redirect('/kiosk/')

				Transaction.objects.create(user=user,book=book)
				book.book_quantity-=1
				book.save()

			else:
				TransactionStack.objects.filter(user=request.user).delete()
				messages.success(request,f'Transaction Failed - Please try again')
				return redirect('/kiosk/')

		TransactionStack.objects.filter(user=request.user).delete()
		messages.success(request,f'Transaction created Successfully')

		user = request.user
		date= datetime.datetime.now()
		college= "Demo College"
		transType="Book Issue"

		html_string = render_to_string('kiosk/kioskPrint.html', {'user': user,'date':date,'college':college,'transType':transType,'books':books})

		html = HTML(string=html_string)
		html.write_pdf(target='/tmp/transaction-reciept.pdf');

		from_email=settings.EMAIL_HOST_USER
		to_email=[request.user.email]

		subject="SPI - Transaction Receipt"
		html_template=render_to_string('kiosk/SPIMail.html')
		text_body="Transaction details of your recent activity at SPI powered Library"


		fs = FileSystemStorage('/tmp')
		with fs.open('transaction-reciept.pdf') as pdf:
			receipt=pdf
			receipt.content_type='application/pdf'
			message=EmailMultiAlternatives(subject=subject,body=text_body,from_email=from_email,to=to_email)
			message.attach(receipt.name, receipt.read(), receipt.content_type)
			message.attach_alternative(html_template,'text/html')
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="transaction-receipt.pdf"'
			message.send()
			return response

		return response


	elif('user' in request.POST and 'return' in request.POST and request.method=='POST'):
		transactionStack=TransactionStack.objects.filter(user=request.user)
		temp=request.POST['user']
		books=[]
		if(User.objects.filter(username=temp).exists()):
			user=User.objects.get(username=temp)
		else:
			messages.success(request,f'Return Failed - User/RollNo Doesnt Exist')
			return redirect('/kiosk/')

		if(len(transactionStack)==0):
			messages.success(request,f'Return Failed - Please try again')
			return redirect('/kiosk/')

		for instance in transactionStack:
			if(Transaction.objects.filter(user=user,book=instance.book,return_date=None).exists()):
				return_instance=Transaction.objects.get(user=user,book=instance.book,return_date=None)
				if(Book.objects.filter(book_number=return_instance.book.book_number).exists()):
					book=Book.objects.get(book_number=return_instance.book.book_number)
					return_instance.return_date=datetime.datetime.now().date()
					return_instance.fine_status=True
					return_instance.save()
					book.book_quantity+=1
					book.save()
				else:
					TransactionStack.objects.filter(user=request.user).delete()
					messages.success(request,f'Return Failed - Please try again')
					return redirect('/kiosk/')
			else:
				TransactionStack.objects.filter(user=request.user).delete()
				messages.success(request,f'Return Failed - Please try again')
				return redirect('/kiosk/')

		TransactionStack.objects.filter(user=request.user).delete()
		messages.success(request,f'Return Successful')

		user = request.user
		date= datetime.datetime.now()
		college= "Demo College"
		transType="Book Return"

		html_string = render_to_string('kiosk/kioskPrint.html', {'user': user,'date':date,'college':college,'transType':transType,'books':books})

		html = HTML(string=html_string)
		html.write_pdf(target='/tmp/transaction-reciept.pdf');

		from_email=settings.EMAIL_HOST_USER
		to_email=[request.user.email]

		subject="SPI - Transaction Receipt"
		html_template=render_to_string('kiosk/SPIMail.html')
		text_body="Transaction details of your recent activity at SPI powered Library"


		fs = FileSystemStorage('/tmp')
		with fs.open('transaction-reciept.pdf') as pdf:
			receipt=pdf
			receipt.content_type='application/pdf'
			message=EmailMultiAlternatives(subject=subject,body=text_body,from_email=from_email,to=to_email)
			message.attach(receipt.name, receipt.read(), receipt.content_type)
			message.attach_alternative(html_template,'text/html')
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="transaction-receipt.pdf"'
			message.send()
			return response

		return response

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/kiosk/')


def transaction_stack_kiosk(request):
	user=request.user
	transactionStack=TransactionStack.objects.filter(user=user)
	return render_to_response('transactions/ajax_transStack.html',{'transactionStack':transactionStack})

def transaction_stack(request):
	user=request.user
	transactionStack=TransactionStack.objects.filter(user=user)
	return render_to_response('transactions/ajax_transStack.html',{'transactionStack':transactionStack})

def admin_trans_search(request):
	query=request.GET.get('admintransquery',None)
	if(User.objects.filter(username=query).exists()):
		user=User.objects.get(username=query)
		transactions=Transaction.objects.filter(user=user)
		result=True
	else:
		result=False
		transaction=transactions.objects.all()
	return render_to_response('transactions/ajax_trans_search.html',{'transactions':transactions,'result':result})


def admin_user_search(request):
	query=request.GET.get('userquery',None)
	if(User.objects.filter(username=query).exists()):
		user=User.objects.get(username=query)
		result=True
	else:
		user=None
		result=False
	return render_to_response('transactions/ajax_user_search.html',{'user':user,'result':result})


def transactionStackAdd(request):
	book_number=request.GET.get('book_number',None)
	try:
		if(Book.objects.filter(book_number=book_number).exists()):
			book=Book.objects.get(book_number=book_number)
			user=request.user
			if(TransactionStack.objects.filter(user=user,book=book).exists()):
				message="Book already in queue.Please select another book or create the transaction."
			else:
				TransactionStack.objects.create(user=user,book=book)
				message="Book added for transaction"
		else:
			message="No matching Book"
	except:
		message="Inclusion Error - Invalid Book or unauthorised access requested. Try again | "+book_number+str(request.user)

	return render_to_response('transactions/trans_messages.html',{'message':message})


def transactionStackDelete(request):
	book_number=request.GET.get('book_number',None)
	try:
		if(Book.objects.filter(book_number=book_number).exists()):
			book=Book.objects.get(book_number=book_number)
			user=request.user
			if(TransactionStack.objects.filter(user=user,book=book).exists()):
				TransactionStack.objects.get(user=user,book=book).delete()
				message="Book delete from queue"
			else:
				message="Book doesnt exist in queue"
	except:
		message="Inclusion Error - Invalid Book or unauthorised access requested. Try again | "+book_number

	return render_to_response('transactions/trans_messages.html',{'message':message})


@user_passes_test(lambda u: u.is_staff)
def transactionFilters(request):
	query=request.GET.get('filter',None)
	if(query=="all"):
		filter_type="All";
		transactions=Transaction.objects.all()
	elif(query=="month"):
		filter_type="Last 30 Days";
		transactions=Transaction.objects.filter(issue_date__gte=(datetime.datetime.now()-datetime.timedelta(days=30)).date()).order_by('-issue_date')
	elif(query=="week"):
		filter_type="Last 7 Days";
		transactions=Transaction.objects.filter(issue_date__gte=(datetime.datetime.now()-datetime.timedelta(days=7)).date()).order_by('-issue_date')
	elif(query=="pending"):
		filter_type="Pending Returns";
		transactions=Transaction.objects.filter(return_date=None).order_by('-issue_date')
	else:
		transactions=Transaction.objects.all()

	return render_to_response('transactions/ajax_transFilter.html',{'filter_type':filter_type,'transactions':transactions})


@user_passes_test(lambda u:u.is_staff)
def chartsView(request):

	dataset=Transaction.objects.values('user__gender').annotate(male_count=Count('user__gender',filter=Q(user__gender="male")),female_count=Count('user__gender',filter=Q(user__gender='female')))

	categories=list()
	male_series_data=list()
	female_series_date=list()

	for entry in dataset:
		categories.append(entry['user__gender'])
		male_series_data.append(entry['male_count'])
		female_series_date.append(entry['female_count'])


	male_series={
		'name':'Male',
		'data':male_series_data,
		'color':'blue'
	}

	female_series={
		'name':'Female',
		'data':female_series_date,
		'color':'pink'
	}

	chart={
		'chart':{'type':'column'},
		'title':{'text':'Transactions Gender Ratio'},
		'xAxis':{'categories':categories},
		'series':[male_series,female_series]
	}

	dump=json.dumps(chart)

	return render_to_response('transactions/GenderChart.html',{'chart':dump})