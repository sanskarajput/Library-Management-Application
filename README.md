# 📚 Library Management Application

A comprehensive web-based Library Management System built with Flask that provides an efficient and user-friendly platform for managing books, sections, users and library operations. The application supports two distinct user roles: **Librarians** and **Readers**, each with tailored functionalities.

## 🌟 Features

### 🔐 Authentication & User Management
- **User Registration & Login**: Secure signup and login system for readers
- **Librarian Authentication**: Separate login portal for librarians with role-based access
- **Password Security**: Bcrypt hashing for secure password storage
- **Profile Management**: Upload profile pictures, view account information, and delete accounts
- **Session Management**: Secure session handling with Flask-Login

### 📖 Book Management
- **CRUD Operations**: Create, read, update, and delete books with metadata (name, author, description, cover images, PDF attachments)
- **Book Organization**: Assign/remove books from sections and view by section
- **Book Tracking**: Issue count tracking and date management

### 📑 Section Management
- **CRUD Operations**: Create, edit, and delete sections with descriptions and custom images
- **Section Features**: View all sections with book counts and add multiple books to sections in bulk

### 📥 Book Request & Access System
- **Request Management**: Users can request books for various durations (6 hours to 2 weeks), view pending requests, and cancel requests
- **Access Control**: Librarians review and approve/reject requests with configurable access durations
- **Automatic Expiration**: Scheduled task runs every 5 seconds to automatically expire and remove outdated book access
- **Fair Resource Distribution**: Maximum limit of 5 concurrent book access grants per user

### ⭐ Rating & Review System
- **Rating System**: 5-star ratings with average calculations and top-rated showcases
- **Comment System**: Users and librarians can leave timestamped comments on books

### 🔍 Search & Discovery
- **Advanced Search**: Filter by book name, author, description, and section with real-time filtering
- **Recommendations**: Top-rated books showcase and book popularity tracking

### 📊 Analytics & Statistics
- **Dashboard Analytics**: Track total books, sections, readers, requests, and active access
- **Visual Charts**: Interactive pie charts for book distribution and bar charts for top-rated books
- **User Statistics**: Personal reading history, completed books, and currently accessed books with remaining time

### 📄 PDF Reading
- **In-Browser Viewer**: Full-screen PDF access with text-to-speech functionality and access control

### 🔒 Security & Access Control
- **Role-Based Access Control (RBAC)**: Librarian-only and user-only routes with automatic role verification
- **Error Handling**: Custom error pages (403, 404, 500) with user-friendly messages
- **Data Validation**: Input sanitization, secure file uploads, SQL injection prevention, and XSS protection

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migrations
- **Flask-Login**: User session management
- **Flask-Bcrypt**: Password hashing
- **Flask-RESTful**: REST API development
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-APScheduler**: Task scheduling for automatic access expiration
- **Alembic**: Database migration tool

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **JavaScript (ES6+)**: Client-side interactivity
- **Chart.js**: Data visualization (bar charts)
- **Google Charts**: Data visualization (pie charts)
- **Font Awesome**: Icons
- **Jinja2**: Template engine

### Database
- **SQLite3**: Lightweight relational database

### Additional Libraries
- **Werkzeug**: WSGI utilities and file handling
- **python-dateutil**: Date/time utilities
- **pytz**: Timezone support

## 📁 Project Structure

```
Library-Management-Application/
│
├── application/              # Main application package
│   ├── __init__.py
│   ├── api.py                # RESTful API endpoints
│   ├── config.py             # Configuration settings
│   ├── controllers.py        # Route handlers and business logic
│   ├── database.py           # Database initialization
│   ├── functions.py          # Helper functions and utilities
│   ├── login.py              # Authentication and authorization
│   └── models.py             # SQLAlchemy database models
│
├── database/                 # Database files
│   └── database.sqlite3      # SQLite database
│
├── media/                    # Media storage
│   ├── pdfs/                 # PDF files
│   └── picture/              # Image files
│       ├── books/            # Book cover images
│       ├── profiles/         # User profile pictures
│       ├── sections/         # Section images
│       └── ...               # Other images
│
├── migrations/               # Database migrations
│   ├── alembic.ini
│   ├── env.py
│   └── versions/             # Migration scripts
│
├── static/                   # Static files
│   ├── script.js             # JavaScript files
│   └── style.css             # CSS styles
│
├── templates/                # Jinja2 templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   ├── user_home.html        # User dashboard
│   ├── librarian_home.html   # Librarian dashboard
│   ├── dashboard.html        # Dynamic dashboard
│   ├── book.html             # Book card component
│   ├── sections.html         # Section card component
│   ├── profile.html          # User profile page
│   ├── search.html           # Search results
│   ├── add_book.html         # Add book form
│   ├── add_section.html      # Add section form
│   ├── signup.html           # Registration page
│   ├── user_login.html       # User login
│   ├── librarian_login.html  # Librarian login
│   ├── 403.html              # Forbidden error page
│   ├── 404.html              # Not found error page
│   └── 500.html              # Server error page
│
├── app.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Library-Management-Application
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
The database will be automatically created when you first run the application. However, you can also run migrations:

```bash
# Initialize migration repository (if not already done)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Step 5: Create Librarian Account
When you first run the application, it will prompt you to create a librarian account in the terminal:
- Enter a username for the librarian
- Enter a password (input will be hidden)

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📖 Usage Guide

### For Librarians

1. **Login**: Navigate to the homepage and use the librarian login credentials
2. **Dashboard**: View library statistics, pending requests, and system overview
3. **Add Books**: 
   - Click "Add Book" 
   - Fill in book details (name, author, description)
   - Upload book cover image (optional)
   - Upload PDF file (optional)
   - Assign to a section (optional)
4. **Manage Sections**:
   - Create new sections
   - Edit section details
   - Add/remove books from sections
   - Delete sections
5. **Handle Requests**:
   - View all pending book requests
   - Grant or reject requests
   - Set access duration based on user request
6. **Manage Readers**:
   - View all registered readers
   - Revoke book access if needed
   - Delete reader accounts
7. **View Analytics**:
   - Check book distribution across sections
   - View top-rated books
   - Monitor library statistics

### For Users/Readers

1. **Sign Up**: Create a new account with username and password
2. **Login**: Use your credentials to access your dashboard
3. **Browse Books**:
   - View all available books
   - Browse by sections
   - Use search functionality
4. **Request Books**:
   - Click on a book you want to read
   - Select desired access duration
   - Submit request
5. **Read Books**:
   - Once access is granted, click on book cover to read PDF
   - Use full-screen mode for better reading experience
6. **Rate & Comment**:
   - Rate books (1-5 stars)
   - Leave comments and feedback
   - View other users' comments
7. **Manage Your Books**:
   - View currently accessed books
   - Return books early if needed
   - Track completed books
   - View reading statistics

---

<div align="center">

<🚀>Thank you</🚀>

</div>