import os
from flask import Flask, request, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'users.db'

def get_db():
    if 'db' not in g:
        # Use a context manager for safety
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.route('/user')
def get_user_profile():
    user_id = request.args.get('id')
    
    # Check if user_id exists and is numeric
    if not user_id or not user_id.isdigit():
        return {"error": "Invalid or missing user ID"}, 400

    db = get_db()
    cursor = db.cursor()

    # Use parameterized query to avoid SQL injection
    query = "SELECT * FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))

    user_data = cursor.fetchone()

    # Clearer variable names
    user_profile = process_data(user_data)
    response = format_response(user_profile)

    return response

# (Assume process_data and format_response exist elsewhere)
