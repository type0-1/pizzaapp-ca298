from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from django.utils import timezone

class UserSignupForm(forms.ModelForm):
    # Passing in widget attributes to forms.field_name to apply prettier styling and looks to form 
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'})) 
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}), # Widget form, same as below line 
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        user.set_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user

# Form that handles the login and user authentication

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class OrderForm(ModelForm):
    class Meta:
        model = Pizza
        fields = "__all__" # Includes all fields from the Pizza Model, including booleans.

        # Making every field a widget except for boolean fields.
        widgets = {
            'size': forms.Select(attrs={'class': 'form-control'}),
            'crust': forms.Select(attrs={'class': 'form-control'}),
            'cheese': forms.Select(attrs={'class': 'form-control'}),
            'sauce': forms.Select(attrs={'class': 'form-control'}),
        }

class DeliveryForm(ModelForm):
    class Meta:
        model = DeliveryDetail
        fields = "__all__" # Include all fields from the DeliveryDetail Model.

        # Same as OrderForm, making every field a widget for better styling.
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'card_no': forms.TextInput(attrs={'class': 'form-control'}),
            'card_exp': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):

        # Retrieving data that the user has submitted into the form for validation checks.

        data = self.cleaned_data
        cvv = data.get('cvv') # Get CVV for validation
        card_no = data.get('card_no') # Get card_no for validation
        card_exp = data.get('card_exp') # Get card_exp for validation

        # Helper functions to go through validation.

        # validate_cvv, performs validations on CVV number.

        def validate_cvv(cvv):
            if not cvv.isnumeric() or len(cvv) != 3: # Checks if CVV are all digits and is of length 3.
                raise forms.ValidationError(f'Your CVV number {cvv} is invalid, please try again!')

        # validate_cardno, performs multiple validations on the card number.
            
        def validate_cardno(card_no):
            if len(card_no) != 19: # Checks for correct length
                raise forms.ValidationError(f'Your card number {card_no} is not long enough, please try again!')
            elif card_no.count("-") != 3: # Checks for proper card formatting
                raise forms.Validation(f'Invalid card number {card_no}, please try again!')
            else:
                for num in card_no.split("-"):
                    if not num.isnumeric(): # Checks if each section of digits are numbers
                        raise forms.ValidationError(f'The digits "{num}" is invalid for a card number, please try again!')
        
        # validate_expiry, performs multiple validations on card expiry number.
        def validate_expiry(card_exp):
            if card_exp.count("/") != 1: # Checks for proper formatting.
                raise forms.ValidationError(f'Invalid formatting of expiry date, make sure expiry is of the form "MM/YY')
            else:
                current_time = timezone.now() # Gets the current time.
                times = [int(num) for num in card_exp.split("/")] # Creates a list in the form of [Day, Month, Year]
                if (int(str(current_time.year)[2:]) > times[1]) or times[0] > 12: # Checks for proper date formatting.
                    raise forms.ValidationError(f'The expiry year is invalid {times[0]}/{times[1]}, please try again!')
                else:
                    for time in times: 
                        if time < 0: # Checks that each number is negative.
                            raise forms.ValidationError(f'An expiry date cannot have negative numbers, please try again!')
        
        # Call each function to perform validations.
                        
        validate_cvv(cvv)
        validate_expiry(card_exp)
        validate_cardno(card_no)