from application.database import db
from flask_login import UserMixin, LoginManager, login_user, login_required ,logout_user ,current_user
from datetime import datetime , timedelta




class Users(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False, unique=True)
    time = db.Column(db.DateTime, default=datetime.now)
    profile_path = db.Column(db.String(250), default="default_profile.jpg")
    label = db.Column(db.String, default='user')

    comments = db.relationship("Comment_Book", backref="commenter" ,cascade="all, delete")
    rates = db.relationship("Rate_Book",cascade="all, delete")

    granted = db.relationship("Books",secondary="access",backref="granters")
    completed_books = db.relationship("Books",secondary="completed",backref="completers")
    requested = db.relationship("Books",secondary="request_book",backref="requesters")

    access = db.relationship("Access",back_populates="accesser",cascade="all, delete",lazy=True,overlaps="granters,granted")
    requests = db.relationship("Request_Book",back_populates="requester",cascade="all, delete",lazy=True,overlaps="requested,requesters")

    rejected_request_books  = db.relationship("Books",secondary="reject",backref="rejected_users")
    rejected_requests  = db.relationship("Reject",back_populates="rejected_user",cascade="all, delete",lazy=True,overlaps="rejected_request_books,rejected_users")

    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_id(self):
        return int(self.id)
    

class Sections(db.Model):
    __tablename__='sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    time = db.Column(db.DateTime, default=datetime.now)
    image_path = db.Column(db.String(250), default="default_section.jpg")
    description = db.Column(db.Text)

    books = db.relationship("Books", backref="from_section",lazy=True)

    def __repr__(self):
        return f'<Section {self.name}>'


class Books(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    author = db.Column(db.String(50), nullable=False)
    pdf_path = db.Column(db.String(250), default="default.pdf")
    time = db.Column(db.DateTime, default=datetime.now)
    image_path = db.Column(db.String(250), default="default_book.jpg")
    description = db.Column(db.Text)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), default=None)
    issued = db.Column(db.Integer,default=0)
        
    ratings = db.relationship("Rate_Book" ,cascade="all, delete")
    comments = db.relationship("Comment_Book",cascade="all, delete")

    access = db.relationship("Access",back_populates="accessed_book",cascade="all, delete" ,lazy=True,overlaps="granters,granted")
    request = db.relationship("Request_Book",back_populates="requested_book",cascade="all, delete",lazy=True,overlaps="requested,requesters")
    completed = db.relationship("Completed",back_populates="completed_book",cascade="all, delete",lazy=True,overlaps="completed_books,completers")

    rejected_request  = db.relationship("Reject",back_populates="rejected_book",cascade="all, delete",lazy=True,overlaps="rejected_request_books,rejected_users")

    def __repr__(self):
        return f'<Book {self.name}>'
    
    def increment(self):
        self.issued += 1
        db.session.commit()


class Request_Book(db.Model):
    __tablename__='request_book'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    duration = db.Column(db.String) 

    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique'),)
    __mapper_args__ = {'confirm_deleted_rows': False}
    requester = db.relationship("Users",back_populates="requests",overlaps="requested,requesters")
    requested_book = db.relationship("Books",back_populates="request",overlaps="requested,requesters")

    def __repr__(self):
        return f'<Request_Book {self.user_id}>'
  

class Access(db.Model):
    __tablename__='access'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique'),)
    __mapper_args__ = {'confirm_deleted_rows': False}
    accesser = db.relationship("Users",back_populates="access",overlaps="granters,granted")
    accessed_book = db.relationship("Books",back_populates="access",overlaps="granters,granted")




    def for_6_hour(self):
        self.end_time = self.start_time + timedelta(hours=6)
        db.session.commit()

    def for_12_hour(self):
        self.end_time = self.start_time + timedelta(hours=12)
        db.session.commit()

    def for_1_day(self):
        self.end_time = self.start_time + timedelta(days=1)
        db.session.commit()

    def for_2_day(self):
        self.end_time = self.start_time + timedelta(days=2)
        db.session.commit()

    def for_4_day(self):
        self.end_time = self.start_time + timedelta(days=4)
        db.session.commit()

    def for_1_week(self):
        self.end_time = self.start_time + timedelta(weeks=1)
        db.session.commit()

    def for_2_week(self):
        self.end_time = self.start_time + timedelta(weeks=2)
        db.session.commit()


class Completed(db.Model):
    __tablename__='completed'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique'),)
    __mapper_args__ = {'confirm_deleted_rows': False}
    completed_book = db.relationship("Books",back_populates="completed",overlaps="completed_books,completers")

    def __repr__(self):
        return f'<Completed {self.id}>'


class Rate_Book(db.Model):
    __tablename__ = 'rate_book'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") ,  primary_key=True )
    book_id = db.Column(db.Integer, db.ForeignKey("books.id") ,  primary_key=True )
    rate = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.CheckConstraint('rate >= 1 AND rate <= 5', name='check_rate_range'),)

    def __repr__(self):
        return f"<Rate_Book {self.rate}>"


class Comment_Book(db.Model):
    __tablename__ = 'comment_book'
    comment_id =  db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)


    def __repr__(self):
        return f"<Comment_Book {self.comment_id}>"
    

class Reject(db.Model):
    __tablename__='reject'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    duration = db.Column(db.String) 
    time = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique'),)
    __mapper_args__ = {'confirm_deleted_rows': False}
    rejected_user  = db.relationship("Users",back_populates="rejected_requests",overlaps="rejected_request_books,rejected_users")
    rejected_book  = db.relationship("Books",back_populates="rejected_request",overlaps="rejected_request_books,rejected_users")


    def __repr__(self):
        return f'<Reject {self.id}>'
