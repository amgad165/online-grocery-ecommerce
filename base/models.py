from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    COMPANY = 'company'
    PRIVATE = 'private'
    ROLE_CHOICES = [
        (COMPANY, 'Company'),
        (PRIVATE, 'Private'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    company_name = models.CharField(_('company name'), max_length=100, blank=True, null=True)
    atu_number = models.CharField(_('ATU number'), max_length=20, blank=True, null=True)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default=PRIVATE)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    address_type = models.CharField(max_length=255, choices=[('billing', 'Billing'), ('delivery', 'Delivery')], blank=True, null=True)

    bezirk = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    hausnummer = models.CharField(max_length=255)
    plz_zip = models.CharField(max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class InactiveCompanyUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Inactive Company User'
        verbose_name_plural = 'Inactive Company Users'


class DeliveryAddress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_addresses')
    bezirk = models.CharField(_('bezirk'), max_length=255)
    street_address = models.CharField(_('street address'), max_length=255)
    hausnummer = models.CharField(_('hausnummer'), max_length=255)
    plz_zip = models.CharField(_('postal code'), max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=255)
    additional_info = models.CharField(_('additional info'), max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.street_address}, {self.bezirk}, {self.plz_zip}'


    
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    unit = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=355, blank=True, null=True)
    delivery = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, choices=[('privat', 'Privat'), ('business', 'Business')])
    image = models.FileField(upload_to='product_images/')
    price = models.FloatField()
    customize = models.BooleanField(_('Customize'), default=False)
    view_homepage = models.BooleanField(default=False)

    class Meta:
        ordering = ['-customize', 'name']
    def calculate_total_cost(self):
        total_cost = 0
        # Iterate through each ProductIngredient related to this product
        for product_ingredient in self.ingredients.all():
            # Calculate the cost of the ingredient by multiplying its price with quantity
            ingredient_cost = product_ingredient.ingredient.price * product_ingredient.quantity
            # Add the ingredient cost to the total cost
            total_cost += ingredient_cost
        return total_cost

    def __str__(self):
        return self.name + '-' + self.category

# this model shows the ingredient set initially by the admin
class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL,blank=True, null = True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="quantity")  # Default quantity for the ingredient

    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name} - {self.quantity}"
    

# this model shows the ingredients customized by the user and this model represents the user orders.
class IngredientUserCustomize(models.Model):
    product = models.ForeignKey(Product, related_name='ingredients_customized', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL,blank=True, null = True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="quantity")  # Default quantity for the ingredient

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity} {self.ingredient.unit}"

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ingredients_customized = models.ManyToManyField(IngredientUserCustomize, related_name='order_items', blank=True )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_item_price(self):
        if not self.product.customize:
            # If product is not customizable, calculate based on regular price
            return int(self.quantity) * self.product.price
        else:
            # If product is customizable, calculate based on customized ingredients
            total_price = 0
            for customized_ingredient in self.ingredients_customized.all():

                total_price += customized_ingredient.quantity * customized_ingredient.ingredient.price * int(self.quantity)
            return total_price

    def get_total_order_quantity(self):
            # If product is customizable, calculate based on customized ingredients
            total_quantity = 0
            for customized_ingredient in self.ingredients_customized.all():

                total_quantity += customized_ingredient.quantity * int(self.quantity)
            return total_quantity

class Order(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem,related_name='order')
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Order {self.pk}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
 
        return total
    

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()

        return total
    
    def get_total_quantity(self):
        quantity = 0
        for order_item in self.items.all():
            quantity += order_item.quantity

        return quantity
    
class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)




# transaction model
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True,related_name='transaction_order')
    subscription_type = models.CharField(max_length=255, choices=[('active', 'Active'), ('non active', 'Non Active'),('one time purchase', 'One Time Purchase'),('cash', 'Cash')])


    def __str__(self):
        return f"user {self.user} - amount {self.amount} - created at {self.created_at} - order {self.order}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    telephone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255,null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name