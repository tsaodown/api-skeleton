from datetime import time
from flask import Flask
from src.extensions import db
from src.endpoints import appts
from src.models import DayOfWeek, Doctor, Schedule


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    # We are doing a create all here to set up all the tables. Because we are using an in memory sqllite db, each
    # restart wipes the db clean, but does have the advantage of not having to worry about schema migrations.
    with app.app_context():
        db.create_all()

        strange = Doctor(first_name='Stephen', last_name='Strange')
        strange.schedules.append(Schedule(day_of_week=DayOfWeek.MON, start_time=time(hour=9), end_time=time(hour=17)))
        strange.schedules.append(Schedule(day_of_week=DayOfWeek.TUE, start_time=time(hour=9), end_time=time(hour=17)))
        strange.schedules.append(Schedule(day_of_week=DayOfWeek.WED, start_time=time(hour=9), end_time=time(hour=17)))
        strange.schedules.append(Schedule(day_of_week=DayOfWeek.THU, start_time=time(hour=9), end_time=time(hour=17)))
        strange.schedules.append(Schedule(day_of_week=DayOfWeek.FRI, start_time=time(hour=9), end_time=time(hour=17)))
        db.session.add(strange)

        who = Doctor(first_name='Doctor', last_name='Who')
        who.schedules.append(Schedule(day_of_week=DayOfWeek.MON, start_time=time(hour=8), end_time=time(hour=16)))
        who.schedules.append(Schedule(day_of_week=DayOfWeek.TUE, start_time=time(hour=8), end_time=time(hour=16)))
        who.schedules.append(Schedule(day_of_week=DayOfWeek.WED, start_time=time(hour=8), end_time=time(hour=16)))
        who.schedules.append(Schedule(day_of_week=DayOfWeek.THU, start_time=time(hour=8), end_time=time(hour=16)))
        who.schedules.append(Schedule(day_of_week=DayOfWeek.FRI, start_time=time(hour=8), end_time=time(hour=16)))
        db.session.add(who)
        
        db.session.commit()

    app.register_blueprint(appts, url_prefix='/appts')
    return app
