from flask import Flask, render_template, redirect, url_for, request, session, flash
from routes.books import books_bp
from routes.borrow import borrow_bp
from routes.chatbot import chatbot_bp
from db import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(books_bp)
app.register_blueprint(borrow_bp)
app.register_blueprint(chatbot_bp)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s AND password_hash=%s", (user_id, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            error = "Invalid ID or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
