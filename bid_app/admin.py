from django.contrib import admin
from .models import *

# Custom admin class for Product
class ProductAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin interface
    list_display = ('name', 'base_price', 'start_session_date', 'end_session_date', 'status')  # Add other fields as necessary
    # Exclude final_price and interval_price
    exclude = ('final_price', 'interval_price')

# Register your models here.
admin.site.register(AuctionUser )
admin.site.register(Member_fee)
admin.site.register(Product, ProductAdmin)  # Use the custom admin class
admin.site.register(Participants)
admin.site.register(ParticipantsHistory)
admin.site.register(Send_Feedback)
admin.site.register(Category)
# admin.site.register(Sub_Category)