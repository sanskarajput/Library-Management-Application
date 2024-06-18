from application.login import *
from flask import  flash , render_template ,redirect ,url_for ,request, send_from_directory,g
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os 
import uuid,random
import getpass  # for hidden passwords in terminal

bcrypt = Bcrypt(app)

# add librarian if does't exist
def add_librarian():
    with app.app_context():
            db.create_all()
            if Users.query.filter_by(label="librarian").first() is None:
                username = input("Set your username to become a librarian : ")
                while Users.query.filter(func.lower(Users.username) == username.lower()).first():
                    username = input("( Username not available ) username to become a librarian : ")
                password = getpass.getpass("Set your password : ")
                user = Users(username=username, password=bcrypt.generate_password_hash(password),label = "librarian")
                db.session.add(user)
                db.session.commit()





# # # # # # # # # # # # # # # # # index page # # # # # # # # # # # # # # # # #
@app.route('/')
def index():
    logout_user()
    return render_template("index.html",page="index")





# # # # # # # # # # # # # # # # # # Signup user  # # # # # # # # # # # # # # # #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    logout_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_user = Users.query.filter(func.lower(Users.username) == username.lower()).first()
        if is_user is None:
            password = bcrypt.generate_password_hash(password)
            new_user = Users(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash(f"{username} Signup successfully !")
            return redirect(url_for('user_home'))
        else:
            flash(f"{username} username not available !")
            flash("Try another username !")
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html',page="Sign up")





# # # # # # # # # # # # # # # # # # Login user  # # # # # # # # # # # # # # # #
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    logout_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_user = Users.query.filter_by(username = username).first()
        if is_user:
            if bcrypt.check_password_hash(is_user.password,password):
                login_user(is_user)
                flash("Login successful !")
                return redirect(url_for('user_home'))
            else:
                flash("incorrect password!")
                return redirect(url_for('user_login'))
        else:
            flash("invalid username !")
            return redirect(url_for('user_login'))
    else:        
        return render_template("user_login.html",page="Login")





# # # # # # # # # # # # # # # # # # Login librarian # # # # # # # # # # # # # # # #
@app.route('/librarian_login', methods=['GET', 'POST'])
def librarian_login():
    logout_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        is_user = Users.query.filter_by(username = username).first()
        if is_user:
            if bcrypt.check_password_hash(is_user.password,password):
                login_user(is_user)
                flash("Login successful !")
                return redirect(url_for('librarian_home'))
            else:
                flash("incorrect password !")
                return redirect(url_for('librarian_login'))
        else:
            flash("invalid username !")
            return redirect(url_for('librarian_login'))
    else:
        return render_template('librarian_login.html',page = 'librarian login')





# # # # # # # # # # # # # # # # # # # # Logout # # # # # # # # # # # # # # # # # # # 
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are logged out !")
    return redirect(url_for('index'))





# # # # # # # # # # # # # # # # # # # # User Home # # # # # # # # # # # # # # # # # #
@app.route('/user_home')
@login_required
@role_required(['user'])
def user_home():
    return render_template("user_home.html",page="Home")





# # # # # # # # # # # # # # # # # # # # Librarian Home # # # # # # # # # # # # # # # #
@app.route('/librarian_home')
@login_required
@role_required(['librarian'])
def librarian_home():
    return render_template("librarian_home.html",page="Home")





# # # # # # # # # # # # # # # # # # # # # # Profile # # # # # # # # # # # # # # # # # #
@app.route('/profile')
@login_required
def profile():
    user = Users.query.get_or_404(current_user.id)
    return render_template("profile.html",user=user,page="",book_availability=book_availability)





# # # # # # # # # # # # # # # # # upload_profile_picture # # # # # # # # # # # # # # # #
@app.route('/upload_profile_picture' ,methods=['POST'])
@login_required
@role_required(['user','librarian'])
def upload_profile_picture():
    user = Users.query.get_or_404(current_user.id)
    if request.method == "POST":
        new_picture_file = request.files.get('picture')

        if new_picture_file:
            pre_picture_file = user.profile_path

            if pre_picture_file != "default_profile.jpg":
                picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], pre_picture_file)
                if os.path.exists(picture_full_path):
                    os.remove(picture_full_path)

            picture_path = secure_filename(new_picture_file.filename)
            picture_path = str(uuid.uuid1()) + "_" + picture_path
            picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], picture_path)
            new_picture_file.save(picture_full_path)
            user.profile_path = picture_path
            db.session.commit()
    return redirect(url_for('profile'))





