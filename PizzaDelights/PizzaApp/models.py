from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#... any other imports

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.AutoField(primary_key=True) # An ID key that will be primarily used (primary key) for referencing.
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

# Size model for choosing the size of the pizza.
class Size(models.Model):
    SIZE_CHOICES = [("S", "Small"), ("M", "Medium"), ("L", "Large"),
                     ("XL", "Extra Large")]
    
    size = models.CharField(choices=SIZE_CHOICES, default=SIZE_CHOICES[0], max_length=20)

    def __str__(self):
        return self.size

# Crust model for choosing the type of crust for the pizza.
class Crust(models.Model):
    
    crust = models.CharField(max_length=20)

    def __str__(self):
        return self.crust

# Cheese model for choosing the type of cheese for the pizza.
class Cheese(models.Model):
    cheese = models.CharField(max_length=20)

    def __str__(self):
        return self.cheese

# Sauce model for choosing the type of sauce for the pizza.
class Sauce(models.Model):
    sauce = models.CharField(max_length=20)

    def __str__(self):
        return self.sauce

# Pizza model, consisting of foreign keys along with toppings (boolean fields)
class Pizza(models.Model):
    id = models.AutoField(primary_key=True)
    
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE)

    # Toppings for the pizza
    
    pepperoni = models.BooleanField(default=False)
    chicken = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    pineapple = models.BooleanField(default=False)
    peppers = models.BooleanField(default=False)
    mushrooms = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)
    pear = models.BooleanField(default=False)
    garlic = models.BooleanField(default=False)
    jalepenos = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.size} {self.crust} Pizza with {self.sauce} sauce'

# Order model for creating orders from the user.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    date_of_order = models.DateTimeField()

    def __str__(self):
        return f'Order {self.id}'

# Delivery Details model to display and take in delivery details.
class DeliveryDetail(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=150)
    card_no = models.CharField(max_length=19)
    card_exp = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)