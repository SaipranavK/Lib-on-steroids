from django.urls import path
from . import views

app_name="suggestions"

urlpatterns = [
    path('push/',views.suggestion_create,name="suggestions-create"),
]