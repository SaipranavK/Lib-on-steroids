from django.urls import path
from . import views

app_name="kiosk"

urlpatterns = [
    path('',views.kiosk_home,name="kiosk-home"),
    path('opPicker/',views.kiosk_opPicker,name="kiosk-opPicker"),
    path('close/<reciept>',views.kioskClose,name="kiosk-Close"),
]