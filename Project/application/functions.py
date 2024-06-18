from application.models import *
from flask import abort

from sqlalchemy.orm import aliased
from sqlalchemy import func
import random


####################################################### will shuffle list of comments #######################################################
def Random(list):
    random.shuffle(list)
    return list




####################################################### for deleting access automatically #######################################################
def delete_access():
    try:
        all_accesses = Access.query.all()
        for access in all_accesses:
            if access.end_time < datetime.now():
                print(f"Access id '{access.id}' of user '{access.accesser.username}' for book '{access.accessed_book.name}' is deleted from database.")
                db.session.delete(access)
                db.session.commit()
    except Exception as e:
        print(f"Error deleting accesses: {e}")




####################################################### for making 3 pair tuples of users #######################################################
def make_tuple(input_list):
    pairs_list = []
    for i in range(0, len(input_list) - 1, 2):
        pair = (input_list[i], input_list[i + 1])
        pairs_list.append(pair)

    remaining_elements = len(input_list) % 2
    if remaining_elements == 1:
        remaining_tuple = (input_list[-1],)
        pairs_list.append(remaining_tuple)
    return pairs_list





####################################################### for calculating average #######################################################
def calu_avg(book):
    avg = db.session.query(db.func.avg(Rate_Book.rate)).filter_by(book_id=book.id).scalar()
    if avg is None:
        avg = 0
    return round(avg,1)




####################################################### for checking book availability #######################################################
def book_availability(book_id,user_id):
    book = Books.query.filter_by(id=book_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if book is None or user is None:
        abort(404)
    if Access.query.filter_by(user_id=user_id, book_id=book_id).first():
        return True
    else:
        return False




####################################################### for checking request availability #######################################################
def request_exist(book_id,user_id):
    book = Books.query.filter_by(id=book_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if book is None or user is None:
        abort(404)
    if Request_Book.query.filter_by(user_id=user_id, book_id=book_id).first():
        return True
    else:
        return False
    




####################################################### for checking rate availability #######################################################
def can_rate(book_id,user_id):
    book = Books.query.filter_by(id=book_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if book is None or user is None:
        abort(404)
    if Rate_Book.query.filter_by(user_id=user_id, book_id=book_id).first():
        return False
    else:
        return True





####################################################### for showing time of entry creation #######################################################
def format_time_difference(start_time):
    if start_time:
        current_time = datetime.now()
        time_difference = current_time - start_time
        
        # Extract days, hours, minutes, seconds
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} ago"
        elif hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
        elif minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
        else:
            return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"
    return "time not found"
    




####################################################### for showing remaining time #######################################################
def remaining_time(reader_id,book_id):
    acs = Access.query.filter_by(user_id=reader_id, book_id=book_id).first()
    current_time = datetime.now()
    time_difference = acs.end_time -  current_time 

    # Extract days, hours, minutes, seconds
    days = time_difference.days
    seconds = time_difference.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days >= 7:
        weeks = days // 7
        return f"{weeks} {'week' if weeks == 1 else 'weeks'} left"
    elif 7 > days > 0:
        return f"{days} {'day' if days == 1 else 'days'} left"
    elif hours > 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'} left"
    elif minutes > 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} left"
    else:
        return f"{seconds} {'second' if seconds == 1 else 'seconds'} left"






##################################### for calculating notifications and librarains home page ##########################################
def calu_notification():
    try:
        requested = Request_Book.query.all()
        books = Books.query.all()
        sections = Sections.query.all()
        readers = Users.query.filter_by(label='user').all()
        accesses = Access.query.order_by(Access.book_id).all()
        dict = {'requested': requested, 'books': books, 'sections': sections, 'readers': readers,'accesses': accesses}
        return dict
    except: 
        pass





####################################################### for add/edit book form #######################################################
def all_sectionss():
    sections = db.session.query(Sections).all()
    return sections



 
####################################################### for add book to section #######################################################
def remaining_books():
    remaining_books = Books.query.filter_by(section_id = None).all()
    return remaining_books




########################################## for fetching top_10_books_sorted_by_avg_ratings from database ################################
def top_books():
    # books_with_avg_ratings = db.session.query(Books,func.avg(Rate_Book.rate).label('average_rating')).join(Rate_Book).group_by(Books.id).limit(10).all()
    # books = sorted(books_with_avg_ratings, key=lambda x: x.average_rating, reverse=True)
    books_alias = aliased(Books)
    top_10_books_sorted_by_avg_ratings = (
    db.session.query(
        books_alias,
        func.coalesce(func.avg(Rate_Book.rate), 0).label('average_rating')
    )
    .outerjoin(Rate_Book, books_alias.id == Rate_Book.book_id)
    .group_by(books_alias.id)
    .order_by(func.avg(Rate_Book.rate).desc())  # Order by average rating descending
    .limit(10)
    .all()
    )
    return top_10_books_sorted_by_avg_ratings