# 📚 Library Management System

A full-stack web application designed to streamline library operations and enhance the reading experience. Built as a college project, this system demonstrates practical implementation of web development concepts while solving real-world library management challenges.

## 🎯 Project Overview

This Library Management System is a **server-side rendered web application** developed using Flask, offering a complete solution for managing library resources, user interactions, and administrative tasks. The application follows the traditional Model-View-Controller (MVC) architecture, where all pages are dynamically rendered on the server using Jinja2 templates, providing a seamless and interactive experience.

**Developed as part of academic coursework**, this project showcases the integration of modern web technologies, database management, and user-centric design principles to create a practical library management solution.

### Why This Project?

Libraries are fundamental to education and knowledge sharing, yet managing them efficiently can be challenging. This application was created to:

- Simplify book cataloging and organization for librarians
- Provide readers with easy access to library resources
- Automate routine tasks like request handling and access expiration
- Offer insights through analytics and statistics
- Demonstrate full-stack development capabilities in an academic setting

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
git clone https://github.com/sanskarajput/Library-Management-Application
cd Library-Management-Application
```


### Step 2: Create Virtual Environment (Recommended but Optional)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
```


### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup (Optional)

> **Skip this step if you already have an existing database configured.**

The database is automatically created on first run.
If you want to set up a **fresh database** or manage migrations manually, run:

```bash
# Initialize migration repository (if not already done)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Step 5: Create Librarian Account (Optional)

> **Required only for first-time setup with a new database.**

On the first run, the application will prompt you in the terminal to create a librarian account:

```
>>> Database Already Exists. Want to setup a new database ? (y/N): n
>>> Librarian Already Exists. Want to setup a new librarian ? (y/N): y
>>> Set your username to become a librarian : admin
>>> Set your password : 
```

If you’re using an **existing database**, this step is **not required**.

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at:
👉 `http://localhost:5000`

## 📱 Using the Application

### For Librarians
1. Login with your credentials → Access the admin dashboard
2. Create sections to organize your library (Fiction, Science, etc.)
3. Add books with details, cover images, and PDF files
4. Review pending requests → Approve/reject with access duration
5. Monitor analytics and manage user accounts

### For Readers
1. Sign up and create your account
2. Browse books by section or search by title/author
3. Request books with your preferred reading duration
4. Once approved, read PDFs directly in your browser
5. Rate and comment on books you've read

## 🔒 Security Features

- **Password Protection**: Bcrypt hashing for secure credential storage
- **Role-Based Access Control**: Separate interfaces and permissions for librarians and readers
- **Session Management**: Secure user sessions with Flask-Login
- **Input Validation**: Protection against SQL injection and XSS attacks
- **File Upload Security**: Validated and sanitized file uploads
- **Error Handling**: Graceful error pages that don't expose sensitive information

## 🎓 Academic Context

This project was developed as part of college coursework to demonstrate:

- Full-stack web development proficiency
- Database design and management
- User authentication and authorization
- Server-side rendering with Flask and Jinja2
- RESTful API development
- Responsive web design principles
- Practical application of software engineering concepts

The project emphasizes clean code, proper documentation, and real-world applicability while maintaining academic rigor.

## 🔄 Server-Side Rendering Approach

Unlike modern single-page applications (SPAs), this project utilizes **traditional server-side rendering** where:

- Pages are fully rendered on the server using Jinja2 templates
- HTML is sent to the client as complete documents
- Reduces client-side JavaScript complexity
- Provides better initial load times and SEO benefits
- Demonstrates fundamental web development principles

---

<div align="center">

**Built with dedication as a learning journey in web development** 📖✨

*Questions or feedback? Feel free to reach out!*

</div>
