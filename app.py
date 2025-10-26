from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config
from models.database import db

jwt = JWTManager()

# Import models to ensure they are registered with SQLAlchemy
from models.user import User
from models.product import Product, Category
from models.order import Order, OrderItem, CartItem

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure JWT to handle integer identities
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=int(identity)).one_or_none()
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.customer import customer_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Frontend routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/orders')
    def orders():
        return render_template('orders.html')
    
    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')
    
    @app.route('/admin')
    def admin_dashboard():
        return render_template('admin/dashboard.html')
    
    @app.route('/admin/products')
    def admin_products():
        return render_template('admin/products.html')
    
    @app.route('/admin/orders')
    def admin_orders():
        return render_template('admin/orders.html')
    
    @app.route('/admin/analytics')
    def admin_analytics():
        return render_template('admin/analytics.html')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
