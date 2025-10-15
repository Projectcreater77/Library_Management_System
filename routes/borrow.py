from flask import Blueprint, jsonify, session
from db import get_db_connection
import datetime

borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")


@borrow_bp.route("/book/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must log in to borrow books."}), 401

    book = cursor.fetchone()
    if not book or book["available_copies"] <= 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Book not available"}), 400
    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(days=14)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book borrowed successfully", "due_date": str(due_date)})
