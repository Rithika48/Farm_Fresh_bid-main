from django.urls import path
from . import views  # Import all views
from django.urls import get_resolver

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('about/', views.about, name='about'),  # About page URL
    path('admin/', views.admin_login, name='admin_login'),  # Admin login URL
    path('login/', views.login_user, name='login'),  # User login URL
    path('signup/', views.signup_view, name='signup'),  # User signup URL
    path('add_product/', views.add_product, name='add_product'),  # Add product URL
    path('view_product/', views.view_product, name='view_product'),  # View products URL
    path('edit_product/<int:pid>/', views.edit_product, name='edit_product'),  # Edit product URL
    path('delete_product/<int:pid>/', views.delete_product, name='delete_product'),  # Delete product URL
    path('product_detail/<int:pid>/', views.product_detail, name='product_detail'),  # Product detail URL
    path('dropdowns/', views.show_dropdowns, name='show_dropdowns'),  # New URL for dropdowns
]


# Optional: Print the current URL patterns for debugging

print(get_resolver().url_patterns)