# # # # # # # # # # # # # # # # # confirm_delete_profile # # # # # # # # # # # # # # # #
@app.route('/confirm_delete_profile')
@login_required
@role_required(['user'])
def delete_profile():
    user = Users.query.get(current_user.id)
    picture_path = user.profile_path
    if picture_path != "default_profile.jpg":
        picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], picture_path)
        if os.path.exists(picture_full_path):
            os.remove(picture_full_path)
    logout_user() 
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))





# # # # # # # # # # # # # # # # # delete_reader # # # # # # # # # # # # # # # #
@app.route('/delete_reader/<int:id>')
@login_required
@role_required(['librarian'])
def delete_reader(id):
    user = Users.query.get_or_404(id)
    picture_path = user.profile_path
    if picture_path != "default_profile.jpg":
        picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], picture_path)
        if os.path.exists(picture_full_path):
            os.remove(picture_full_path)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('all_readers'))









###########################################################################
############################### CRUD on Books #############################
###########################################################################



# # # # # # # # # # # # # # # # # Create book # # # # # # # # # # # # # # # #
@app.route('/add_book', methods=['GET','POST'])
@login_required
@role_required(['librarian'])
def add_book():
    if request.method == "POST":
        name = request.form['name']
        author = request.form['author']
        description = request.form['description']
        image_file = request.files.get('image')
        pdf_file = request.files.get('pdf')
        section = request.form.get('section')
        book = Books.query.filter_by(name = name).first()

        if book is None:
            new_book = Books(name=name, author=author, description=description)
            db.session.add(new_book)
            db.session.commit()
            if image_file:
                picture_path = secure_filename(image_file.filename)
                picture_path = str(uuid.uuid1()) + "_" + picture_path
                image_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path))
                new_book.image_path =  picture_path
                db.session.commit()

            if pdf_file:
                pdf_path = secure_filename(pdf_file.filename) 
                pdf_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)) 
                new_book.pdf_path =  pdf_path
                db.session.commit()

            if section:
                new_book.section_id = section
                db.session.commit()
            
            return redirect(url_for('librarian_home'))
        else:
            flash("Book already exists!")
            return redirect(url_for('add_book'))
    return render_template("add_book.html", page="Add Book")





# # # # # # # # # # # # # # # # # Read book # # # # # # # # # # # # # # # # #
# not required

# # # # # # # # # # # # # # # # # Edit book # # # # # # # # # # # # # # # # #
@app.route('/edit_book/<int:id>', methods=['POST'])
@login_required
@role_required(['librarian'])
def edit_book(id):
    book = Books.query.filter_by(id = id).first()
    name = request.form.get('name')
    author = request.form.get('author')
    description = request.form.get('description')
    new_image_file = request.files.get('image')
    new_pdf_file = request.files.get('pdf')
    section = request.form.get('section')
    name_exist = Books.query.filter_by(name = name).all()

    if len(name_exist) < 1 or name_exist[0].id == id:
        if name:
            book.name = name

        if author:
            book.author = author
        
        if description:
            book.description = description

        if section=="none":
            book.section_id = None
        elif section:
            book.section_id = section


        if new_image_file:
            pre_picture_file = book.image_path
            if pre_picture_file != "default_book.jpg":
                picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], pre_picture_file)
                if os.path.exists(picture_full_path):
                    os.remove(picture_full_path)

            picture_path = secure_filename( new_image_file.filename )
            picture_path = str(uuid.uuid1()) + "_" + picture_path
            new_image_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path))
            book.image_path = picture_path
        
        if new_pdf_file:
            pre_pdf_file = book.pdf_path
            if pre_pdf_file != "default.pdf":
                pre_pdf_file = os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pre_pdf_file)
                if os.path.exists(pre_pdf_file):
                    os.remove(pre_pdf_file)
            pdf_path = secure_filename( new_pdf_file.filename ) 
            new_pdf_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)) 
            book.pdf_path = pdf_path
        
        db.session.commit()
        return redirect(url_for('librarian_home'))
    flash("Choose another book name....")
    return redirect(url_for('librarian_home'))





