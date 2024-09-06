from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer, Seller

class CustomUserCreationForm(UserCreationForm):
    mobile_number = forms.CharField(required=True, max_length=10, help_text="Enter a valid 10-digit mobile number")

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2', 'email')

class BuyerRegistrationForm(forms.ModelForm):
    # mobile_number = forms.CharField(required=True, max_length=10)
    class Meta:
        model = Buyer
        fields = []  # No additional fields needed for buyer

class SellerRegistrationForm(forms.ModelForm):
    registered_name = forms.CharField(required=True)
    gst_number = forms.CharField(required=True)
    registered_address = forms.CharField(required=True)
    owner_poc_name = forms.CharField(required=True)
    # contact_number = forms.CharField(required=True)
    # email_id = forms.EmailField(required=True)
    # company_name = forms.CharField(required=True)  # Required for seller registration
    services_type = forms.MultipleChoiceField(
        choices=[
            ('packing_source', 'Packing at source'),
            ('unpacking_destination', 'Unpacking at destination'),
            ('packing_material', 'Packing material'),
            ('insurance', 'Insurance'),
            ('loading_source', 'Loading at source'),
            ('unloading_destination', 'Unloading at destination'),
            ('warehousing', 'Warehousing'),
            ('specialized_boxes_electronics', 'Specialized boxes for electronics'),
            ('specialized_boxes_vehicle', 'Specialized boxes for vehicle'),
            ('specialized_boxes_pet', 'Specialized boxes for pet'),
            ('specialized_boxes_plant', 'Specialized boxes for plant')
        ],
        widget=forms.CheckboxSelectMultiple
    )
    company_videos_photos = forms.FileField(required=False)
    top_clients = forms.FileField(required=False)
    awards_recognition = forms.FileField(required=False)

    class Meta:
        model = Seller
        fields = [
            'registered_name', 'gst_number', 'registered_address',
            'owner_poc_name', 
            # 'contact_number',
            # 'email_id',
            # 'company_name',
            'services_type', 'company_videos_photos',
            'top_clients', 'awards_recognition'
        ]
