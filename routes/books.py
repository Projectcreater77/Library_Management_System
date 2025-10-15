from flask import Blueprint, request, jsonify
from db import get_db_connection

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/', methods=['GET'])
def get_books():
    category = request.args.get('category')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if category:
        cursor.execute("""
            SELECT b.id, b.title, b.author, c.name AS category, b.available_copies
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE c.name = %s
        """, (category,))
        
    else:
        cursor.execute("""
            SELECT b.id, b.title, b.author, c.name AS category, b.available_copies
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
        """)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)
