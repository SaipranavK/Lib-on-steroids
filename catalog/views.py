from django.shortcuts import render_to_response,render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm

@login_required(login_url="accounts:accounts-login")
def book_search(request):
	query=request.GET.get('query',None)
	books=Book.objects.filter(Q(book_title__contains=query) | Q(book_author__contains=query) | Q(book_category__contains=query) | Q(book_number__contains=query))
	result=True
	user=request.user
	return render_to_response('catalog/ajax_search.html',{'books':books[:20],'result':result,'user':user})

def book_searchpage(request):
	query=request.GET.get('query',None)
	books=Book.objects.filter(Q(book_title__contains=query) | Q(book_author__contains=query) | Q(book_category__contains=query) | Q(book_number__contains=query))
	result=True
	return render_to_response('catalog/ajaxSearchPage.html',{'books':books[:20],'result':result})

@login_required(login_url="accounts:accounts-login")
def book_trans_search(request):
	query=request.GET.get('transquery',None)
	books=Book.objects.filter(Q(book_title__contains=query) | Q(book_author__contains=query) | Q(book_category__contains=query) | Q(book_number__contains=query))
	result=True
	return render_to_response('catalog/ajax_TransSearch.html',{'books':books[:20],'result':result})


def book_mtrans_search(request):
	query=request.GET.get('mquery',None)
	books=Book.objects.filter(Q(book_title__contains=query) | Q(book_author__contains=query) | Q(book_category__contains=query) | Q(book_number__contains=query))
	result=True
	return render_to_response('catalog/ajax_TransSearch.html',{'books':books[:20],'result':result})

@login_required(login_url="accounts:accounts-login")
def book_create(request):
	if(request.method=='POST'):
		bookForm=BookForm(request.POST,request.FILES)
		if(bookForm.is_valid()):
			instance.save()
			messages.success(request,f'Book added to Catalog !')
			return redirect('/core/')

		messages.success(request,f'Validation error - Explicit or invalid data format !')

	else:
		bookForm=BookForm()

	return render(request,'catalog/book_create.html',{'bookForm':bookForm})

@login_required(login_url="accounts:accounts-login")
def book_edit(request,booknumber):
	book=Book.objects.get(book_number=booknumber)
	if(request.method=='POST'):
		bookEditForm=BookForm(request.POST,request.FILES,instance=book)
		if(bookEditForm.is_valid()):
			bookEditForm.save()
			messages.success(request,f'Book updated !')
			return redirect("/core/")

		messages.success(request,f'Validation error - Explicit or invalid data format !')
		return redirect('/core/')

	else:
		editForm=BookForm(instance=book)
		return render(request,"catalog/book_edit.html",{'book':book,'editForm':editForm})

@login_required(login_url="accounts:accounts-login")
def book_delete_confirm(request,booknumber):
	if(request.method=='POST'):
		book=Book.objects.get(book_number=booknumber)
		return render(request,"catalog/book_delete_confirm.html",{'book':book})

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/core/')

@login_required(login_url="accounts:accounts-login")
def book_delete(request,booknumber):
	if(request.method=='POST'):
		book=Book.objects.get(book_number=booknumber)
		Book.objects.get(book_number=booknumber).delete()
		messages.success(request,f'Book deleted from Catalog !')
		return redirect("/core/")
	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/core/')

