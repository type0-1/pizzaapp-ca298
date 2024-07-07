import re
from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random 

# For rendering the index (main) page 
def index(request):
    return render(request, 'index.html')

# Invoking and enabling user sign-up

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('previous_orders') # Redirect user to previous orders page when signed in.

# View for logging in.
    
class UserLoginView(LoginView):
    template_name='login.html'

# Function that redirects user after logging out.
    
def logout_user(request):
    logout(request)
    return redirect("/")

# Function for creating a pizza.

@login_required
def create(request):
    if request.method == "POST": 
        form = OrderForm(request.POST) # Creates a new instance of the order form.
        if form.is_valid(): 
            pizza = form.save() # Save the details of the form the user has picked
            user = request.user # Get the user
            Order.objects.create(user=user, pizza=pizza, date_of_order=timezone.now()) # Create a new order object associated with the user, pizza details and time created.
            return redirect('details') # Redirect to details page for further purchase.
        else:
            return render(request, 'create.html', {'form':form}) # Failure, show the user the page again.
    else:
        form = OrderForm() # It's a GET request, create a new instance of the form and show the user.
        return render(request, 'create.html', {'form':form})

@login_required
def details(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST) # Create a new instance of the DeliveryForm.
        if form.is_valid():
            details = form.save() # Save the details of the delivery form page.
            user = request.user # Get the user
            # Gets the latest order by sorting by the most recent time using date_of_order field.
            order = (Order.objects.filter(user=user)).latest('date_of_order')
            return render(request, 'confirm.html', {'details':details, 'pizza':order.pizza, 'order':order, 'time':random.randint(30, 45)})
        else:
            return render(request, 'details.html', {'form':form}) # Failure, show the user the page again.
    else:
        form = DeliveryForm() # A GET request, create a new instance of the form and show the user.
        return render(request, 'details.html', {'form':form})

@login_required
def previous_orders(request):
    user = request.user # Get the user
    orders = Order.objects.filter(user=user) # Filter all objects created by the user

    # Show all previous orders from the user, from most recent on the top of the page to oldest on the bottom ([::-1])"""

    return render(request, 'previous_orders.html', {'orders':[order for order in orders][::-1]})