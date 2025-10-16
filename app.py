from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for cart session

# Sample products (replace/add as needed)
# Sample products in Taka
products = [
    {"id": 1, "name": "30 pcs Eggs", "description": "Farm-fresh eggs, full tray (30 pieces)", "price": 500.00},
    {"id": 2, "name": "4 pcs Eggs", "description": "Small pack for daily use (4 pieces)", "price": 75.00},
    {"id": 3, "name": "Milk - 10 Litres", "description": "Pure cow milk, bulk pack (10 litres)", "price": 750.00},
    {"id": 4, "name": "Milk - 1 Litre", "description": "Fresh cow milk, 1 litre bottle", "price": 100.00},
    {"id": 5, "name": "Duck (Per Piece)", "description": "Farm-raised duck, ready for cooking", "price": 600.00},
]

# Helper function to load gallery images from static/images/farm/
def get_farm_images():
    folder = 'static/images/farm'
    if not os.path.exists(folder):
        return []
    files = os.listdir(folder)
    return [f"farm/{f}" for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Home page
@app.route('/')
def index():
    farm_images = get_farm_images()
    return render_template('index.html', products=products, farm_images=farm_images)

# Cart page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

# Add to cart (POST via AJAX or form)
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Get the product
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart_items = session.get('cart', [])
        cart_items.append(product)
        session['cart'] = cart_items
    return redirect(url_for('cart'))

# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        # Here you can process payment or save order to DB
        session['cart'] = []  # Clear cart after checkout
        return f"Thank you {name}! Your order has been submitted successfully."
    return render_template('checkout.html', cart_items=cart_items)

# Example product detail page
@app.route('/product/<int:id>')
def product(id):
    product_item = next((p for p in products if p['id'] == id), None)
    if not product_item:
        return "Product not found", 404
    return render_template('product.html', product=product_item)

if __name__ == "__main__":
    app.run(debug=True)
