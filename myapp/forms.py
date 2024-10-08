from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer, Seller

class CustomUserCreationForm(UserCreationForm):
    mobile_number = forms.CharField(required=True,
                                     max_length=10, 
                                    #  help_text="Enter a valid 10-digit mobile number",
                                     widget=forms.TextInput(attrs={'style': 'width: 32%; margin-left: 10.5%;',}
                                                            )
                                    )
    username = forms.CharField(label="Username (Use Mobile No.)")
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'style': 'width: 186px; margin-left: 100px;',}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'style': 'width: 32%; margin-left: 12%;',}),
        }

class BuyerRegistrationForm(forms.ModelForm):
    # mobile_number = forms.CharField(required=True, max_length=10)
    class Meta:
        model = Buyer
        fields = []  # No additional fields needed for buyer

class SellerRegistrationForm(forms.ModelForm):
    registered_name = forms.CharField(required=True,
                                      widget=forms.TextInput(attrs={'style': 'width: 32%; margin-left: 7.75%; margin-right: 0%;',}
                                                            ))
    gst_number = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'style': 'width: 32%; margin-left: 14.8%; margin-right: 0%;',}
                                                            ))
    registered_address = forms.CharField(required=True,
                                         widget=forms.TextInput(attrs={'style': 'width: 32%; margin-left: 4%; margin-right: 0%;',}
                                                            ))
    owner_poc_name = forms.CharField(required=True,
                                     widget=forms.TextInput(attrs={'style': 'width: 32%; margin-left: 7.6%; margin-right: 0%;',}
                                                            ))
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
            ('specialized_boxes_electronics', 'Specialized Boxes for Electronics'),
            ('specialized_boxes_vehicle', 'Vehicle Relocation'),
            ('specialized_boxes_pet', 'Pet Relocation'),
            ('specialized_boxes_plant', 'Plant Relocation Expert')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'margin-top: 0%;',})
    )
    company_videos_photos = forms.FileField(required=False,
                                            widget=forms.FileInput(attrs={'style': 'width: 100%; margin-left: 32%; display: inline-block; margin-right: 0%;',}))
    top_clients = forms.FileField(required=False,
                                  widget=forms.FileInput(attrs={'style': 'width: 100%; margin-left: 32%;',}))
    awards_recognition = forms.FileField(required=False,
                                         widget=forms.FileInput(attrs={'style': 'width: 100%; margin-left: 32%;',}))

    # New fields
    company_size = forms.ChoiceField(
        choices=[
            ('<10', '<10 employees'), 
            ('10-20', '10-20 employees'), 
            ('20-50', '20-50 employees'),
            ('50-100', '50-100 employees'),
            ('100-500', '100-500 employees'), 
            ('>500', '>500 employees')
        ],
        required=True,
        widget=forms.Select(attrs={ 'style': 'margin-left: 32%;',})
    )
    truck_ownership = forms.ChoiceField(
        choices=[('Own', 'Own trucks'), ('Aggregator', 'Aggregator (we do not own trucks)')], 
        required=True,
        widget=forms.Select(attrs={ 'style': 'margin-left: 32%;',})
    )
    call_support = forms.ChoiceField(
        choices=[(True, 'Yes'), (False, 'No')], 
        required=True,
        widget=forms.RadioSelect  # Display Yes/No as radio buttons
    )
    running_business_since = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={})
    )

    class Meta:
        model = Seller
        fields = [
            'registered_name', 'gst_number', 'registered_address',
            'owner_poc_name', 
            # 'contact_number',
            # 'email_id',
            # 'company_name',
            'services_type', 'company_videos_photos',
            'top_clients', 'awards_recognition', 'company_size', 'truck_ownership','call_support','running_business_since'
        ]
