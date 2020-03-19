from django.urls import path
from . import views

app_name="fine"

urlpatterns = [
    path('manage/',views.fine_manager,name="fine-manager"),
]