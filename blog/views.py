from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Post
from .forms import PostForm

@login_required(login_url="accounts:accounts-login")
def blog_create(request):
	if(request.method=='POST'):
		postForm=PostForm(request.POST,request.FILES)
		if(postForm.is_valid()):
			instance=postForm.save(commit=False)
			instance.author=request.user
			count=Post.objects.all().count()
			instance.slug="post-"+str(count)+"-"+str(instance.title)
			instance.save()
			messages.success(request,f'Blog Post created !')
			return redirect('/controls/')
		
		messages.success(request,f'Validation error - Explicit or invalid data format !')
		
	else:
		postForm=PostForm()

	return render(request,'blog/blog_create.html',{'postForm':PostForm})

@login_required(login_url="accounts:accounts-login")
def blog_edit(request,username,slug):
	post=Post.objects.get(slug=slug)
	user=User.objects.get(username=username)
	if(post.author==user):		
		if(request.method=='POST'):
			postEditForm=PostForm(request.POST,request.FILES,instance=post)
			if(postEditForm.is_valid()):
				postEditForm.save()
				messages.success(request,f'Post updated !')
				return redirect("/controls/")

			messages.success(request,f'Validation error - Explicit or invalid data format !')
			return redirect('/controls/')
		
		else:
			editForm=PostForm(instance=post)
			return render(request,"blog/blog_edit.html",{'post':post,'editForm':editForm})
	else:
		messages.success(request,f'Authorization error - Illegal data access !')
		return redirect('/controls/')

@login_required(login_url="accounts:accounts-login")
def blog_delete_confirm(request,username,slug):
	if(request.method=='POST'):
		post=Post.objects.get(slug=slug)
		user=User.objects.get(username=username)
		if(post.author==user):
			return render(request,"blog/blog_delete_confirm.html",{'post':post,'user':user})
		else:
			messages.success(request,f'Authorization error - Illegal data access !')
			return redirect('/controls/')

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/controls/')

@login_required(login_url="accounts:accounts-login")
def blog_delete(request,username,slug):
	if(request.method=='POST'):
		post=Post.objects.get(slug=slug)
		user=User.objects.get(username=username)
		if(post.author==user):
			Post.objects.get(slug=slug).delete()
			messages.success(request,f'Blog Post deleted !')
			return redirect("/controls/")
		else:
			messages.success(request,f'Authorization error - Illegal data access !')
			return redirect('/controls/')

	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/controls/')		