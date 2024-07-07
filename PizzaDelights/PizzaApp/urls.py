from django.urls import path
from . import views
from .forms import *

# Paths to navigate through the website. 

urlpatterns = [
   path('', views.index, name="index"),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name="login"),
   path('logout/', views.logout_user, name="logout"),
   path('create/', views.create, name="create"),
   path('details/', views.details, name="details"),
   path('previous_orders/', views.previous_orders, name="previous_orders")
]