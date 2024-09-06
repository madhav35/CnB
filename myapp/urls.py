"""
URL configuration for myproject_pnm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]


# myapp/urls.py

# myapp/urls.py

# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('request_quotes/<int:product_id>/', views.request_quotes, name='request_quotes'),
    path('view_quotes/<int:product_id>/', views.view_quotes, name='view_quotes'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('support/', views.support, name='support'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new_request/', views.create_new_request, name='create_new_request'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('provide_quote/<int:product_id>/', views.provide_quote, name='provide_quote'),
    path('select_quotes/<int:product_id>/', views.select_quotes, name='select_quotes'),
    path('seller_details/<int:seller_id>/', views.seller_details, name='seller_details'),
    path('interest_details/<int:product_id>/<int:bid_id>/', views.interest_details, name='interest_details'),
    path('quote_details/<int:product_id>/<int:bid_id>/', views.quote_details, name='quote_details'),
    path('quote_details/<int:product_id>/', views.quote_details, name='quote_details'),
    path('quote_details/<int:product_id>/<int:bid_id>/', views.quote_details, name='quote_details_with_bid'),
    path('provide_quote/<int:product_id>/', views.provide_quote, name='provide_quote'),

]