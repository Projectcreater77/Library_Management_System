from flask import Blueprint, jsonify, session
from db import get_db_connection
import datetime

borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")


@borrow_bp.route("/book/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must log in to borrow books."}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT available_copies FROM books WHERE id=%s', (book_id,))
    book = cursor.fetchone()
    if not book or book["available_copies"] <= 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Book not available"}), 400
    cursor.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id=%s', (book_id,))
    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(days=14)
    cursor.execute(
        "INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)",
        (user_id, book_id, borrow_date, due_date)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book borrowed successfully", "due_date": str(due_date)})
