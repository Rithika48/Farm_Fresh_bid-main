# 🌾 Farm Fresh Bid: Bid For The Best

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-Web%20Framework-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Docker](https://img.shields.io/badge/Deployment-Docker-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)


An online agricultural bidding platform where farmers and buyers connect through competitive bidding.

The platform creates a transparent, fair, and efficient digital marketplace connecting farmers directly with buyers.

---

## ⚠ Problem Statement

Farmers frequently face challenges in selling their produce due to:

- Dependence on middlemen
- Lack of transparency in crop pricing
- Limited market reach
- Unfair price negotiation

These issues reduce farmer profits and limit access to competitive markets.

The objective of this project is to create a secure online bidding platform where farmers can list crops and buyers can place competitive bids, ensuring fair pricing and better market opportunities.

---

## 📌 Project Description (Solution)

**Farm Fresh Bid: Bid For The Best** is an online agricultural bidding platform developed to improve the way farmers sell their products. The system allows farmers to list their crops on the platform while buyers can place competitive bids to purchase them.

This platform eliminates traditional intermediaries and creates a **direct connection between farmers and buyers**, ensuring that farmers receive fair prices for their products.

The application is built using the **Django web framework** with **PostgreSQL** as the database. The system includes three main roles: **Farmer, Bidder, and Administrator**, each with specific functionalities that support the overall auction process.

---

## ⭐ Project Highlights

- ✅ Farmer-to-buyer direct marketplace  
- ✅ Secure bidding system  
- ✅ Admin verification for users  
- ✅ Real-time crop listings  
- ✅ PostgreSQL database integration  
- ✅ Built using Django framework  

---

## 👥 System Roles

### 👨‍🌾 Farmer

Farmers can sell their crops using the bidding system.

**Features**

- Register and login
- Add crop details
- Upload crop information
- View bids from bidders
- Accept the best bid

---

### 💰 Bidder

Bidders compete to purchase farmer crops.

**Features**

- Register and login
- Browse available crops
- Place bids
- Track bidding activity
- View bidding results

---

### 🛠 Admin

Admin manages and monitors the platform.

**Features**

- Approve farmer registrations
- Approve bidder registrations
- Manage crop listings
- Monitor bids
- Control platform activity

**Admin Panel**

```
http://127.0.0.1:8000/admin
```

---

## 🔄 System Workflow

```
Farmer → Upload Crop
         │
         ▼
Bidder → Place Bid
         │
         ▼
Farmer → Accept Bid
         │
         ▼
Transaction Completed
```

---

## 🛠 Tech Stack

### Backend

- Python
- Django Framework

### Frontend

- HTML
- CSS
- JavaScript

### Database

- PostgreSQL

### Deployment

- Docker

---

## 🗄 Database

The application uses PostgreSQL to store all system data including:

- Users
- Crops
- Bids
- Auction information

Example configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auction_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📊 Dataset

This project does not require an external dataset.

All data is generated dynamically during platform usage, including:

- User registrations
- Crop listings
- Bidding activity
- Auction results

The data is securely stored in the PostgreSQL database.

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Rithika48/Farm_Fresh_bid-main.git
```

### 2. Navigate to the Project Folder

```bash
cd Farm_Fresh_bid-main
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

Activate the environment

**Windows**

```bash
env\Scripts\activate
```

**Linux / Mac**

```bash
source env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

### 7. Run the Application

```bash
python manage.py runserver
```

### 8. Open in Browser

Main Application

```
http://127.0.0.1:8000
```

Admin Panel

```
http://127.0.0.1:8000/admin
```

## 🎥 Project Demo

This GIF demonstrates the core workflow of the Farm Fresh Bid platform.

![Farm Fresh Bid Demo](Screenshots/demo7.gif)

---

## 🚀 Future Improvements

- Secure online payment integration
- Email and SMS notifications
- Mobile application support
- Advanced analytics dashboard for farmers
- Multi-language support
