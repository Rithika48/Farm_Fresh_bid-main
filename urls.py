from django.contrib import admin
from django.urls import path, include  # Import include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', include('bid_app.urls')),  # Include URLs from bid_app
]