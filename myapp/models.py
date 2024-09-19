# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    registered_name = models.TextField(blank=False, null=True)
    gst_number = models.CharField(max_length=15, blank=False, null=True)
    registered_address = models.TextField(blank=False, null=True)
    poc_name = models.CharField(max_length=255, blank=False, null=True)
    services_type = models.TextField(blank=True, null=True)  # Store the services as a comma-separated string
    company_media = models.FileField(upload_to='company_media/', blank=True, null=True)
    top_clients = models.FileField(upload_to='top_clients/', blank=True, null=True)
    awards = models.FileField(upload_to='awards/', blank=True, null=True)

    # New fields
    company_size = models.CharField(
        max_length=50,
        choices=[
            ('<10', '<10 employees'), 
            ('10-20', '10-20 employees'), 
            ('20-50', '20-50 employees'),
            ('50-100', '50-100 employees'),
            ('100-500', '100-500 employees'), 
            ('>500', '>500 employees')
        ],
        blank=False, 
        null=True
    )
    
    truck_ownership = models.CharField(
        max_length=50, 
        choices=[
            ('own', 'Own trucks'), 
            ('aggregator', 'Aggregator (we do not own trucks)')
        ], 
        blank=False, 
        null=True
    )
    call_support = models.BooleanField(default=False)  # Yes/No for 24/7 call support
    running_business_since = models.PositiveIntegerField(null=True, blank=False)  # Year

    
    def __str__(self):
        return self.user.username

class Product(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    from_city = models.CharField(max_length=255)
    to_city = models.CharField(max_length=255)
    shifting_plan = models.CharField(max_length=20, choices=[('7 days', 'In next 7 days'), ('15 days', 'In next 15 days'), ('30 days', 'In next 30 days'), ('30+ days', 'In next 30+ days')])
    item_details = models.TextField()
    call_preference = models.BooleanField(default=False)
    call_time = models.TimeField(blank=True, null=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    specific_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_quote_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_city} to {self.to_city} - {self.buyer.username}"


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')  # Set your upload path

    def __str__(self):
        return f"Image for {self.product}"
    

class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    bid_date = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=False) 

    def __str__(self):
        return f"Bid by {self.seller.user.username} on {self.product.from_city} to {self.product.to_city}"

class Deal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    status_choices = [
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Under Review')
    deal_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deal on {self.product.from_city} to {self.product.to_city} with {self.seller.user.username}"