# # # # # # # # # # # # # # # # # Delete book # # # # # # # # # # # # # # # #
@app.route('/delete_book/<int:id>')
@login_required
@role_required(['librarian'])
def delete_book(id):
    book = Books.query.filter_by(id = id).first_or_404()
    picture_path = book.image_path  
    if picture_path != "default_book.jpg":
        picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path)
        if os.path.exists(picture_full_path):
            os.remove(picture_full_path)
    pdf_path = book.pdf_path
    if pdf_path!= "default.pdf":
        pdf_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)
        if os.path.exists(pdf_full_path):
            os.remove(pdf_full_path)
    db.session.delete(book)
    db.session.commit()
    flash("book deleted successfully !!")
    return redirect(url_for('librarian_home'))





# # # # # # # # # # # # # # # # # Rate book # # # # # # # # # # # # # # # #
@app.route('/rate/<int:book_id>/<int:rate>')
@login_required
@role_required(['user'])
def rate(book_id,rate):
    book = Books.query.filter_by(id = book_id).first_or_404()
    entry = Rate_Book.query.filter_by(user_id = current_user.id, book_id=book_id).first()
    if entry is None: 
        new_rating = Rate_Book(user_id = current_user.id, book_id = book.id, rate = rate)
        db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for('user_home'))
    flash("Already rated !!")
    return redirect(url_for('user_home'))    





# # # # # # # # # # # # # # # # # Comment on book # # # # # # # # # # # # # # # #
@app.route('/comment/<int:book_id>', methods=['POST'])
@login_required
@role_required(['user','librarian'])
def comment(book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    comment = request.form.get('comment')
    new_comment = Comment_Book(comment = comment,user_id = current_user.id, book_id = book.id)
    db.session.add(new_comment)
    db.session.commit()
    if current_user.label == 'librarian':
        return redirect(url_for('librarian_home'))
    return redirect(url_for('user_home'))












###########################################################################
############################### CRUD on Sections ##########################
###########################################################################



# # # # # # # # # # # # # # # # # Create Section # # # # # # # # # # # # # # # #
@app.route('/add_section', methods=['GET','POST'])
@login_required
@role_required(['librarian'])
def add_section():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        image_file = request.files.get('image')

        section = Sections.query.filter_by(name = name).first()
        if section is None:
            new_section = Sections(name=name, description= description)
            db.session.add(new_section)
            db.session.commit()

            if image_file:
                picture_path = secure_filename( image_file.filename )
                picture_path = str(uuid.uuid1()) + "_" + picture_path
                image_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], picture_path))
                new_section.image_path =  picture_path
                db.session.commit()

            return redirect(url_for('librarian_home'))
        else:
            flash("Section already exists!")
            return redirect(url_for('add_section'))

    return render_template("add_section.html",page="Add Section")





# # # # # # # # # # # # # # # # # Read Section # # # # # # # # # # # # # # # # #
@app.route('/section/<int:id>')
@login_required
@role_required(['librarian','user'])
def section(id):
    section = Sections.query.filter_by(id = id).first_or_404()
    return render_template("showSection.html",section=section,page="Section")





