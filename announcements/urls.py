from django.urls import path
from . import views

app_name="announcements"

urlpatterns = [
    path('push/',views.announcement_create,name="announcements-create"),
    path('edit/<str:slug>/',views.announcement_edit,name="announcements-edit"),
    path('delete/<str:slug>/',views.announcement_delete,name="announcements-delete"),
    path('delete/confirm/<str:slug>/',views.announcement_delete_confirm,name="announcements-delete-confirm"),
]