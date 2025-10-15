# init_db.py
import sqlite3

conn = sqlite3.connect('data/alif.db')
c = conn.cursor()

# Products table
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    image TEXT
)
''')

# Orders table
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT,
    address TEXT,
    items TEXT,  -- JSON string of items
    total REAL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Admin user table (simple)
c.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Insert sample products if empty
c.execute('SELECT COUNT(*) FROM products')
if c.fetchone()[0] == 0:
    products = [
        ('30 pcs Eggs', 'Farm-fresh eggs, full tray (30 pieces)', 500.00, 50, ''),
        ('4 pcs Eggs', 'Small pack for daily use (4 pieces)', 75.00, 100, ''),
        ('Milk - 10 Litres', 'Pure cow milk, bulk pack (10 litres)', 750.00, 30, ''),
        ('Milk - 1 Litre', 'Fresh cow milk, 1 litre bottle', 100.00, 100, ''),
        ('Duck (Per Piece)', 'Farm-raised duck, ready for cooking', 600.00, 40, '')
    ]
    c.executemany('INSERT INTO products (name, description, price, stock, image) VALUES (?, ?, ?, ?, ?)', products)

# Insert a default admin (password is 'admin' plain text -> change later)
c.execute('SELECT COUNT(*) FROM admin')
if c.fetchone()[0] == 0:
    c.execute('INSERT INTO admin (username, password) VALUES (?, ?)', ('admin', 'admin'))

conn.commit()
conn.close()

print("Database initialized at data/alif.db")
