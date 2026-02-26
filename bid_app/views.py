from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from .models import AuctionUser , Member_fee, Product, Category, Participants, ParticipantsHistory #,Bid # Ensure these models exist
import random
import math
from django.conf import settings
from django.http import JsonResponse

# Home view
def home(request):
    if request.user.is_authenticated:
        try:
            auctionuser = AuctionUser .objects.get(user=request.user)
            if auctionuser.status == "pending":
                messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
                return redirect('profile', request.user.id)
        except AuctionUser .DoesNotExist:
            messages.error(request, "You need to register as an Auction User to access this feature.")
            return redirect('signup')

    upcoming_product = Product.objects.filter(status="upcoming")
    closed_product = Product.objects.filter(status="closed")
    live_product = Product.objects.filter(status="live")
    context = {
        'upcoming_product': upcoming_product,
        'closed_product': closed_product,
        'live_product': live_product
    }
    return render(request, 'home.html', context)

# About view
def about(request):
    return render(request, 'about.html')

# Contact view
def contact(request):
    return render(request, 'contact.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        # Extract data from the form
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pwd']
        contact = request.POST['contact']
        dob = request.POST['dob']
        address = request.POST['add']
        user_type = request.POST.get('reg')

        print(f"Received signup data: {fname}, {lname}, {username}, {email}, {user_type}")  # Debugging line

        if user_type is None:
            messages.error(request, "Please select a user type (Bidder or Seller).")
            return render(request, 'signup.html')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'signup.html')

        # Handle file upload
        image = request.FILES.get('image')

        try:
            # Create the user
            user = User .objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname)
            print(f"User  created: {user}")  # Debugging line

            # Create an instance of AuctionUser   
            mem = Member_fee.objects.filter(fee="Unpaid").first() # Ensure this membership exists
            auction_user = AuctionUser .objects.create(
                membership=mem,
                user=user,
                contact=contact,
                address=address,
                dob=dob,
                image=image,
                user_type=user_type
            )
            print(f"AuctionUser  created: {auction_user}")  # Debugging line
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            print(f"Error during signup: {e}")  # Debugging line

    return render(request, 'signup.html')  # Render the signup page if GET request

# Logout view
def logout_user(request):
    logout(request)
    return redirect('home')

