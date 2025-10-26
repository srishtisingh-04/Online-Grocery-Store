# Online Grocery Store

A full-stack web application for online grocery shopping with customer and admin interfaces.

## Features

### Customer Features
- User registration and login
- Browse products by category
- Search products
- Add items to cart
- Checkout and place orders
- View order history

### Admin Features
- Product management (add, edit, delete)
- Category management
- Order processing and status updates
- Sales analytics
- User management

## Technology Stack
- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python Flask
- **Database**: MySQL
- **Authentication**: JWT-based secure login

## Setup Instructions

### Prerequisites
- Python 3.7+
- MySQL 5.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ECommerce and Retail
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Create a MySQL database named `grocery_store`
   - Update database credentials in `config.py` if needed
   - Run the database schema:
     ```bash
     mysql -u root -p grocery_store < database/schema.sql
     mysql -u root -p grocery_store < database/init_data.sql
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Customer interface: http://localhost:5000
   - Admin interface: http://localhost:5000/admin
   - API endpoints: http://localhost:5000/api/

## Default Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Customer
- Username: `customer1`
- Password: `customer123`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Customer
- `GET /api/customer/products` - Get products
- `GET /api/customer/products/<id>` - Get product details
- `GET /api/customer/categories` - Get categories
- `GET /api/customer/cart` - Get cart items
- `POST /api/customer/cart` - Add to cart
- `PUT /api/customer/cart/<id>` - Update cart item
- `DELETE /api/customer/cart/<id>` - Remove from cart
- `POST /api/customer/checkout` - Place order
- `GET /api/customer/orders` - Get user orders

### Admin
- `GET /api/admin/products` - Get all products
- `POST /api/admin/products` - Create product
- `PUT /api/admin/products/<id>` - Update product
- `DELETE /api/admin/products/<id>` - Delete product
- `GET /api/admin/categories` - Get all categories
- `POST /api/admin/categories` - Create category
- `PUT /api/admin/categories/<id>` - Update category
- `GET /api/admin/orders` - Get all orders
- `PUT /api/admin/orders/<id>/status` - Update order status
- `GET /api/admin/analytics/sales` - Get sales analytics

## Project Structure
```
ECommerce and Retail/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt       # Python dependencies
├── database/
│   ├── schema.sql        # Database schema
│   └── init_data.sql     # Initial sample data
├── models/
│   ├── user.py           # User model
│   ├── product.py        # Product and Category models
│   └── order.py          # Order, OrderItem, CartItem models
├── routes/
│   ├── auth.py           # Authentication routes
│   ├── customer.py       # Customer routes
│   └── admin.py          # Admin routes
├── static/
│   ├── css/style.css     # Custom styles
│   ├── js/main.js        # Custom JavaScript
│   └── images/           # Product images
└── templates/
    ├── base.html         # Base template
    └── admin/
        └── base.html     # Admin base template
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is licensed under the MIT License.
