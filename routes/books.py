from flask import Blueprint, request, jsonify
from db import get_db_connection

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/', methods=['GET'])
def get_books():
    category = request.args.get('category')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # if category:
        # Code for database
        
    # else:
        # Code for database

    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)