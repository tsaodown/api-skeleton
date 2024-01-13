from datetime import datetime
from http import HTTPStatus
import pytest

from src.models import Appointment


@pytest.fixture
def data_appointment_doc_1_appt_1(db):
    db.session.add(Appointment(doctor_id=1, start_time=datetime.fromisoformat(
        '2021-01-01T09:00:00'), end_time=datetime.fromisoformat('2021-01-01T10:00:00')))
    db.session.commit()


@pytest.fixture
def data_appointment_doc_2_appt_1(db):
    db.session.add(Appointment(doctor_id=2, start_time=datetime.fromisoformat(
        '2021-01-01T09:00:00'), end_time=datetime.fromisoformat('2021-01-01T10:00:00')))
    db.session.commit()


@pytest.fixture
def data_appointment_doc_1_appt_2(db):
    db.session.add(Appointment(doctor_id=1, start_time=datetime.fromisoformat(
        '2024-01-11T16:00:00'), end_time=datetime.fromisoformat('2024-01-11T17:00:00')))
    db.session.commit()


@pytest.fixture
def data_appointment_doc_1_appt_3(db):
    db.session.add(Appointment(doctor_id=1, start_time=datetime.fromisoformat(
        '2024-01-12T16:00:00'), end_time=datetime.fromisoformat('2024-01-12T17:00:00')))
    db.session.commit()


def test_create_appointment_happy_path(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 1,
        'start': '2021-01-01T09:00:00',
        'end': '2021-01-01T10:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 1
    assert res.json.get('data').get('start_time') == '2021-01-01T09:00:00'
    assert res.json.get('data').get('end_time') == '2021-01-01T10:00:00'


def test_create_appointment_missing_doctor(client):
    res = client.post('/appts/create', query_string={
        'start': '2021-01-01T09:00:00',
        'end': '2021-01-01T10:00:00'
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get('error') == 'Doctor ID is required'


def test_create_appointment_invalid_doctor(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 3,
        'start': '2021-01-01T09:00:00',
        'end': '2021-01-01T10:00:00'
    })

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json.get('error') == 'Doctor not found'


def test_create_appointment_off_schedule(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 1,
        'start': '2021-01-01T08:00:00',
        'end': '2021-01-01T09:00:00'
    })

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json.get('error') == 'Doctor not available'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_1')
def test_create_appointment_doctor_busy(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 1,
        'start': '2021-01-01T09:30:00',
        'end': '2021-01-01T10:30:00'
    })

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json.get('error') == 'Doctor not available'


def test_create_appointment_invalid_start_end(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 1,
        'start': '2021-01-01T10:00:00',
        'end': '2021-01-01T09:00:00'
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get('error') == 'Invalid start and end times'


def test_create_appointment_invalid_day(client):
    res = client.post('/appts/create', query_string={
        'doctor_id': 1,
        'start': '2021-01-02T09:00:00',
        'end': '2021-01-03T10:00:00'
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get(
        'error') == 'Start and end times must be on the same day'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_1', 'data_appointment_doc_2_appt_1')
def test_get_appointments_happy_path_1(client):
    res = client.get('/appts/', query_string={
        'doctor_id': 1,
        'start': '2021-01-01T00:00:00',
        'end': '2021-01-02T00:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert len(res.json.get('data')) == 1
    assert res.json.get('data')[0].get('doctor').get('id') == 1
    assert res.json.get('data')[0].get('start_time') == '2021-01-01T09:00:00'
    assert res.json.get('data')[0].get('end_time') == '2021-01-01T10:00:00'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_1', 'data_appointment_doc_2_appt_1')
def test_get_appointments_happy_path_2(client):
    res = client.get('/appts/', query_string={
        'doctor_id': 2,
        'start': '2021-01-01T00:00:00',
        'end': '2021-01-02T00:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert len(res.json.get('data')) == 1
    assert res.json.get('data')[0].get('doctor').get('id') == 2
    assert res.json.get('data')[0].get('start_time') == '2021-01-01T09:00:00'
    assert res.json.get('data')[0].get('end_time') == '2021-01-01T10:00:00'


def test_get_appointments_missing_doctor(client):
    res = client.get('/appts/', query_string={
        'start': '2021-01-01T00:00:00',
        'end': '2021-01-02T00:00:00'
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get('error') == 'Doctor ID is required'


def test_get_appointments_invalid_doctor(client):
    res = client.get('/appts/', query_string={
        'doctor_id': 3,
        'start': '2021-01-01T00:00:00',
        'end': '2021-01-02T00:00:00'
    })

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json.get('error') == 'Doctor not found'


def test_get_appointments_missing_start_end(client):
    res = client.get('/appts/', query_string={
        'doctor_id': 1
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get('error') == 'Start and end times are required'


def test_get_appointments_invalid_start_end(client):
    res = client.get('/appts/', query_string={
        'doctor_id': 1,
        'start': '2021-01-02T00:00:00',
        'end': '2021-01-01T00:00:00'
    })

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json.get('error') == 'Invalid start and end times'


def test_first_available_happy_path_at_start(client):
    res = client.get('/appts/first_available', query_string={
        'start': '2021-01-01T09:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 1
    assert res.json.get('data').get('time') == '2021-01-01T09:00:00'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_1', 'data_appointment_doc_2_appt_1')
def test_first_available_happy_path_start_occupied(client):
    res = client.get('/appts/first_available', query_string={
        'start': '2021-01-01T09:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 1
    assert res.json.get('data').get('time') == '2021-01-01T10:00:00'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_2')
def test_first_available_happy_path_next_day(client):
    res = client.get('/appts/first_available', query_string={
        'start': '2024-01-11T16:30:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 2
    assert res.json.get('data').get('time') == '2024-01-12T08:00:00'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_3')
def test_first_available_happy_path_over_weekend(client):
    res = client.get('/appts/first_available', query_string={
        'start': '2024-01-12T16:30:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 2
    assert res.json.get('data').get('time') == '2024-01-15T08:00:00'


@pytest.mark.usefixtures('data_appointment_doc_1_appt_1')
def test_first_available_happy_path_doctor_2(client):
    res = client.get('/appts/first_available', query_string={
        'start': '2021-01-01T09:00:00'
    })

    assert res.status_code == HTTPStatus.OK
    assert res.json.get('data').get('doctor').get('id') == 2
    assert res.json.get('data').get('time') == '2021-01-01T09:00:00'

    def test_first_available_invalid_start(client):
        res = client.get('/appts/first_available', query_string={
            'start': '2021-01-01T08:00:00'
        })

        assert res.status_code == HTTPStatus.BAD_REQUEST
        assert res.json.get('error') == 'Invalid start time'
