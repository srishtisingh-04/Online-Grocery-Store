# Online Grocery Store - Setup Script

# This script helps you set up the Online Grocery Store application

echo "🛒 Online Grocery Store Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL is not installed. Please install MySQL 5.7+ first."
    echo "   You can download it from: https://dev.mysql.com/downloads/"
    exit 1
fi

echo "✅ MySQL found"

# Create database
echo "🗄️  Setting up database..."
echo "Please enter your MySQL root password:"
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_store;"

if [ $? -eq 0 ]; then
    echo "✅ Database created successfully"
else
    echo "❌ Failed to create database"
    exit 1
fi

# Import database schema
echo "📋 Importing database schema..."
mysql -u root -p grocery_store < database/schema.sql

if [ $? -eq 0 ]; then
    echo "✅ Database schema imported successfully"
else
    echo "❌ Failed to import database schema"
    exit 1
fi

# Import initial data
echo "📊 Importing initial data..."
mysql -u root -p grocery_store < database/init_data.sql

if [ $? -eq 0 ]; then
    echo "✅ Initial data imported successfully"
else
    echo "❌ Failed to import initial data"
    exit 1
fi

# Create .env file
echo "⚙️  Creating environment configuration..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ Environment file created (.env)"
    echo "⚠️  Please update the .env file with your database credentials"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update the .env file with your database credentials"
echo "2. Run the application: python app.py"
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "Default login credentials:"
echo "Admin: username=admin, password=admin123"
echo "Customer: username=customer1, password=customer123"
