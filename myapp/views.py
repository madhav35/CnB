from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer, Seller, Product, Bid, Deal, Profile, Image
from .forms import CustomUserCreationForm, BuyerRegistrationForm, SellerRegistrationForm
from django.http import HttpResponse
from django.template.loader import render_to_string 
from django.db.models import Min, Q
from datetime import datetime, timedelta

def home(request):
    if request.user.is_authenticated:
        return redirect('about_us')  # Redirect to the dashboard if logged in
    return render(request, 'myapp/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'buyer'):
                return redirect('buyer_dashboard')
            elif hasattr(user, 'seller'):
                return redirect('seller_dashboard')
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'myapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        user_type = request.POST.get('user_type')

        if user_type == 'seller':
            profile_form = SellerRegistrationForm(request.POST, request.FILES)
        else:
            profile_form = BuyerRegistrationForm(request.POST)

        # Ensure both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.email = user_form.cleaned_data.get('email')
            user.save()

            # Create Profile
            profile = Profile.objects.create(user=user, mobile_number=request.POST.get('mobile_number'))

            # Handle buyer or seller logic
            if user_type == 'buyer':
                Buyer.objects.create(user=user, profile=profile)
            elif user_type == 'seller':
                Seller.objects.create(
                    user=user,
                    profile=profile,
                    registered_name=profile_form.cleaned_data.get('registered_name'),
                    gst_number=profile_form.cleaned_data.get('gst_number'),
                    registered_address=profile_form.cleaned_data.get('registered_address'),
                    poc_name=profile_form.cleaned_data.get('owner_poc_name'),
                    services_type=','.join(profile_form.cleaned_data.get('services_type')),
                    company_media=profile_form.cleaned_data.get('company_videos_photos'),
                    top_clients=profile_form.cleaned_data.get('top_clients'),
                    awards=profile_form.cleaned_data.get('awards_recognition'),
                )

            # Log the user in and redirect to the dashboard
            login(request, user)
            return redirect('dashboard')
        else:
            # Pass errors to the template for both user_form and profile_form
            return render(request, 'myapp/register.html', {
                'form': user_form,
                'buyer_form': BuyerRegistrationForm(),
                'seller_form': SellerRegistrationForm(),
                'user_form_errors': user_form.errors,
                'profile_form_errors': profile_form.errors,
            })
    else:
        user_form = CustomUserCreationForm()
        profile_form = BuyerRegistrationForm()  # Default to buyer registration form

    return render(request, 'myapp/register.html', {
        'form': user_form,
        'buyer_form': BuyerRegistrationForm(),
        'seller_form': SellerRegistrationForm()
    })



# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.email = request.POST['email']
#             user.save()

#             mobile_number = request.POST['mobile_number']
#             company_name = request.POST.get('company_name', '')
#             user_type = request.POST['user_type']

#             # Create Profile
#             profile = Profile.objects.create(user=user, mobile_number=mobile_number)

#             # Create the appropriate profile based on the user_type
#             if user_type == 'buyer':
#                 Buyer.objects.create(user=user, profile=profile, company_name=company_name)
#             elif user_type == 'seller':
#                 Seller.objects.create(user=user, profile=profile, company_name=company_name)

#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UserCreationForm()
#     return render(request, 'myapp/register.html', {'form': form})

def support(request):
    return render(request, 'myapp/support.html')

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'myapp/profile.html', {'profile': profile})


# def buyer_dashboard(request):
#     if not hasattr(request.user, 'buyer'):
#         return redirect('login')
#     # Logic for buyer dashboard
#     return render(request, 'myapp/buyer_dashboard.html')

