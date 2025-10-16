

# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, g
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'alif.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace_this_with_env_secret'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM products')
    products = cur.fetchall()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product(id):
    db = get_db()
    cur = db.execute('SELECT * FROM products WHERE id=?', (id,))
    product = cur.fetchone()
    if not product:
        return "Product not found", 404
    return render_template('products.html', product=product)

@app.route('/order', methods=['POST'])
def order():
    data = request.json or request.form
    name = data.get('name')
    phone = data.get('phone')
    address = data.get('address')
    items = data.get('items')  # expecting JSON string or array
    total = float(data.get('total', 0))

    if isinstance(items, str):
        items_json = items
    else:
        items_json = json.dumps(items)

    db = get_db()
    db.execute('INSERT INTO orders (customer_name, phone, address, items, total) VALUES (?, ?, ?, ?, ?)',
               (name, phone, address, items_json, total))
    db.commit()

    return jsonify({'status': 'ok', 'message': 'Order received'}), 201

@app.route('/admin')
def admin():
    # VERY simple admin: no auth for demo. Add auth in production.
    db = get_db()
    cur = db.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = cur.fetchall()
    return render_template('admin.html', orders=orders)

# Simple API to get products as JSON (used by frontend)
@app.route('/api/products')
def api_products():
    db = get_db()
    cur = db.execute('SELECT * FROM products')
    products = [dict(row) for row in cur.fetchall()]
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/cart')
def cart():
    # Example: cart items (later connect to session or DB)
    cart_items = []
    return render_template('cart.html', cart_items=cart_items)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Collect form data from user (name, address, phone, etc.)
        pass
    return render_template('checkout.html')


@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    # (You can later save to DB or send email here)
    return f"Thank you, {name}! Your order has been received."

