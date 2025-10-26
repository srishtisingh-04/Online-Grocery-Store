from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db
from models.product import Product, Category
from models.order import Order, OrderItem, CartItem
from models.user import User
from datetime import datetime

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/products', methods=['GET'])
def get_products():
    try:
        # Get query parameters
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        # Paginate results
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        print(f"[DEBUG] Getting cart for user_id: {user_id} (type: {type(user_id)})")
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        print(f"[DEBUG] Converted user_id: {user_id}")
        
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        print(f"[DEBUG] Found {len(cart_items)} cart items")
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items if item.product)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total_amount': float(total_amount)
        }), 200
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Cart loading error: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        
        # Check if product exists and is active
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock availability
        if product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            user_id=user_id, product_id=product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
            if existing_item.quantity > product.stock_quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({'message': 'Item added to cart successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        data = request.get_json()
        
        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({'error': 'Quantity is required'}), 400
        
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        if quantity <= 0:
            db.session.delete(cart_item)
        else:
            if cart_item.product.stock_quantity < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            cart_item.quantity = quantity
        
        db.session.commit()
        
        return jsonify({'message': 'Cart item updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from cart successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        data = request.get_json()
        
        shipping_address = data.get('shipping_address')
        if not shipping_address:
            return jsonify({'error': 'Shipping address is required'}), 400
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total and validate stock
        total_amount = 0
        for item in cart_items:
            if not item.product or not item.product.is_active:
                return jsonify({'error': f'Product {item.product_id} is no longer available'}), 400
            
            if item.product.stock_quantity < item.quantity:
                return jsonify({'error': f'Insufficient stock for {item.product.name}'}), 400
            
            total_amount += float(item.product.price * item.quantity)
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            
            # Update stock
            item.product.stock_quantity -= item.quantity
        
        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'orders': [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        # Convert string ID to int for database query
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
