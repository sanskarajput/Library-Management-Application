from flask_restful import Api , reqparse , Resource ,fields,marshal_with, marshal
from werkzeug.exceptions import HTTPException
from flask import make_response
import json
from application.functions import *
from flask_cors import CORS
from flask import current_app as app

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class CorrectResponse(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class BadRequest(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {
            "error_code": error_code,
            "error_message": error_message
            }
        self.response = make_response(json.dumps(message), status_code)

class AlreadyExixt(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)



api = Api(app)
cors = CORS(app)


###########################################################################
############################## api for Books ##############################
###########################################################################

parser_book = reqparse.RequestParser()
parser_book.add_argument("name",default=None)
parser_book.add_argument("author",default=None)
parser_book.add_argument("description",default=None)

comment_fields = {
    "comment_id": fields.Integer,
    "comment": fields.String,
    "time": fields.DateTime
    }

out_book = {
    "id": fields.Integer,
    "name": fields.String,
    "author": fields.String,
    "description": fields.String,
    "image_path": fields.String,
    "pdf_path": fields.String,
    "section_id": fields.Integer,
    "issued": fields.Integer,
    "time": fields.DateTime,
    "ratings": fields.Float(attribute=lambda book:calu_avg(book)),
    "comments": fields.Raw(attribute=lambda book: {str(book.comments.index(cmt)+1): marshal(cmt, comment_fields) for cmt in book.comments})
}

class Books_api(Resource):
    @marshal_with(out_book)
    def get(self,id):
        book = Books.query.filter_by(id = id).first()
        if book:
            return book
        else:
            raise NotFoundError(status_code=404)
    
    def post(self):
        args = parser_book.parse_args()
        if args["name"] is None or args["name"]=="":
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book Name is required")
            
        if args["author"] is None or args["author"]=="":
            raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book author is required")
        
        if args["description"] is None:
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book description is required")
    
        if Books.query.filter_by(name=args['name']).count() == 0:
            book = Books(name = args['name'], author = args['author'], description = args['description'])
            db.session.add(book)
            db.session.commit()
            book = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
            "image_path": book.image_path,
            "pdf_path": book.pdf_path,
            }
            return book
        
        else:
            raise AlreadyExixt(status_code=409)
        
    def put(self,id):
        book = Books.query.filter_by(id = id).first()
        if book:
            args = parser_book.parse_args()
            if args["name"] is None or args["name"]=="":
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book Name is required")
            
            if args["author"] is None or args["author"]=="":
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book author is required")
            
            if args["description"] is None:
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Book description is required")

            book.name = args['name']
            book.author = args['author']
            book.description = args['description']
            db.session.commit()
            book = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
            "image_path": book.image_path,
            "pdf_path": book.pdf_path,
            }
            return book
        else:
            raise NotFoundError(status_code=404)
        
    def delete(self,id):
        book = Books.query.filter_by(id = id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            raise CorrectResponse(status_code=200)
        else:
            raise NotFoundError(status_code=404)
         



###########################################################################
############################ api for Sections #############################
###########################################################################

parser_section = reqparse.RequestParser()
parser_section.add_argument("name",default=None)
parser_section.add_argument("description",default=None)


out_section = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "image_path": fields.String,
    "books": fields.Raw(attribute=lambda section: {str(section.books.index(book)+1): marshal(book, out_book) for book in section.books}),
}

class Sections_api(Resource):
    @marshal_with(out_section)
    def get(self, id):
        section = Sections.query.filter_by(id=id).first()
        if section:
            return section
        else:
            raise NotFoundError(status_code=404)
          
    def post(self):
        args = parser_section.parse_args()
        if args["name"] is None or  args["name"] =="":
            raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Section Name is required")
        
        if args["description"] is None:
            raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Section description is required")
        
        if Sections.query.filter_by(name=args['name']).count() == 0:
            section = Sections(name = args['name'], description = args['description'])
            db.session.add(section)
            db.session.commit()
            section_with_books = {
                "id": section.id,
                "name": section.name,
                "description": section.description,
                "image_path": section.image_path,
                "books": len(section.books)
            }
            return section_with_books
        else:
            raise AlreadyExixt(status_code=409)
        
    def put(self,id):
        section = Sections.query.filter_by(id = id).first()
        if section:
            args = parser_section.parse_args()
            if args["name"] is None:
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Section Name is required")
            
            if args["description"] is None:
                raise BadRequest(status_code=400, error_code="DataNotAvailable", error_message="Section description is required")
            
            if section:
                section.name = args['name']
                section.description = args['description']
                db.session.commit()
                section_with_books = {
                "id": section.id,
                "name": section.name,
                "description": section.description,
                "image_path": section.image_path,
                "books": len(section.books)
            }
            return section_with_books
        else:
            raise NotFoundError(status_code=404)
        

    def delete(self,id):
        section = Sections.query.filter_by(id = id).first()
        if section:
            db.session.delete(section)
            db.session.commit()
            raise CorrectResponse(status_code=200)
        else:
            raise NotFoundError(status_code=404)
        




########## endpoints for apis ##############

api.add_resource(Books_api , "/api/course/<int:id>" , "/api/book")    
api.add_resource(Sections_api, "/api/section/<int:id>", "/api/section")




          
         
        
              

             
        
    
