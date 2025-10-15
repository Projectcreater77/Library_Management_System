document.addEventListener('DOMContentLoaded', () => {
  const booksContainer = document.getElementById('booksContainer');
  const searchInput = document.getElementById('searchInput');
  const categoryButtons = document.querySelectorAll('.category-btn');
  const chatbotToggle = document.getElementById('chatbotToggle');
  const chatbot = document.getElementById('chatbot');
  const chatMessages = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const sendChatBtn = document.getElementById('sendChatBtn');

  let books = [];
  let currentCategory = 'All';

  async function fetchBooks(category = 'All') {
    let url = '/books';
    if (category !== 'All') {
      url += `?category=${encodeURIComponent(category)}`;
    }
    const resp = await fetch(url);
    books = await resp.json();
    renderBooks(books);
  }

  function renderBooks(bookList) {
    booksContainer.innerHTML = '';
    if (!bookList.length) {
      booksContainer.innerHTML = '<p>No books found.</p>';
      return;
    }
    bookList.forEach(book => {
      const div = document.createElement('div');
      div.className = 'book-card';
      div.innerHTML = `
        <h3>${book.title}</h3>
        <p>Author: ${book.author || 'Unknown'}</p>
        <p>Category: ${book.category || 'N/A'}</p>
        <p>Available copies: ${book.available_copies}</p>
        <button ${book.available_copies <= 0 ? 'disabled' : ''} onclick="borrowBook(${book.id})">Borrow</button>
      `;
      booksContainer.appendChild(div);
    });
  }

  function filterBooks() {
    const query = searchInput.value.toLowerCase();
    let filteredBooks = books.filter(book => {
      return (
        book.title.toLowerCase().includes(query) ||
        (book.author && book.author.toLowerCase().includes(query)) ||
        (book.category && book.category.toLowerCase().includes(query))
      );
    });
    renderBooks(filteredBooks);
  }

  searchInput.addEventListener('input', filterBooks);

  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-category');
      fetchBooks(currentCategory);
      searchInput.value = '';
    });
  });

  window.borrowBook = async function(bookId) {
  try {
    const resp = await fetch(`/borrow/book/${bookId}`, { method: 'POST' });
    const data = await resp.json();
    alert(data.message || data.error);
    fetchBooks(currentCategory);
  } catch (error) {
    alert('Error borrowing book.');
  }
};

  chatbotToggle.addEventListener('click', () => {
    chatbot.classList.toggle('hidden');
  });

  sendChatBtn.addEventListener('click', sendChatMessage);

  function appendChatMessage(text, sender) {
    const msg = document.createElement('div');
    msg.textContent = text;
    msg.className = `chat-message ${sender}`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    appendChatMessage(`You: ${message}`, 'user');

    try {
      const resp = await fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await resp.json();
      appendChatMessage(`Bot: ${data.reply}`, 'bot');
    } catch (error) {
      appendChatMessage('Bot: Sorry, there was an error.', 'bot');
    }
    chatInput.value = '';
  }
  fetchBooks();
});
