from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.models import User
from .models import Announcement
from .forms import AnnouncementForm

@user_passes_test(lambda u: u.is_staff)
def announcement_create(request):
	if(request.method=='POST'):
		announcementForm=AnnouncementForm(request.POST,request.FILES)
		if(announcementForm.is_valid()):
			instance=announcementForm.save(commit=False)
			count=Announcement.objects.all().count()
			instance.slug="announcement-"+str(count)+"-"+str(instance.content)
			instance.save()
			messages.success(request,f'Announcement Posted !')
			return redirect('/controls/')
		
		messages.success(request,f'Validation error - Explicit or invalid data format !')
		
	else:
		announcementForm=AnnouncementForm()

	return render(request,'announcements/announcement_create.html',{'announcementForm':announcementForm})

@user_passes_test(lambda u: u.is_staff)
def announcement_edit(request,slug):
	announcement=Announcement.objects.get(slug=slug)
	if(request.method=='POST'):
		announcementEditForm=AnnouncementForm(request.POST,request.FILES,instance=announcement)
		if(announcementEditForm.is_valid()):
			announcementEditForm.save()
			messages.success(request,f'Announcement Updated !')
			return redirect("/controls/")

		messages.success(request,f'Validation error - Explicit or invalid data format !')
		return redirect('/controls/')
		
	else:
		editForm=AnnouncementForm(instance=announcement)
		return render(request,"announcements/announcement_edit.html",{'announcement':announcement,'editForm':editForm})

@user_passes_test(lambda u: u.is_staff)	
def announcement_delete_confirm(request,slug):
	if(request.method=='POST'):
		announcement=Announcement.objects.get(slug=slug)
		return render(request,"announcements/announcement_delete_confirm.html",{'announcement':announcement})
	
	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/controls/')

@user_passes_test(lambda u: u.is_staff)
def announcement_delete(request,slug):
	if(request.method=='POST'):
		Announcement.objects.get(slug=slug).delete()
		messages.success(request,f'Announcement deleted !')
		return redirect("/controls/")
		
	else:
		messages.success(request,f'Request Error - Undefined Action !')
		return redirect('/controls/')		