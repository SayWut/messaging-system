# Messaging System

**Description**

This is a Django-based application for managing messages between users. It provides functionalities for user registration, message sending, receiving, and deletion.

**Features**

- User registration with password validation
- Message sending with sender, receiver, subject, and message body fields
- Message retrieval for a user based on optional `unread` filter
- Message deletion based on sender or receiver username (one required)

**Installation**

1. **Prerequisites:** Ensure you have Python (version 3.x recommended) and pip (package manager) installed.
2. **Clone the repository:**

   ```bash
   git clone https://docs.github.com/articles/changing-your-github-username
   ```

3. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv  # Or equivalent command for your Python version
   ./venv/Scripts/activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

**Usage**

1. **Run migrations:**

   ```bash
   python manage.py migrate --run-syncdb
   ```

   This creates the necessary database tables.

2. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   This will start the Django development server at http://127.0.0.1:8000/ by default.
