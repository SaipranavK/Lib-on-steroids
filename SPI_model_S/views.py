from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Count,Q
import json

from accounts.models import User
from accounts.forms import LoginForm,ProfileUpdateForm
from announcements.models import Announcement
from blog.models import Post
from catalog.models import Book
from fine.models import Fine
from fine.forms import FineForm
from suggestions.models import Suggestion
from suggestions.forms import SuggestionForm
from transactions.models import Transaction,TransactionStack

def index(request):
	book_count=Book.objects.all().count()
	student_count=User.objects.filter(is_staff=False).count()
	male_count=User.objects.filter(gender="MALE").count()
	female_count=User.objects.filter(gender="FEMALE").count()
	transactions_count=Transaction.objects.all().count()
	postCount=Post.objects.all().count()
	annCount=Announcement.objects.all().count()
	suggCount=Suggestion.objects.all().count()
	staffCount=User.objects.filter(is_staff=True).count()
	recently_added=Book.objects.all().order_by('-id')[:20]
	authForm=LoginForm()

	if(request.user.is_authenticated):
		return redirect("/core/")
	else:
		if('query' in request.GET):
			query=request.GET['query']
			books=Book.objects.filter(Q(book_title__contains=query) | Q(book_author__contains=query) | Q(book_category__contains=query) | Q(book_number__contains=query))
			if(books):
				result=True
			else:
				result=False
			return render(request,'index.html',{'book_count':book_count,'student_count':student_count,'male_count':male_count,'female_count':female_count,'transactions_count':transactions_count,'authForm':authForm,'books':books,'result':result,'postCount':postCount,'annCount':annCount,'suggCount':suggCount,'staffCount':staffCount,'recently_added':recently_added})

		else:
			return render(request,'index.html',{'book_count':book_count,'student_count':student_count,'male_count':male_count,'female_count':female_count,'transactions_count':transactions_count,'authForm':authForm,'postCount':postCount,'annCount':annCount,'suggCount':suggCount,'staffCount':staffCount,'recently_added':recently_added})

@login_required(login_url="accounts:accounts-login")
def core(request):
	if(request.user.email=='' or request.user.pin=='0000'):
		logout(request)
		messages.success(request,f'Complete accounts setup to continue')
		return redirect('/')
	else:
		posts=Post.objects.all().order_by('-date_posted')
		announcements=Announcement.objects.all().order_by('-date_posted')
		books=Book.objects.all().order_by('-book_date_added')
		recently_added=Book.objects.all().order_by('-id')[:20]
		distinct = Transaction.objects.values('book').annotate(book_count=Count('book')).filter(book_count=1)
		trending=Transaction.objects.filter(book__in=[item['book'] for item in distinct]).order_by('-id')[:10]
		if(request.user.is_staff):
			transactions=Transaction.objects.all()
			transactionStack=TransactionStack.objects.filter(user=request.user)
			suggestions=Suggestion.objects.all().order_by('-date')
			return render(request,'core.html',{'posts':posts,'announcements':announcements,'books':books,'recently_added':recently_added,'trending':trending,'suggestions':suggestions,'transactions':transactions,'transactionStack':transactionStack})
	    
		transactions=Transaction.objects.filter(user=request.user)
		return render(request,'core.html',{'posts':posts,'announcements':announcements,'transactions':transactions,'books':books,'recently_added':recently_added,'trending':trending})

@login_required(login_url="accounts:accounts-login")
def controls(request):
	user=request.user
	posts=Post.objects.filter(author=user).order_by('-date_posted')

	profileForm=ProfileUpdateForm(instance=user.profile)
	suggForm=SuggestionForm()

	return render(request,'controls.html',{'user':user,'posts':posts,'suggForm':suggForm,'profileForm':profileForm})


def search(request):
    return render(request,'search.html')

def about(request):
    book_count=Book.objects.all().count()
    student_count=User.objects.filter(is_staff=False).count()
    male_count=User.objects.filter(gender="MALE").count()
    female_count=User.objects.filter(gender="FEMALE").count()
    transactions_count=Transaction.objects.all().count()
    postCount=Post.objects.all().count()
    annCount=Announcement.objects.all().count()
    suggCount=Suggestion.objects.all().count()
    staffCount=User.objects.filter(is_staff=True).count()
    return render(request,'about.html',{'book_count':book_count,'student_count':student_count,'male_count':male_count,'female_count':female_count,'transactions_count':transactions_count,'postCount':postCount,'annCount':annCount,'suggCount':suggCount,'staffCount':staffCount})