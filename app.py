import os
import sqlite3
from datetime import datetime
from flask import Flask, g, jsonify, request, render_template
from flask_cors import CORS

# Paths and DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'expenses.db')

# Ensure instance folder exists
os.makedirs(INSTANCE_DIR, exist_ok=True)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    # Create DB and table if not exists
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB at import time (works with Flask 3.x)
init_db()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    db = get_db()
    cur = db.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC')
    rows = cur.fetchall()
    expenses = [dict(r) for r in rows]
    return jsonify(expenses), 200

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json() or {}
    errors = []

    amount = data.get('amount')
    category = data.get('category')
    description = data.get('description') or ''
    date = data.get('date')

    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            errors.append('amount must be greater than 0')
    except Exception:
        errors.append('amount must be a number')

    # Validate category
    if not category or not isinstance(category, str) or not category.strip():
        errors.append('category is required')

    # Validate date (accept ISO format YYYY-MM-DD)
    try:
        date_str = datetime.fromisoformat(date).date().isoformat()
    except Exception:
        errors.append('date must be a valid ISO date (YYYY-MM-DD)')

    if errors:
        return jsonify({'errors': errors}), 400

    db = get_db()
    cur = db.execute(
        'INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)',
        (amount, category.strip(), description.strip(), date_str)
    )
    db.commit()
    new_id = cur.lastrowid
    row = db.execute('SELECT * FROM expenses WHERE id = ?', (new_id,)).fetchone()
    return jsonify(dict(row)), 201

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    db = get_db()
    cur = db.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'success': True}), 200

@app.route('/api/summary', methods=['GET'])
def summary():
    db = get_db()
    cur = db.execute('SELECT category, SUM(amount) as total FROM expenses GROUP BY category')
    rows = cur.fetchall()
    summary = {row['category']: row['total'] for row in rows}
    return jsonify(summary), 200

if __name__ == '__main__':
    app.run(debug=True)