# # # # # # # # # # # # # # # # # Edit Section # # # # # # # # # # # # # # # # #
@app.route('/edit_section/<int:id>' , methods=['POST'])
@login_required
@role_required(['librarian'])
def edit_section(id):
    section = Sections.query.filter_by(id = id).first_or_404()
    name = request.form.get('name')
    description = request.form.get('description')
    new_image_file = request.files.get('image')
    name_exist = Sections.query.filter_by(name = name).all()

    if len(name_exist) < 1 or name_exist[0].id == id:
        if name:
            section.name = name

        if description:
            section.description = description

        if new_image_file:
            pre_picture_file = section.image_path

            if pre_picture_file != "default_section.jpg":
                picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], pre_picture_file)
                if os.path.exists(picture_full_path):
                    os.remove(picture_full_path)

            picture_path = secure_filename( new_image_file.filename )
            picture_path = str(uuid.uuid1()) + "_" + picture_path
            new_image_file.save(os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], picture_path))
            section.image_path = picture_path
        
        db.session.commit()
        flash("Edit successfully !!")
        return redirect(url_for('section',id=section.id))
    flash("Choose another section name....")
    return redirect(url_for('section',id=section.id))





# # # # # # # # # # # # # # # # # Delete Section # # # # # # # # # # # # # # # # #
@app.route('/delete_section/<int:id>')
@login_required
@role_required(['librarian'])
def delete_section(id):
    section = Sections.query.filter_by(id = id).first_or_404()
    books = section.books
    picture_path = section.image_path
    if picture_path!= "default_section.jpg":
        picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], picture_path)
        if os.path.exists(picture_full_path):
            os.remove(picture_full_path)
    db.session.delete(section)
    db.session.commit()
    for book in books:
        book = Books.query.filter_by(id = book.id).first_or_404()
        picture_path = book.image_path  
        if picture_path != "default_book.jpg":
            picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path)
            if os.path.exists(picture_full_path):
                os.remove(picture_full_path)
        pdf_path = book.pdf_path
        if pdf_path!= "default.pdf":
            pdf_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)
            if os.path.exists(pdf_full_path):
                os.remove(pdf_full_path)
        db.session.delete(book)
        db.session.commit()
    flash("Section deleted successfully with all the books...")
    return redirect(url_for('librarian_home'))





# # # # # # # # # # # # # # # # # Add Book to section # # # # # # # # # # # # # # # #
@app.route('/addbooktosection/<int:id>', methods=['POST'])
@login_required
@role_required(['librarian'])
def addbooktosection(id):
    section = Sections.query.filter_by(id = id).first_or_404()
    all_books = request.form.getlist('books')
    if len(all_books) != 0:
        for book_id in all_books:
            book = Books.query.filter_by(id = book_id).first()
            if book:
                if book.section_id == section.id:
                    flash(f"Book {book.name} is already in {section.name} section . .")
                    return redirect(url_for('section',id=section.id))
                elif book.section_id != None:
                    flash(f"Book {book.name} is already added in any section by another librarian . .")
                    return redirect(url_for('section',id=section.id))
                else: 
                    book.section_id = section.id
            else:
                flash(f"Any book is deleted by another librarian...")
                return redirect(url_for('section',id=section.id))
        db.session.commit()
        flash("Books added successfully !")
        return redirect(url_for('section',id=section.id))
    flash("Select Atleast one book..")
    return redirect(url_for('section',id=section.id))





