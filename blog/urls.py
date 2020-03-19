from django.urls import path
from . import views

app_name="blog"

urlpatterns = [
    path('push/',views.blog_create,name="blog-create"),
    path('edit/<str:username>/<str:slug>/',views.blog_edit,name="blog-edit"),
    path('delete/<str:username>/<str:slug>/',views.blog_delete,name="blog-delete"),
    path('delete/confirm/<str:username>/<str:slug>/',views.blog_delete_confirm,name="blog-delete-confirm"),
    
]