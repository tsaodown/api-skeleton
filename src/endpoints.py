from http import HTTPStatus
from flask import Blueprint, jsonify
from src.extensions import db
from webargs import fields
from webargs.flaskparser import use_args

from src.models import Appointment, DayOfWeek, Schedule

home = Blueprint('/', __name__)

@home.route('/appts/create', methods=['POST'])
@use_args({'doctor_id': fields.Int(), 'start': fields.DateTime(), 'end': fields.DateTime()}, location='query')
def create_appointment(args):
    doctor_id = args.get('doctor_id')
    start = args.get('start')
    end = args.get('end')
    
    if doctor_id is None:
        return {'error': 'Doctor ID is required'}, HTTPStatus.BAD_REQUEST
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
    
    appointment = Appointment(doctor_id=args.get('doctor_id'), start_time=start.time(), end_time=end.time())
    db.session.add(appointment)
    db.session.commit()

    return {'data': appointment.serialize()}

@home.route('/appts', methods=['GET'])
@use_args({'doctor_id': fields.Int(), 'start': fields.DateTime(), 'end': fields.DateTime()}, location='query')
def get_appointments(args):
    doctor_id = args.get('doctor_id')
    start = args.get('start')
    end = args.get('end')

    appointments = db.session.scalars(db.select(Appointment).filter(Appointment.doctor_id == doctor_id, Appointment.end_time >= start.time(), Appointment.start_time <= end.time())).all()

    return {'data': [appointment.serialize() for appointment in appointments]}