from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

responses = {
    'hello': 'Hi there! How can I assist you in the library today?',
    'help': 'You can ask about categories, borrowing, opening hours, or library facilities.',
    'timing': 'The library is open from 9 AM to 7 PM every day except Sundays.',
    'categories': 'We offer books in Math, Science, Literature, Python, Linux, and more.',
    'math books': 'Math books include Algebra, Calculus, Geometry, and more. Find them in "Math" category.',
    'science books': 'We have Physics, Chemistry, and Biology books in the Science section.',
    'linux books': 'Linux books guide you from basics to advanced system administration.',
    'python books': 'We have Python for Beginners, Data Science with Python, and more in the Python section.',
    'operating system books': 'Our OS section covers Windows, Linux, Unix, and concepts in OS.',
    'how to borrow': 'Click "Borrow" on a book. Each user can borrow up to 3 books at a time.',
    'return book': 'Return books to the counter or click "Return" if implemented online.',
    'max books': 'Each user can borrow up to 3 books at a time.',
    'late fee': 'Late fee is ₹10 per day after the due date.',
    'library location': 'The library is located on the 2nd floor of the Main Building.',
    'membership': 'Library membership is open to all students and staff. Register at the counter.',
    'digital resources': 'We offer online journals and e-books. Ask a librarian for access.',
    'contact': 'Contact us at knowledgekartlibrary@gmail.com or call 123-456-7890.',
    'events': 'Library events are posted on the notice board and website regularly.',
    'study rooms': 'Study rooms can be reserved at the counter.',
    'thank you': "You're welcome! Have a great day and happy reading.",
    # Fallback
    'default': "Sorry, I didn't understand that. Please ask about timing, books, borrowing, or say 'help'."
}


@chatbot_bp.route('/', methods=['POST'])
def chatbot():
    data = request.get_json()
    msg = data.get('message', '').strip().lower()
    reply = responses.get(msg, responses['default'])
    return jsonify({'reply': reply})
