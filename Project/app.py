from flask import Flask
from flask_migrate import Migrate
from application.config import LocalDevelopmentConfig
from flask_apscheduler import APScheduler
from application.models import db
import os


app = None


def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development ...")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    migrate = Migrate(app, db)

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('interval', id='delete_access', seconds=5)
    def scheduled_job():
        with app.app_context():
            delete_access()

    return app, scheduler


app, scheduler = create_app()


from application.api import *
from application.controllers import *



@app.context_processor
def inject_all_func():
    return dict(can_rate = can_rate,
                Random =  Random,
                make_tuple = make_tuple,
                remaining_books = remaining_books,
                calu_avg = calu_avg,
                book_availability = book_availability,
                format_time_difference = format_time_difference,
                remaining_time = remaining_time,
                calu_notification = calu_notification,
                all_sectionss = all_sectionss,
                top_books = top_books,
                request_exist = request_exist)



if __name__ == "__main__":
    add_librarian()
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, use_reloader=False)