def buyer_dashboard(request):
    if not hasattr(request.user, 'buyer'):
        return redirect('login')
    
    # Get all products associated with the logged-in user (assuming the user is a Buyer)
    products = Product.objects.filter(buyer=request.user)

    context = {
        'products': products
    }
    return render(request, 'myapp/buyer_dashboard.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, buyer=request.user)

    if request.method == 'POST':
        product.from_city = request.POST.get('from_city')
        product.to_city = request.POST.get('to_city')
        product.item_details = request.POST.get('item_details')
        product.shifting_plan = request.POST.get('shifting_plan')
        product.call_preference = request.POST.get('call_preference') == 'on'
        product.call_time = request.POST.get('call_time') if request.POST.get('call_preference') == 'on' else None
        product.budget_min = request.POST.get('budget_min')
        product.budget_max = request.POST.get('budget_max')
        product.specific_requirements = request.POST.get('specific_requirements')
        product.save()

        return redirect('buyer_dashboard')

    return render(request, 'myapp/edit_product.html', {'product': product})


def view_quotes(request, product_id):
    product = get_object_or_404(Product, id=product_id, buyer=request.user)
    bids = Bid.objects.filter(product=product)

    if request.method == "POST":
        selected_bids_ids = request.POST.getlist('selected_bids')
        for bid in bids:
            bid.selected = str(bid.id) in selected_bids_ids
            bid.save()

    context = {
        'product': product,
        'bids': bids,
    }
    return render(request, 'myapp/view_quotes.html', context)

def select_quotes(request, product_id):
    if request.method == 'POST':
        selected_bids = request.POST.getlist('selected_bids')
        # Process the selected bids, for example, save them to the database
        # or mark them as selected.

        # Assuming you want to update the selected bids as chosen by the buyer
        for bid_id in selected_bids:
            bid = Bid.objects.get(id=bid_id)
            # Perform any operation you need with the selected bid
            # For example, mark as 'selected' in your database or send notifications
            # bid.selected = True
            # bid.save()

        # Redirect to the dashboard or a confirmation page
        return redirect('buyer_dashboard')

    return redirect('view_quotes', product_id=product_id)

def seller_details(request, seller_id):
    seller = Seller.objects.get(id=seller_id)
    html = render_to_string('myapp/seller_details.html', {'seller': seller})
    return HttpResponse(html)



def request_quotes(request, product_id):
    product = get_object_or_404(Product, id=product_id, buyer=request.user)

    # Mark the product as having requested quotes
    product.is_quote_requested = True
    product.save()

    return redirect('buyer_dashboard')

from django.db.models import Min, Q


from datetime import datetime, timedelta
from django.shortcuts import render, redirect

def seller_dashboard(request):
    if not hasattr(request.user, 'seller'):
        return redirect('login')

    # Get filter values from request.GET
    status_filter = request.GET.get('status')
    date_range_filter = request.GET.get('date_range')
    quote_filter = request.GET.get('quote_status')
    time_to_shift_filter = request.GET.get('time_to_shift')

    # Get all products where quotes have been requested
    products = Product.objects.filter(is_quote_requested=True)

    # Apply date range filter if applicable
    if date_range_filter:
        if date_range_filter == 'last_24_hours':
            start_date = datetime.now() - timedelta(hours=24)
            products = products.filter(created_at__gte=start_date)
        elif date_range_filter == 'last_7_days':
            start_date = datetime.now() - timedelta(days=7)
            products = products.filter(created_at__gte=start_date)
        elif date_range_filter == 'last_15_days':
            start_date = datetime.now() - timedelta(days=15)
            products = products.filter(created_at__gte=start_date)
        elif date_range_filter == 'last_30_days':
            start_date = datetime.now() - timedelta(days=30)
            products = products.filter(created_at__gte=start_date)
        elif ' - ' in date_range_filter:
            try:
                start_date_str, end_date_str = date_range_filter.split(' - ')
                start_date = datetime.strptime(start_date_str.strip(), '%d/%m/%Y')
                end_date = datetime.strptime(end_date_str.strip(), '%d/%m/%Y')
                products = products.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
            except ValueError:
                pass  # Ignore invalid date formats

    # Apply time to shift filter if provided
    if time_to_shift_filter and time_to_shift_filter != 'all':
        products = products.filter(shifting_plan=time_to_shift_filter)

    # Now, gather products with their status information
    products_with_status = []

    for product in products:
        bids = Bid.objects.filter(product=product)
        seller_bid = bids.filter(seller=request.user.seller).first()
        lowest_bid = bids.aggregate(Min('bid_amount'))['bid_amount__min']
        buyer_interested_bid = bids.filter(selected=True).first()  # Buyer interest

        # Determine the button status
        if bids.exists():  # If any bids exist
            if seller_bid and buyer_interested_bid and buyer_interested_bid.seller == request.user.seller:
                # Buyer interested in the current seller's quote
                button_status = 'green'
            elif seller_bid and buyer_interested_bid and buyer_interested_bid.seller != request.user.seller:
                # Buyer interested in another seller's quote
                button_status = 'light-red'
            else:
                # Bidding in progress, but no interest from buyer yet
                button_status = 'amber'
        else:
            # No one has quoted
            button_status = 'light-green'

        # Apply status filter if provided
        if status_filter and status_filter != 'all':
            if status_filter == 'no_one_quoted' and button_status != 'light-green':
                continue
            if status_filter == 'bidding_in_progress' and button_status != 'amber':
                continue
            if status_filter == 'interested_in_your_quote' and button_status != 'green':
                continue
            if status_filter == 'interested_in_another_quote' and button_status != 'light-red':
                continue

        # Apply quote filter if provided
        if quote_filter and quote_filter != 'all':
            if quote_filter == 'quoted' and not seller_bid:
                continue
            if quote_filter == 'not_quoted' and seller_bid:
                continue

        # Append product details along with its status
        products_with_status.append({
            'product': product,
            'seller_bid_id': seller_bid.id if seller_bid else None,
            'lowest_bid': lowest_bid,
            'button_status': button_status,
            'has_provided_quote': seller_bid is not None
        })

    context = {
        'products_with_status': products_with_status
    }
    return render(request, 'myapp/seller_dashboard.html', context)



def interest_details(request, product_id, bid_id):
    product = get_object_or_404(Product, id=product_id)
    seller_bid = get_object_or_404(Bid, id=bid_id)

    # Fetch the lowest bid for the product excluding the seller's bid
    other_bids = Bid.objects.filter(product=product).exclude(id=seller_bid.id).order_by('bid_amount')

    context = {
        'seller_bid': seller_bid,
        'other_bids': other_bids,
    }

    return render(request, 'myapp/interest_details.html', context)
# views.py

def provide_quote(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = request.user.seller

    if request.method == 'POST':
        # Get quote details from the form
        bid_amount = request.POST.get('bid_amount')
        attachment = request.FILES.get('attachment')

        # Ensure bid_amount is provided before creating/updating the bid
        if bid_amount:
            # Check if a bid already exists for this product and seller
            try:
                bid = Bid.objects.get(product=product, seller=seller)
                bid.bid_amount = bid_amount  # Update existing bid amount
                if attachment:
                    bid.attachment = attachment  # Update attachment if provided
                bid.save()
            except Bid.DoesNotExist:
                # Create a new bid since one doesn't exist yet
                bid = Bid.objects.create(
                    product=product,
                    seller=seller,
                    bid_amount=bid_amount,
                    attachment=attachment
                )

            # Redirect to seller dashboard with a success message
            return redirect('seller_dashboard')

    # If not a POST request, redirect back to seller dashboard
    return redirect('seller_dashboard')


def quote_details(request, product_id, bid_id=None):
    product = get_object_or_404(Product, id=product_id)
    seller_bid = None

    if bid_id:
        seller_bid = get_object_or_404(Bid, id=bid_id, seller=request.user.seller)

    other_bids = Bid.objects.filter(product=product).exclude(seller=request.user.seller).order_by('bid_amount')

    context = {
        'product': product,
        'seller_bid': seller_bid,
        'other_bids': other_bids,
    }

    return render(request, 'myapp/quote_details.html', context)


def about_us(request):
    return render(request, 'myapp/about_us.html')

def contact_us(request):
    return render(request, 'myapp/contact_us.html')

def dashboard(request):
    if hasattr(request.user, 'buyer'):
        return redirect('buyer_dashboard')
    elif hasattr(request.user, 'seller'):
        return redirect('seller_dashboard')
    else:
        return redirect('login')
    

# def create_new_request(product):
#     if product.method == 'POST':
#         from_city = product.POST.get('from_city')
#         to_city = product.POST.get('to_city')
#         shifting_plan = product.POST.get('shifting_plan')
#         item_details = product.POST.get('item_details')
#         call_preference = product.POST.get('call_preference')
#         call_time = product.POST.get('call_time') if call_preference else None
#         budget_min = product.POST.get('budget_min')
#         budget_max = product.POST.get('budget_max')
#         specific_requirements = product.POST.get('specific_requirements')
#         images = product.FILES.getlist('images')

#         # Save the request in the database (assuming a model Request)
#         new_request = Product.objects.create(
#             from_city=from_city,
#             to_city=to_city,
#             shifting_plan=shifting_plan,
#             item_details=item_details,
#             call_preference=bool(call_preference),
#             call_time=call_time,
#             budget_min=budget_min,
#             budget_max=budget_max,
#             specific_requirements=specific_requirements
#         )

#         # Save the uploaded images
#         for image in images:
#             # Assuming you have an Image model to handle images related to the request
#             Image.objects.create(product=new_request, image=image)

#         return redirect('buyer_dashboard')  # Redirect to buyer's dashboard after submission

#     return render(product, 'myapp/new_request.html')

# myapp/views.py

# from django.shortcuts import render, redirect
# from .models import Product  # Import the Product model

def create_new_request(request):
    if request.method == 'POST':
        from_city = request.POST.get('from_city')
        to_city = request.POST.get('to_city')
        shifting_plan = request.POST.get('shifting_plan')
        item_details = request.POST.get('item_details')
        call_preference = request.POST.get('call_preference') == 'on'
        call_time = request.POST.get('call_time') if call_preference else None
        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')
        specific_requirements = request.POST.get('specific_requirements')

        # Save the request in the database
        new_request = Product.objects.create(
            buyer=request.user,  # Assuming the logged-in user is the buyer
            from_city=from_city,
            to_city=to_city,
            shifting_plan=shifting_plan,
            item_details=item_details,
            call_preference=call_preference,
            call_time=call_time,
            budget_min=budget_min,
            budget_max=budget_max,
            specific_requirements=specific_requirements
        )

        # Handle uploaded images if any
        images = request.FILES.getlist('images')
        for image in images:
            # Assuming you have a model to handle images
            Image.objects.create(product=new_request, image=image)

        return redirect('buyer_dashboard')  # Redirect to buyer's dashboard after submission

    return render(request, 'myapp/new_request.html')

# views.py

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'myapp/product_details.html', {'product': product})



def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'myapp/profile.html', {'profile': profile})