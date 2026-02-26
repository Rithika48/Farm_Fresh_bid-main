<<<<<<< HEAD
<div align="center">

# BidScape

</div>

## BidScape-Online_Auction_Website

### Introduction:
The bidding-based web platform serves as a marketplace for both individuals and businesses to engage in buying and selling a wide range of goods and services. Users on the platform can participate in auctions and submit bids to purchase items or services of interest. Additionally, sellers can list their products or services for potential buyers to bid on. The platform provides a convenient and accessible online venue for facilitating transactions, promoting competitive pricing, and connecting buyers and sellers from various backgrounds and industries.

### Problem statement:
The current lack of a reliable and user-friendly online auction website creates difficulties for individuals and businesses looking to buy and sell goods and services. Existing platforms often suffer from inadequate security measures, limited functionality, and a lack of effective administration. These issues result in a suboptimal user experience and hinder the efficient and transparent exchange of items. Therefore, there is a need to develop an online auction website that addresses these challenges by providing a secure, intuitive, and feature-rich platform for users to participate in buying and selling activities. 
This website have features such as
1. User able to create auction for selling a product or service with an expiry timeline.
2. Users are able to bid in increasing order. No bids for same amount is accepted.
3. Home page lists all auctions with most bids for a current auction.
4. When timeline expires, the product/service is rewarded to highest bidder and order is placed with cash on delivery using razorpay.
5. constant supervision by the administrator for security reasons.
6. Google Analytics is utilized to gather real-time data, while Looker Studio is employed to visualize and analyze that data in a comprehensive manner.
7. Deployed on Docker


Used Tech Stack
1. Django
2. Sqlite
3. HTML
4. CSS
5. Javascript
6. Node.js
7. Python

#### Install

1. Create a virtual environment

    `virtualenv venv`

    Or

    `python3.8 -m venv venv`

2. Activate it

    `source venv/bin/activate`

3. Clone the repository and install the packages in the virtual env:

    `pip install -r requirements.txt`

4. Add `.env` file.

    `cp .env.dev.sample .env`

5. Add Github client ID and client secret in the `.env` file

#### Run

1.With the venv activate it, execute:

    python manage.py collectstatic

*Note* : Collect static is not necessary when debug is True (in dev mode)

2. Create initial database:

    `python manage.py migrate`


3. Load demo data (optional):

    `python manage.py loaddata fixtures/app_name_initial_data.json --app app.model_name`

4. Run server:

    `python manage.py runserver`
  
5. If you are Docker user then you can use this command: <br>
   `docker pull omdubey/auction_websitee` 
    
=======
# Farm_Fresh_bid
Real-time Django vegetable auction platform — sellers list, buyers bid, highest bidder wins!
>>>>>>> a2a6ed02e203d7afa0f1f4dd70098fb45abbca3f
