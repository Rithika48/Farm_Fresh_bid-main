from django import template
from bid_app.models import *
import datetime
register = template.Library()
from pytz import timezone
from dateutil import tz
tzzone = tz.gettz('Asia/Kolkata') 

@register.filter(name="change_dict")
def change_dict(obj):
    return eval(obj).items()

# @register.simple_tag
# def getquantity(obj, bookid, pid):
#     print(obj)
#     book = Booking.objects.get(id=bookid)
#     proid = (book.booking_id).split('.')[1:]
#     myindex = proid.index(str(pid))
#     li = (book.quantity).split(',')
#     print(li)
#     return li[myindex]

@register.simple_tag
def getupcoming(start, end):
    # Fetch the product using the provided start ID
    prod = Product.objects.get(id=start)
    # Print the start session date for debugging
    print(prod.start_session_date)  # Use the correct attribute
    # If you need to return the start session date
    return prod.start_session_date

@register.simple_tag
def getendtime(start, end):
    asia = timezone('Asia/Kolkata')
    return end

@register.simple_tag
def checkparticipant(pid):
    return pid

@register.simple_tag
def checkUserParticipate(user, product):
    participate = Participants.objects.filter(user=user, product=product)
    if participate:
        return True
    return False

@register.simple_tag
def checkUserParticipate(user, product):
    # Your logic to check if the user is a participant
    return True  # or False based on your logic