# Login view
def login_user(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user and not user.is_staff:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

# Add Product view
def add_product(request):
    if not request.user.is_authenticated:
        return redirect('login')

    categories = Category.objects.all()  # Fetch all categories for the dropdown
    auctionuser = AuctionUser .objects.get(user=request.user)
    
    if auctionuser.status == "pending":
        messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
        return redirect('profile', request.user.id)

    if request.method == "POST":
        # Extract data from the form
        category_id = request.POST['category']  # Get the selected category
        auction_type = request.POST['auction_type']  # Auction type (Auction or Tender)
        start_session_date = request.POST['start_session_date']  # Start date for the auction
        end_session_date = request.POST['end_session_date']  # End date for the auction
        product_name = request.POST['product_name']
        base_price = request.POST['base_price']  # Base price of the product
        quantity = request.POST['quantity']  # Quantity in Kg
        description = request.POST['description']  # Product description
        image = request.FILES.get('image')

        # Convert to timezone-aware datetime objects using fromisoformat
        start_session_date = timezone.make_aware(datetime.fromisoformat(start_session_date))
        end_session_date = timezone.make_aware(datetime.fromisoformat(end_session_date))

        # Validate that the end session date is after the start session date
        if end_session_date <= start_session_date:
            messages.error(request, "End session date must be after the start session date.")
            return render(request, 'add_product.html', {'categories': categories})

        # Determine the initial status based on the current time
        if timezone.now() < start_session_date:
            status = "upcoming"
        elif timezone.now() < end_session_date:
            status = "live"
        else:
            status = "closed"

        # Create the product
        Product.objects.create(
            name=product_name,
            category_id=category_id,  # Ensure this matches your model
            bid_type=auction_type,  # Ensure this matches your model
            start_session_date=start_session_date,  # Start date for the auction
            end_session_date=end_session_date,  # End date for the auction
            base_price=base_price,  # Save the base price
            quantity=quantity,  # Save the quantity
            images=image,
            user=request.user,
            status=status,  # Set the initial status based on the current time
            description=description,  # Save the description
            comment="",  # Initialize comment as empty
        )
        messages.success(request, "Product added successfully.")
        return redirect('view_product')

    return render(request, 'add_product.html', {'categories': categories})  # Pass categories to the template

def edit_product(request, pid):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # Attempt to get the AuctionUser  associated with the logged-in user
        auctionuser = AuctionUser .objects.get(user=request.user)
        
        # Check if the user's status is pending
        if auctionuser.status == "pending":
            messages.warning(request, "Your verification is pending. Please complete your additional details and email verification. If these are already completed, try logging in after some time. We are working on your detail verification. Thanks!")
            return redirect('profile', request.user.id)

        # Attempt to get the product to edit
        product = Product.objects.get(id=pid, user=request.user)  # Ensure the product belongs to the user
        categories = Category.objects.all()  # Fetch all categories for the dropdown
        
        if request.method == "POST":
            # Extract data from the form
            product.name = request.POST['p_name']
            product.base_price = request.POST['price']
            product.quantity = request.POST['quantity']  # Update quantity
            product.description = request.POST['desc']
            product.bid_type = request.POST['bid_type']
            product.category_id = request.POST['cat']  # Directly using category ID
            
            # Handle file upload for the image
            if 'image' in request.FILES:
                product.images = request.FILES['image']
            
            # Update the product
            product.save()
            messages.success(request, "Product updated successfully.")
            return redirect('view_product')

    except AuctionUser .DoesNotExist:
        messages.error(request, "User  profile not found. Please register as an Auction User.")
        return redirect('signup')  # Redirect to signup or another appropriate page
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('view_product')  # Redirect to the view product page

    # Render the edit product page with the product data and categories
    return render(request, 'edit_product.html', {'cat': categories, 'data': product})


def view_product(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        auctionuser = AuctionUser .objects.get(user=request.user)  # Attempt to get the AuctionUser 
        if auctionuser.status == "pending":
            messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
            return redirect('profile', request.user.id)

        products = Product.objects.filter(user=request.user)  # Retrieve products for the authenticated user
        return render(request, 'view_product.html', {'product': products})  # Pass products to the template

    except AuctionUser .DoesNotExist:
        messages.error(request, "User  profile not found. Please register as an Auction User.")
        return redirect('signup')  # Redirect to signup or another appropriate page

# Delete Product
def delete_product(request, pid):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        # Attempt to get the product, ensuring it belongs to the authenticated user
        product = Product.objects.get(id=pid, user=request.user)  # Ensure the product belongs to the user
        product.delete()  # Delete the product if it exists
        messages.success(request, "Product deleted successfully.")  # Success message
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")  # Error message if product does not exist
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")  # General error handling

    return redirect('view_product')  # Redirect to the view product page
# Product Detail
def product_detail(request, pid):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # Attempt to get the AuctionUser  associated with the logged-in user
        auctionuser = AuctionUser .objects.get(user=request.user)
        
        # Check if the user's status is pending
        if auctionuser.status == "pending":
            messages.warning(request, "Your verification is pending. Please complete your additional details and email verification. If these are already completed, try logging in after some time. We are working on your detail verification. Thanks!")
            return redirect('profile', request.user.id)

        # Attempt to get the product details
        product = Product.objects.get(id=pid)  # You may want to check if the product belongs to the user

        # Render the product detail page with the product data
        return render(request, 'product_detail.html', {'product': product})

    except AuctionUser .DoesNotExist:
        messages.error(request, "User  profile not found. Please register as an Auction User.")
        return redirect('signup')  # Redirect to signup or another appropriate page
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")  # Error message if product does not exist
        return redirect('view_product')  # Redirect to the view product page
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")  # General error handling
        return redirect('view_product')  # Redirect to the view product page
# Make Participants
def make_participants(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    auctionuser = AuctionUser  .objects.get(user=request.user)
    if auctionuser.status == "pending":
        messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
        return redirect('profile', request.user.id)

    product = Product.objects.get(id=pid)
    participant = Participants.objects.create(user=request.user, product=product)
    messages.success(request, "Added for participant successfully.")
    return redirect('product_detail', pid)

# Get Bid History
def getbidhistory(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=pid)
    participant = ParticipantsHistory.objects.filter(product=product).order_by('-id')[:5]
    winner_status = False
    if product.bid_type == "Tendor":
        max_val = product.min_price - product.interval_price
    else:
        max_val = product.min_price + product.interval_price

    if participant.first():
        minutes = datetime.now(timezone.utc) - participant.first().created
        
        if minutes.seconds / 60 >= 3 and product.status == "live":
            product.winner = participant.first().user
            product.status = "closed"
            winner_status = True

        if product.bid_type == "Tendor":
            max_val = participant.first().new_price - product.interval_price
        else:
            max_val = participant.first().new_price + product.interval_price

    d = {'status': 'Success', 'new_price': [], 'name': [], 'time': [], 'maximum': max_val, 'winner_status': winner_status}
    try:
        product.final_price = participant.first().new_price
        product.save()
    except:
        pass

    for i in participant:
        d['new_price'].append(i.new_price)
        d['name'].append(i.user.first_name + " " + i.user.last_name)
        d['time'].append(i.created)
    return JsonResponse(d)

# Start Bidding
def startbidding(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=pid)

    # Check if the product is live
    if product.status != "live":
        messages.error(request, "Bidding is not currently open for this product.")
        return redirect('product_detail', pid)

    # Get the new bid price from the request
    new = request.POST.get('new_price')

    # Check if the new price is valid (you may want to add more validation here)
    if not new or float(new) <= 0:
        messages.error(request, "Invalid bid price.")
        return redirect('product_detail', pid)

    # Fetch the last participant
    participant1 = ParticipantsHistory.objects.filter(product=product).order_by('-id')[:5]

    # Check if there are any previous bids
    if participant1.first():
        minutes = (timezone.now() - participant1.first().created).total_seconds() / 60
        if minutes >= 3:
            # If 3 minutes have passed since the last bid, declare the winner
            product.winner = participant1.first().user
            product.status = "closed"
            product.save()
            messages.success(request, "Sorry! You are late, Winner has announced.")
            return redirect('product_detail', pid)
        else:
            # If still within the bidding time, create a new participant record
            participant = ParticipantsHistory.objects.create(user=request.user, product=product, new_price=new)
            messages.success(request, "Your bid has been placed successfully.")
    else:
        # If no previous bids, create the first participant record
        participant = ParticipantsHistory.objects.create(user=request.user, product=product, new_price=new)
        messages.success(request, "Your bid has been placed successfully.")

    return redirect('product_detail', pid)


# Change Live to Complete
def changelivetocomplete(request, pid):
    product = Product.objects.get(id=pid)
    winner = ParticipantsHistory.objects.filter(product=product).last()
    product.status = "closed"
    if winner:
        product.winner = winner.user
    product.save()
    return JsonResponse({'myurl': '/'})

# Change Upcoming to Live
def changeupcomingtolive(request, pid):
    product = Product.objects.get(id=pid)
    product.status = "live"
    product.save()
    return JsonResponse({'myurl': '/'})

# Meet Winners
def meetwinners(request):
    if request.user.is_authenticated:
        auctionuser = AuctionUser .objects.get(user=request.user)
        if auctionuser.status == "pending":
            messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
            return redirect('profile', request.user.id)
    product = Product.objects.filter().exclude(winner=None)
    return render(request, 'meetwinners.html', {'product': product})

# All Products
def all_product(request):
    if request.user.is_authenticated:
        auctionuser = AuctionUser .objects.get(user=request.user)
        if auctionuser.status == "pending":
            messages.success(request, "Your verification is pending. Complete your additional detail and email verification. If these are already completed then try login after sometime. We are working on your detail verification. Thanks!")
            return redirect('profile', request.user.id)
    product = Product.objects.filter().exclude(status="pending")
    return render(request, 'HotProducts.html', {'product': product})

# Admin Home
def admin_home(request):
    bidder = AuctionUser .objects.filter(user_type="Bidder")
    seller = AuctionUser .objects.filter(user_type="Seller")
    tender = Product.objects.filter(bid_type="Tendor")
    auction = Product.objects.filter(bid_type="Auction")
    d = {'bidder': bidder.count(), 'seller': seller.count(), 'tender': tender.count(), 'auction': auction.count()}
    return render(request, 'administration/admin_home.html', d)

# Admin Login
def admin_login(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid Credentials.")
    return render(request, 'administration/loginadmin.html')

# View Seller Users
def view_seller_user(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = AuctionUser .objects.filter(user_type='Seller')
    for seller in pro:
        # Ensure the image field is checked before accessing its URL
        if not seller.image:
            seller.image_url = None  # or set a default image URL
        else:
            seller.image_url = seller.image.url
    d = {'user': pro}
    return render(request, 'administration/view_seller_user.html', d)

# View Buyer Users
def view_buyer_user(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = AuctionUser .objects.filter(user_type='Bidder')
    d = {'user': pro}
    return render(request, 'administration/view_user.html', d)

# View Participants
def view_participants(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = Participants.objects.filter()
    d = {'pro': pro}
    return render(request, 'administration/view_participants.html', d)

# Admin Product View
def admin_product(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    product = Product.objects.filter()
    d = {'pro': product}
    return render(request, 'administration/admin_view_product.html', d)

# Add Category
def add_category(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    if request.method == "POST":
        n = request.POST['cat']
        Category.objects.create(name=n)
        messages.success(request, "Added Successfully")
    return render(request, 'administration/add_category.html')

# View Category
def view_category(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = Category.objects.all()
    return render(request, 'administration/view_category.html', {'pro': pro})

# View Winners
def view_winner(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = Product.objects.filter().exclude(winner=None)
    return render(request, 'administration/view_winner.html', {'pro': pro})

# Delete Admin Product
def delete_admin_product(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    pro = Product.objects.get(id=pid)
    pro.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('admin_view_product')

# Delete Category
def delete_category(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    cat = Category.objects.get(id=pid)
    cat.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('view_category')

# Delete User
def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('view_buyer_user')

# Delete Participant
def delete_participant(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    participant = Participants.objects.get(id=pid)
    participant.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('view_participants')

# Change Product Status
def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    product = Product.objects.get(id=pid)
    product.status = "upcoming"
    product.save()
    messages.success(request, "Status Changed Successfully")
    return redirect('admin_view_product')

# Change User Status
def change_user_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    user = AuctionUser .objects.get(id=pid)
    user.status = "pending" if user.status == "Approved" else "Approved"
    user.save()
    messages.success(request, "Status Changed Successfully")
    return redirect('view_seller_user' if user.user_type == "Seller" else 'view_buyer_user')

# Change Password
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        new_password = request.POST['pwd1']
        confirm_password = request.POST['pwd2']
        old_password = request.POST['pwd3']
        if confirm_password == new_password:
            user = User.objects.get(username=request.user.username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Changed Successfully")
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'change_password.html')

# User Profile


def profile(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=pid)
    auction_user = AuctionUser .objects.get(user=user)
    
    # Check if the image exists before rendering
    image_url = auction_user.image.url if auction_user.image else None

    return render(request, 'profile.html', {
        'pro': auction_user,
        'user': user,
        'image_url': image_url  # Pass the image URL to the template
    })

# Edit Profile


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    auction_user = AuctionUser .objects.get(user=request.user)
    
    if request.method == 'POST':
        # Extracting data from the form
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        contact = request.POST['contact']
        dob = request.POST['date']
        address = request.POST['add']

        try:
            # Handle file uploads
            if 'img' in request.FILES:
                auction_user.image = request.FILES['img']
            
            # Update other fields
            auction_user.dob = dob
            auction_user.user.username = username
            auction_user.user.first_name = fname
            auction_user.user.last_name = lname
            auction_user.user.email = email
            auction_user.contact = contact
            auction_user.address = address
            
            # Save the changes
            auction_user.save()
            auction_user.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', request.user.id)
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'edit_profile.html', {'pro': auction_user})

# Email Verification
def email_verify(request, pid):
    user = AuctionUser  .objects.get(id=pid)
    if request.method == "POST":
        otp = request.POST['otp']
        if user.otp == str(otp):
            user.email_verification = True
            user.save()
            messages.success(request, "Email Verified Successfully")
            return redirect('profile', user.user.id)
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('email_verify', pid)
    return render(request, 'verify_email.html', {'pid': pid})

# Generate OTP
def generateotp(request, pid):
    user = AuctionUser  .objects.get(id=pid)
    digits = [i for i in range(0, 10)]

    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    email_host = settings.EMAIL_HOST_USER
    html_content = "<h4>Your Email Verification code is : </h4><h3>" + str(random_str) + "</h3>"
    email = EmailMessage("Send Verification Code", html_content, str(email_host), [str(user.user.email),])
    email.content_subtype = "html"
    email.send()
    user.otp = random_str
    user.save()
    return JsonResponse({'Success': True})

# Admin Product Detail
def admin_product_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login admin')
    product = Product.objects.get(id=pid)
    if request.method == "POST":
        comment = request.POST['comment']
        product.comment = comment
        product.save()
        messages.success(request, "Commented Successfully")
        return redirect('admin_product_detail', pid)
    return render(request, 'administration/admin_product_detail.html', {'product': product, 'booking_id': pid})

# Bidder Detail
def bidder_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data = AuctionUser  .objects.get(id=pid)
    return render(request, 'administration/bidder_detail.html', {'data': data})

# Seller Detail
def seller_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data = AuctionUser  .objects.get(id=pid)
    return render(request, 'administration/seller_detail.html', {'data': data})

# Show Dropdowns
def show_dropdowns(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'courses_dropdown_list_options.html', {'categories': categories})

def load_courses(request):
    # Your logic to load courses
    courses = [...]  # Replace with actual course data
    return JsonResponse(courses, safe=False)
"""
def bidding_history(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Fetch the bidding history for the authenticated user
    bids = Bid.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'bids': bids
    }
    return render(request, 'bidding_history.html', context)"""