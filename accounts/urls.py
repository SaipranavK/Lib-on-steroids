from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('login/',views.login_view,name="accounts-login"),
    path('logout/',views.logout_view,name="accounts-logout"),
    path('profile/',views.profile,name="accounts-profile"),
    path('setup/',views.setup,name="accounts-setup"),
]