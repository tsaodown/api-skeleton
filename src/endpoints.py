from http import HTTPStatus
from flask import Blueprint
from src.extensions import db
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy import or_, and_

from src.models import Appointment, DayOfWeek, Doctor, Schedule

appts = Blueprint('/', __name__)

@appts.route('/create', methods=['POST'])
@use_args({'doctor_id': fields.Int(), 'start': fields.DateTime(), 'end': fields.DateTime()}, location='query')
def create_appointment(args):
    doctor_id = args.get('doctor_id')
    start = args.get('start')
    end = args.get('end')
    
    if doctor_id is None:
        return {'error': 'Doctor ID is required'}, HTTPStatus.BAD_REQUEST
    if db.session.query(Doctor).filter(Doctor.id == doctor_id).count() == 0:
        return {'error': 'Doctor not found'}, HTTPStatus.NOT_FOUND
    if start is None or end is None:
        return {'error': 'Start and end times are required'}, HTTPStatus.BAD_REQUEST
    if start >= end:
        return {'error': 'Invalid start and end times'}, HTTPStatus.BAD_REQUEST
    if start.weekday() != end.weekday():
        return {'error': 'Start and end times must be on the same day'}, HTTPStatus.BAD_REQUEST

    schedule = db.session.scalars(db.select(Schedule).filter(Schedule.doctor_id == doctor_id, Schedule.day_of_week == DayOfWeek(start.weekday()))).first()
    if (schedule is None or start.time() < schedule.start_time or end.time() > schedule.end_time):
        return {'error': 'Doctor not available'}, HTTPStatus.NOT_FOUND

    existing_appointments = db.session.query(Appointment).filter(Appointment.doctor_id == doctor_id, Appointment.end_time >= start, Appointment.start_time <= end).count()
    if (existing_appointments is not None and existing_appointments > 0):
        return {'error': 'Doctor not available'}, HTTPStatus.NOT_FOUND
    
    appointment = Appointment(doctor_id=args.get('doctor_id'), start_time=start, end_time=end)
    db.session.add(appointment)
    db.session.commit()

    return {'data': appointment.serialize()}

@appts.route('/', methods=['GET'])
@use_args({'doctor_id': fields.Int(), 'start': fields.DateTime(), 'end': fields.DateTime()}, location='query')
def get_appointments(args):
    doctor_id = args.get('doctor_id')
    start = args.get('start')
    end = args.get('end')

    if doctor_id is None:
        return {'error': 'Doctor ID is required'}, HTTPStatus.BAD_REQUEST
    if db.session.query(Doctor).filter(Doctor.id == doctor_id).count() == 0:
        return {'error': 'Doctor not found'}, HTTPStatus.NOT_FOUND
    if start is None or end is None:
        return {'error': 'Start and end times are required'}, HTTPStatus.BAD_REQUEST
    if start >= end:
        return {'error': 'Invalid start and end times'}, HTTPStatus.BAD_REQUEST

    appointments = db.session.scalars(db.select(Appointment).filter(Appointment.doctor_id == doctor_id, Appointment.end_time >= start, Appointment.start_time <= end)).all()

    return {'data': [appointment.serialize() for appointment in appointments]}