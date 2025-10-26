-- Initial data for Online Grocery Store
USE grocery_store;

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Fruits & Vegetables', 'Fresh fruits and vegetables'),
('Dairy & Eggs', 'Milk, cheese, eggs and dairy products'),
('Meat & Seafood', 'Fresh meat, poultry and seafood'),
('Bakery', 'Bread, pastries and baked goods'),
('Pantry Staples', 'Rice, pasta, canned goods and spices'),
('Beverages', 'Soft drinks, juices, coffee and tea'),
('Snacks', 'Chips, cookies, nuts and other snacks'),
('Frozen Foods', 'Frozen meals, ice cream and frozen vegetables');

-- Insert sample products
INSERT INTO products (name, description, price, category_id, stock_quantity, image_url) VALUES
-- Fruits & Vegetables
('Fresh Apples', 'Red delicious apples, 1kg', 2.99, 1, 50, '/static/images/apples.jpg'),
('Bananas', 'Fresh bananas, 1 bunch', 1.49, 1, 30, '/static/images/bananas.jpg'),
('Carrots', 'Fresh carrots, 1kg', 1.99, 1, 40, '/static/images/carrots.jpg'),
('Tomatoes', 'Fresh tomatoes, 1kg', 2.49, 1, 35, '/static/images/tomatoes.jpg'),

-- Dairy & Eggs
('Whole Milk', 'Fresh whole milk, 1 liter', 2.19, 2, 25, '/static/images/milk.jpg'),
('Eggs', 'Fresh eggs, 12 count', 3.49, 2, 20, '/static/images/eggs.jpg'),
('Cheddar Cheese', 'Sharp cheddar cheese, 200g', 4.99, 2, 15, '/static/images/cheese.jpg'),

-- Meat & Seafood
('Chicken Breast', 'Fresh chicken breast, 1kg', 8.99, 3, 10, '/static/images/chicken.jpg'),
('Salmon Fillet', 'Fresh salmon fillet, 500g', 12.99, 3, 8, '/static/images/salmon.jpg'),

-- Bakery
('Whole Wheat Bread', 'Fresh whole wheat bread', 2.99, 4, 20, '/static/images/bread.jpg'),
('Croissants', 'Fresh croissants, 6 pack', 4.49, 4, 15, '/static/images/croissants.jpg'),

-- Pantry Staples
('White Rice', 'Long grain white rice, 2kg', 3.99, 5, 30, '/static/images/rice.jpg'),
('Pasta', 'Spaghetti pasta, 500g', 1.99, 5, 25, '/static/images/pasta.jpg'),

-- Beverages
('Orange Juice', 'Fresh orange juice, 1 liter', 3.49, 6, 20, '/static/images/orange_juice.jpg'),
('Coffee Beans', 'Premium coffee beans, 250g', 7.99, 6, 12, '/static/images/coffee.jpg'),

-- Snacks
('Potato Chips', 'Classic potato chips, 150g', 2.49, 7, 40, '/static/images/chips.jpg'),
('Chocolate Cookies', 'Chocolate chip cookies, 200g', 3.99, 7, 25, '/static/images/cookies.jpg'),

-- Frozen Foods
('Frozen Pizza', 'Margherita pizza, frozen', 5.99, 8, 15, '/static/images/pizza.jpg'),
('Ice Cream', 'Vanilla ice cream, 1 liter', 4.99, 8, 20, '/static/images/ice_cream.jpg');

-- Insert admin user (password: admin123)
INSERT INTO users (username, email, password_hash, first_name, last_name, is_admin) VALUES
('admin', 'admin@grocerystore.com', 'scrypt:32768:8:1$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Admin', 'User', TRUE);

-- Insert sample customer (password: customer123)
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address) VALUES
('customer1', 'customer@example.com', 'scrypt:32768:8:1$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'John', 'Doe', '555-0123', '123 Main St, City, State 12345');
