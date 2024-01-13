import enum
from src.extensions import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Doctor(Base):
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    schedules = db.relationship('Schedule', backref='doctor')
    appointments = db.relationship('Appointment', backref='doctor')

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def __repr__(self):
        return f'<Dr. {self.first_name} {self.last_name}>'


class DayOfWeek(enum.Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Schedule(Base):
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'doctor': self.doctor.serialize(),
            'day_of_week': self.day_of_week.name,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M')
        }

    def __repr__(self):
        return f'<Schedule {self.doctor_id} {self.day_of_week.name} {self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}>'


class Appointment(Base):
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'doctor': self.doctor.serialize(),
            'start_time': self.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%dT%H:%M:%S')
        }

    def __repr__(self):
        return f'<Appointment {self.doctor_id} {self.start_time.strftime("%Y-%m-%dT%H:%M:%S")} - {self.end_time.strftime("%Y-%m-%dT%H:%M:%S")}>'