# # # # # # # # # # # # # # # Remove Book from Section # # # # # # # # # # # # # # # # #
@app.route('/removebookfromsection/<int:book_id>')
@login_required
@role_required(['librarian'])
def removebookfromsection(book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    section_id = book.section_id
    section = Sections.query.filter_by(id = section_id).first_or_404()
    book.section_id = None
    db.session.commit()
    return redirect(url_for('section',id=section.id))





# # # # # # # # # # # # # # # # # # # # Request Book # # # # # # # # # # # # # # # # # # #
@app.route('/request_book/<int:book_id>',methods=['POST'])
@login_required
@role_required(['user'])
def request_book(book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    requested_book = Request_Book.query.filter_by(user_id = current_user.id, book_id = book_id).first()
    access = Access.query.filter_by(user_id = current_user.id, book_id = book_id).first()

    duration = request.form.get('duration')
    if access is None:
        if Access.query.filter_by(user_id = current_user.id).count() < 5:
            if requested_book is None:
                new_request = Request_Book(user_id = current_user.id, book_id = book_id, duration = duration)
                db.session.add(new_request)
                db.session.commit()
                return redirect(url_for('user_home'))
            flash("Request already exists!")
            return redirect(url_for('user_home'))
        flash("We can not granted more than 5 books !")
        flash("So don't try to request more books.")
        return redirect(url_for('user_home'))
    flash("You already have Access...")
    return redirect(url_for('user_home'))





# # # # # # # # # # # # # # # # # # # # Return Book # # # # # # # # # # # # # # # # # # # #
@app.route('/return_book/<int:book_id>')
@login_required
@role_required(['user'])
def return_book(book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    user = Users.query.filter_by(id = current_user.id).first_or_404()
    access = Access.query.filter_by(user_id = current_user.id, book_id = book_id).first()
    if access:
        db.session.delete(access)
        if Completed.query.filter_by(user_id = user.id, book_id=book.id).first() is None:
            completed = Completed(book_id=book.id,user_id=user.id)
            db.session.add(completed)
        db.session.commit()
        flash("book returned successfully !")
        return redirect(url_for('my_books'))
    else:
        flash("Access does not exist!")
        return redirect(url_for('user_home'))





# # # # # # # # # # # # # # # # # # # # Revoke Book from User # # # # # # # # # # # # # # # #
@app.route('/revoke/<int:user_id>/<int:book_id>')
@login_required
@role_required(['user','librarian'])
def revoke(user_id,book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    user = Users.query.filter_by(id = user_id).first_or_404()
    access = Access.query.filter_by(user_id = user_id, book_id = book_id).first()
    if access:
        db.session.delete(access)
        db.session.commit()
        flash("Access revoked successfully!")
        return redirect(url_for('accesses'))
    else:
        flash("Access does not exist!")
        return redirect(url_for('all_readers'))





# # # # # # # # # # # # # # # # # # # # Grant Book # # # # # # # # # # # # # # # # # # # #
@app.route('/grant/<int:user_id>/<int:book_id>')
@login_required
@role_required(['librarian'])
def grant(user_id,book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    user = Users.query.filter_by(id = user_id).first_or_404()
    access = Access.query.filter_by(user_id = user_id, book_id = book_id).first()
    requested_book = Request_Book.query.filter_by(user_id = user_id, book_id = book_id).first()
    duration = requested_book.duration

    if Access.query.filter_by(user_id = user_id).count() < 5:
        if access is None:
            new_access = Access(user_id = user_id, book_id = book_id)
            db.session.add(new_access)
            book.increment()

            if requested_book:
                db.session.delete(requested_book)
            db.session.commit() 

            if duration == "6 hour":
                new_access.for_6_hour()
            elif duration == "12 hour":
                new_access.for_12_hour()
            elif duration == "1 day":
                new_access.for_1_day()
            elif duration == "2 day":
                new_access.for_2_day()
            elif duration == "4 day":
                new_access.for_4_day()
            elif duration == "1 week":
                new_access.for_1_week()
            elif duration == "2 week":
                new_access.for_2_week()

            flash('Access granted successfully !')
            return redirect(url_for('requests'))
        else:
            flash("Already haved Access !")
            return redirect(url_for('requests'))
    else:
        flash("Can't granted more than 5 books !")
        return redirect(url_for('requests'))






# # # # # # # # # # # # # # # # # # # # Reject Request # # # # # # # # # # # # # # # # # #
@app.route('/reject/<int:user_id>/<int:book_id>')
@login_required
@role_required(['librarian'])
def reject(user_id,book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    user = Users.query.filter_by(id = user_id).first_or_404()
    requested_book = Request_Book.query.filter_by(user_id = user_id, book_id = book_id).first()

    new_rejection = Reject(user_id=requested_book.user_id, book_id=requested_book.book_id, duration=requested_book.duration)
    db.session.add(new_rejection)
    db.session.commit()

    if requested_book:
        db.session.delete(requested_book)
        db.session.commit() 

    flash('Request Rejected !')
    return redirect(url_for('requests'))





# # # # # # # # # # # # # # # # # Remove from Completed # # # # # # # # # # # # # # # # # # #
@app.route('/rmCompleted/<int:book_id>')
@login_required
@role_required(['user'])
def rmCompleted(book_id):
    book = Books.query.filter_by(id = book_id).first_or_404()
    user = Users.query.filter_by(id = current_user.id).first_or_404()
    access = Completed.query.filter_by(user_id = current_user.id, book_id = book_id).first()
    if access:
        db.session.delete(access)
        db.session.commit()
        flash(f"Book {book.name} Removed successfully from your Completed Books list !")
        return redirect(url_for('stats'))
    else:
        flash("Completion does not exist!")
        return redirect(url_for('stats'))






# # # # # # # # # # # # # # # # # mybooks # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/mybooks')
@login_required
@role_required(['user'])
def my_books():
    return render_template('dashboard.html', page="My Books")





# # # # # # # # # # # # # # # # # allbooks # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/allbooks')
@login_required
@role_required(['librarian','user'])
def all_books():
    books = Books.query.all()
    # random.shuffle(books)
    return render_template('dashboard.html', books=books , page="All Books")





# # # # # # # # # # # # # # # # # allsections # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/allsections')
@login_required
@role_required(['librarian','user'])
def all_sections():
    sections = Sections.query.all()
    # random.shuffle(sections)
    return render_template('dashboard.html', sections=sections, page="All Sections")





# # # # # # # # # # # # # # # # # stats # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/stats')
@login_required
@role_required(['librarian','user'])
def stats():
    books_issued = db.session.query(Books.name, Books.issued).order_by(Books.issued.desc()).all()
    bookname = []
    issued = []
    for book in books_issued:
        bookname.append(book[0])
        issued.append(book[1])

    books_with_avg_rating = (db.session.query(Books.name,func.coalesce(func.avg(Rate_Book.rate), 0).label('average_rating')).outerjoin(Rate_Book).group_by(Books.id).all())
    
    book_name = []
    average_rating = []
    for book in books_with_avg_rating:
        book_name.append(book[0])
        average_rating.append(book[1])
    return render_template("dashboard.html",
                           bookname=bookname,
                           issued=issued,
                           book_name=book_name,
                           average_rating=average_rating,
                           page="Statistics")





# # # # # # # # # # # # # # # # # readers # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/readers')
@login_required
@role_required(['librarian'])
def all_readers():
    readers = Users.query.filter_by(label='user').all()
    random.shuffle(readers)
    return render_template('dashboard.html', readers=readers, page="All Readers")





# # # # # # # # # # # # # # # # # requests # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/requests')
@login_required
@role_required(['librarian'])
def requests():
    requests = Request_Book.query.all()
    random.shuffle(requests)
    return render_template("dashboard.html", requests=requests, page="All Requests")




# # # # # # # # # # # # # # # # # accesses # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard/accesses')
@login_required
@role_required(['librarian'])
def accesses():
    accesses = Access.query.group_by(Access.book_id).all()
    return render_template("dashboard.html", accesses=accesses, page="All Accesses")





# # # # # # # # # # # # # # # # # remove on rejection of request # # # # # # # # # # # # # # # # # 
@app.route('/rm-rejected/<int:id>')
@login_required
@role_required(['user'])
def rm_rejected(id):
    rejection = Reject.query.filter_by(id = id).first_or_404()
    db.session.delete(rejection)
    db.session.commit()
    return redirect(url_for('user_home'))





# # # # # # # # # # # # # # # # # remove all rejections of request # # # # # # # # # # # # # # # #
@app.route('/rm-all-rejected')
@login_required
@role_required(['user'])
def rm_all_rejected():
    all_rejections = Reject.query.filter_by(user_id=current_user.id).all()
    for rejection in all_rejections:
        db.session.delete(rejection)
    db.session.commit()
    return redirect(url_for('user_home'))






# # # # # # # # # # # # # # # # # remove request by book id # # # # # # # # # # # # # # # # # # #
@app.route('/rm-requestBybookid/<int:id>')
@login_required
@role_required(['user'])
def rm_requestBybookid(id):
    request = Request_Book.query.filter_by(book_id = id,user_id=current_user.id).first_or_404()
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('user_home'))




# # # # # # # # # # # # # # # # # remove one request # # # # # # # # # # # # # # # # # # #
@app.route('/rm-request/<int:id>')
@login_required
@role_required(['user'])
def rm_request(id):
    request = Request_Book.query.filter_by(id = id).first_or_404()
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('user_home'))






# # # # # # # # # # # # # # # # # remove all requests # # # # # # # # # # # # # # # # # # #
@app.route('/rm-all-requests')
@login_required
@role_required(['user'])
def rm_all_requests():
    all_requests = Request_Book.query.filter_by(user_id=current_user.id).all()
    for reqst in all_requests:
        db.session.delete(reqst)
    db.session.commit()
    return redirect(url_for('user_home'))





# # # # # # # # # # # # # # # # # search # # # # # # # # # # # # # # # # # # #
@app.route('/search',methods=['GET'])
@login_required
def search():
    query = request.args.get('query')

    all_books = set()
    books_on_name = Books.query.filter(Books.name.like(f"%{query}%")).all()
    all_books.update(books_on_name)
    if len(all_books) < 5:
        books_on_author = Books.query.filter(Books.author.like(f"%{query}%")).limit(5-len(all_books)).all()
        all_books.update(books_on_author)
        if len(all_books) < 5:
            books_on_description = Books.query.filter(Books.description.like(f"%{query}%")).limit(5-len(all_books)).all()
            all_books.update(books_on_description)

    all_sections = set()
    sections_on_name = Sections.query.filter(Sections.name.like(f"%{query}%")).all()
    all_sections.update(sections_on_name)
    if len(all_sections) < 5:
        sections_on_description = Sections.query.filter(Sections.description.like(f"%{query}%")).limit(5-len(all_sections)).all()
        all_sections.update(sections_on_description)

    return render_template('search.html', all_books=all_books, all_sections=all_sections, query=query,page='Search')







# # # # # # # # # # # # # # # # # Sending files # # # # # # # # # # # # # # # # # # #
@app.route('/display/<picture_path>')
def display(picture_path):
    picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["OTHER"], picture_path)
    if os.path.exists(picture_full_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["OTHER"], picture_path)
    return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["OTHER"], "background.jpg")

@app.route('/display_book/<picture_path>')
def display_book(picture_path):
    picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path)
    if os.path.exists(picture_full_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], picture_path)
    return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["BOOK"], "default_book.jpg")

@app.route('/display_section/<picture_path>')
def display_section(picture_path):
    picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], picture_path)
    if os.path.exists(picture_full_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], picture_path)
    return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["SECTION"], "default_section.jpg")

@app.route('/display_profile/<picture_path>')
def display_profile(picture_path):
    picture_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], picture_path)
    if os.path.exists(picture_full_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], picture_path)
    return send_from_directory(app.config["UPLOAD_FOLDER"]["PICTURE"]["PROFILE"], "default_profile.jpg")

@app.route('/send/<pdf_path>')
@login_required
def send(pdf_path):
    pdf_full_path = os.path.join(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)
    if os.path.exists(pdf_full_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"]["PDF"], pdf_path)
    return send_from_directory(app.config["UPLOAD_FOLDER"]["PDF"], "default.pdf")




# # # # # # # # # # # # # # # # # errors # # # # # # # # # # # # # # # # # # #
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html",page="error"), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template("500.html",page="error"), 500

@app.errorhandler(403)
def forbidden_error(e):
	return render_template("403.html",page="error"), 403

