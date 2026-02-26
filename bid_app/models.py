from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member_fee(models.Model):
    fee = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.fee

class AuctionUser (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user_type = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, default="pending")
    membership = models.ForeignKey('Member_fee', on_delete=models.CASCADE, null=True, blank=True)  # Ensure Member_fee is defined
    created = models.DateTimeField(auto_now_add=True)
    adhar_card = models.FileField(null=True, blank=True)
    pan_card = models.FileField(null=True, blank=True)
    bank_statement = models.FileField(null=True, blank=True)
    adhar_number = models.CharField(max_length=100, null=True, blank=True)
    pan_number = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    email_verification = models.BooleanField(null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

"""class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name+" "+self.category.name"""

class Product(models.Model):
    status = models.CharField(max_length=100, null=True, default='pending')  # Status of the product
    bid_type = models.CharField(max_length=100, null=True)  # Auction type (Auction or Tender)
    payment_status = models.CharField(max_length=100, null=True, default='pending')  # Payment status
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='winner')  # Winner of the auction
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='seller')  # Seller of the product
    name = models.CharField(max_length=100, null=True)  # Product name
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Base price of the product
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Quantity in kg
    images = models.ImageField(upload_to='product_images/', null=True)  # Product images
    start_session_date = models.DateTimeField(null=True, blank=True)  # Start date for the auction
    end_session_date = models.DateTimeField(null=True, blank=True)  # End date for the auction
    parameter = models.TextField(null=True, default="{}")  # Parameters related to the product
    description = models.TextField(null=True, blank=True)  # Product description
    comment = models.TextField(null=True, blank=True)  # Comments related to the product
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Timestamp for when the product was created
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Category of the product

    def __str__(self):
        return self.name

class Participants(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    new_price = models.IntegerField(null=True,default=0)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username+ " " + self.product.name

class ParticipantsHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    new_price = models.IntegerField(null=True,default=0)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username+ " " + self.product.name


class Send_Feedback(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.profile.username
    
#models 
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)  # Name of the course
    description = models.TextField(blank=True)  # Description of the course
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the course was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the course was last updated

    def __str__(self):
        return self.name  # Return the name of the course when the object is printed

"""class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # e.g., 'active', 'won', 'lost'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.bid_amount}"""