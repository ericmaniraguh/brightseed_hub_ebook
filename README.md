# BrightSeedHub Backend API Documentation

This is the backend REST API for the **BrightSeedHub eBook Marketplace**.  
Built with **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **JWT Authentication**.

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL (Docker container recommended)
- Virtual Environment

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Create Superuser (Admin)
python manage.py createsuperuser

# Start Server
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000/api/`

---

## 🔐 Authentication

All protected endpoints require a **Bearer Token** in the header:
`Authorization: Bearer <your_access_token>`

### 1. Register User

**POST** `/api/users/register/`
Creates an inactive user and sends an OTP (check console for code).

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "+250788123456"
}
```

### 2. Verify OTP

**POST** `/api/users/verify-otp/`
Verifies the 6-digit code and activates the account.

```json
{
  "email": "john@example.com",
  "code": "123456"
}
```

### 3. Login (Get Token)

**POST** `/api/users/login/`
Returns Access and Refresh tokens.

```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

### 4. Refresh Token

**POST** `/api/users/token/refresh/`

```json
{
  "refresh": "<your_refresh_token>"
}
```

### 5. Get My Profile

**GET** `/api/users/me/`
(Requires Auth)

---

## 📚 Books & Categories

### 1. List Categories

**GET** `/api/categories/`

### 2. List Books

**GET** `/api/books/`
Supports filtering: `?category=<id>&search=<query>`

- Note: `content_url` will be `null` unless you have purchased the book.

### 3. Get Book Details

**GET** `/api/books/<id>/`

---

## 🛒 Orders

### 1. Create Order

**POST** `/api/orders/`
(Requires Auth). Creates a "PENDING" purchase.

```json
{
  "book": 1,
  "payment_method": "CARD"
}
```

### 2. List My Orders

**GET** `/api/orders/`
(Requires Auth). Returns your purchase history.

---

## 💳 Payments

### 1. Process Payment (Mock)

**POST** `/api/payments/process/`
(Requires Auth). Simulates a successful payment.

- Updates Order status to `SUCCESS`.
- Grants access to the Book `content_url`.

```json
{
  "order_id": 5,
  "payment_token": "simulated_token_123"
}
```

---

## 🔧 Admin Panel

Manage Users, Books, and Orders securely.
URL: `http://127.0.0.1:8000/admin/`
User: `brightseed_hub` / Pass: `admin`
