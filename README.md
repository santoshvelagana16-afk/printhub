# 🖨️ PrintHub — Online Printing Service Platform

A full-featured Django web application for an online printing service.

---

## 🚀 Quick Start (3 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup (migrations + fixtures + superuser)
python setup.py

# 3. Start server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔐 Default Credentials

| Role       | Username | Password  |
|------------|----------|-----------|
| Admin      | admin    | admin123  |

Admin panel: **http://127.0.0.1:8000/admin/**

---

## 📁 Project Structure

```
printhub/
├── manage.py
├── requirements.txt
├── setup.py                    # One-time setup script
├── db.sqlite3                  # Created after setup
│
├── printhub/                   # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── views.py                # Home + Contact
│
├── users/                      # Auth & Profiles
│   ├── models.py               # UserProfile
│   ├── views.py                # Register / Login / Logout / Profile
│   ├── forms.py
│   └── urls.py
│
├── services/                   # Printing Services
│   ├── models.py               # ServiceCategory, Service, PrintingOption, etc.
│   ├── views.py                # Service pages + AJAX price endpoints
│   ├── urls.py
│   └── fixtures/
│       └── initial_data.json   # Sample services & pricing
│
├── orders/                     # Cart, Orders, Payment
│   ├── models.py               # Cart, CartItem, Order, OrderItem
│   ├── views.py                # Cart / Checkout / Payment / Tracking
│   ├── urls.py
│   └── context_processors.py  # Cart count in navbar
│
├── templates/
│   ├── base.html               # Navbar + Footer layout
│   ├── home.html               # Landing page
│   ├── contact.html
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── services/
│   │   ├── services_list.html
│   │   ├── printing.html       # With live price calculator
│   │   ├── binding.html
│   │   └── custom_printing.html
│   └── orders/
│       ├── cart.html
│       ├── payment.html        # Demo payment UI (UPI/Card/NetBanking/COD)
│       ├── confirmation.html
│       ├── order_list.html
│       ├── order_detail.html
│       └── tracking.html       # Live status tracker
│
├── static/
│   ├── css/main.css            # Full custom stylesheet
│   └── js/main.js
│
└── media/                      # User-uploaded files
    └── uploads/
```

---

## ✨ Features

### User Authentication
- Register / Login / Logout with validation
- Profile page with editable details
- Order history on profile

### Services
| Service | Features |
|---------|----------|
| **Document Printing** | Upload PDF/DOC, choose B&W/Colour, A4/A3/Letter/Legal, Single/Double side, copies |
| **Spiral Binding** | Spiral, Comb, Tape, Hard Cover binding types |
| **Custom Printing** | T-Shirts, Mugs, Photo prints, Posters, Banners, Visiting Cards |

### Smart Price Calculator
- AJAX live price update on the printing form as you change options
- GST (18%) calculated at checkout

### Cart & Orders
- Add multiple services to cart
- Remove items
- Checkout → Payment → Confirmation flow

### Demo Payment Page
- UPI (with app selector: GPay / PhonePe / Paytm)
- Debit/Credit Card (formatted input)
- Net Banking (bank selector)
- Cash on Delivery
- 2.5-second processing animation → redirects to confirmation

### Order Tracking
- Status: Pending → Confirmed → Processing → Ready → Completed
- Visual progress bar + timeline

### Admin Panel
- Manage users, orders, services
- Edit order status inline
- Add/edit service pricing

---

## 🛠️ Manual Setup (step-by-step)

```bash
# Install
pip install -r requirements.txt

# Migrations
python manage.py makemigrations users services orders
python manage.py migrate

# Load sample data
python manage.py loaddata services/fixtures/initial_data.json

# Create superuser
python manage.py createsuperuser

# Run
python manage.py runserver
```

---

## 📦 Tech Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (swap to MySQL by changing `DATABASES` in `settings.py`)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons, Google Fonts (Syne + DM Sans)
- **Storage**: Local filesystem (Django `MEDIA_ROOT`)

---

## 🗄️ Switch to MySQL

In `printhub/settings.py`, replace the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'printhub_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Then install: `pip install mysqlclient`

---

## 📄 License

MIT — free to use and modify.
