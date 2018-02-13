from random import randint

from django.conf import settings
from django.db.utils import IntegrityError
from django.utils.timezone import datetime, pytz

from assets.models import Action, Cow, Event, Pasture, Illness
from assets.models import Injury, Status, Treatment
from assets.serializers import CowSerializer, EventSerializer
from assets.serializers import ExerciseSerializer, HealthRecordSerializer
from assets.serializers import MilkSerializer, PastureSerializer

class TestTime:
    @classmethod
    def add_time(cls, dt, t):
        pass

    @classmethod
    def convert_datetime(cls, dt):
        tmp = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        return datetime(tmp.year,
                        tmp.month,
                        tmp.day,
                        tmp.hour,
                        tmp.minute,
                        tmp.second,
                        tmp.microsecond,
                        tzinfo=pytz.timezone(settings.TIME_ZONE))

    @classmethod
    def convert_date(cls, d):
        return datetime.date(datetime.strptime(d, '%Y-%m-%d'))

class TestData:
    @classmethod
    def get_health(cls):
        unhealthy = randint(1, 10)
        if unhealthy == 1:
            injured = randint(1, 2)
            if injured == 1:
                return 'injured'
            else:
                return 'ill'
        else:
            return 'healthy'

    @classmethod
    def get_healthy_cow_data(cls, c_id, dt, u_id):
        # ideal healthy temp range: 100.4 - 102.0
        temperature = randint(1004, 1020) * 10.0 / 100
        # ideal healthy resp range: 26 - 50
        respiratory_rate = randint(260, 500) * 10.0 / 100
        # ideal healthy HR range: 48 - 84
        heart_rate = randint(480, 840) * 10.0 / 100
        # ideal healthy BP range: 130 - 150
        blood_pressure = randint(1300, 1500) * 10.0 / 100
        # ideal healthy BCS range: 3.0 - 3.5
        body_condition_score = randint(30, 35) * 10.0 / 100
        # ideal healthy weight range: 450 - 550 
        weight = randint(450, 550)
        status_id = randint(1, 2)
        return {'recorded_by': u_id,
                'timestamp': dt,
                'cow': c_id,
                'temperature': temperature,
                'respiratory_rate': respiratory_rate,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'weight': weight,
                'body_condition_score': body_condition_score,
                'status': status_id}

    @classmethod
    def _get_ill_injured_cow_data(cls, c_id, dt, u_id):
        temperature = randint(960, 1050) * 10.0 / 100
        respiratory_rate = randint(250, 700) * 10.0 / 100
        heart_rate = randint(450, 900) * 10.0 / 100
        blood_pressure = randint(1150, 1750) * 10.0 / 100
        body_condition_score = randint(20, 40) * 10.0 / 100
        weight = randint(400, 650)
        return {'recorded_by': u_id,
                'timestamp': dt,
                'cow': c_id,
                'temperature': temperature,
                'respiratory_rate': respiratory_rate,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'weight': weight,
                'body_condition_score': body_condition_score}

    @classmethod
    def get_injured_cow_data(cls, c_id, dt, u_id):
        status_id = 3
        injuries = [i.id for i in Injury.objects.all() ]
        injury_id = injuries[randint(1, len(injuries) - 1)]
        data = cls._get_ill_injured_cow_data(c_id, dt, u_id)
        data.update({'status': status_id,
                     'injury': injury_id})
        return data

    @classmethod
    def get_ill_cow_data(cls, c_id, dt, u_id):
        statuses = [s.id for s in Status.objects.all() ]
        status_id = statuses[randint(4, len(statuses) - 1)]
        illnesses = [i.id for i in Illness.objects.all() ]
        illness_id = illnesses[randint(1, len(illnesses) - 1)]
        data = cls._get_ill_injured_cow_data(c_id, dt, u_id)
        data.update({'status': status_id,
                     'illness': illness_id})
        return data

    @classmethod
    def log_event(cls, action, c_id, dt, u_id):
        try:
            a = Action.objects.get(name=action)
            if not a:
                print('ERROR: action: {} does not exist!'.format(action))
            data = {'recorded_by': u_id,
                    'timestamp': dt,
                    'cow': c_id,
                    'action': a.id}
            es = EventSerializer(data=data)
            if es.is_valid() and len(es.errors) == 0:
                es.save()
            else:
                print('ERROR: {}'.format(es.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_exercise(cls, distance, p_id, c_id, dt, u_id):
        try:
            data = {'recorded_by': u_id,
                    'timestamp': dt,
                    'cow': c_id,
                    'pasture': p_id,
                    'distance': distance}
            es = ExerciseSerializer(data=data)
            if es.is_valid() and len(es.errors) == 0:
                es.save()
            else:
                print('ERROR: {}'.format(es.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_healthrecord(cls, data, c_id, dt, u_id):
        try:
            hrs = HealthRecordSerializer(data=data)
            if hrs.is_valid() and len(hrs.errors) == 0:
                hrs.save()
            else:
                print('ERROR: {}'.format(hrs.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_milk(cls, gallons, c_id, dt, u_id):
        try:
            data = {'recorded_by': u_id,
                    'timestamp': dt,
                    'cow': c_id,
                    'gallons': gallons}
            ms = MilkSerializer(data=data)
            if ms.is_valid() and len(ms.errors) == 0:
                ms.save()
            else:
                print('ERROR: {}'.format(ms.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_pedicure(cls, action, p_id, c_id, dt, u_id):
        try:
            data = {'recorded_by': u_id,
                    'timestamp': dt,
                    'cow': c_id,
                    'pasture': p_id,
                    'distance': distance}
            es = ExerciseSerializer(data=data)
            if es.is_valid() and len(es.errors) == 0:
                es.save()
            else:
                print('ERROR: {}'.format(es.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_vaccination(cls, diagnosis, c_id, dt, u_id):
        try:
            data = {'recorded_by': u_id,
                    'timestamp': dt,
                    'cow': c_id,
                    'diagnosis': diagnosis}
            ms = MilkSerializer(data=data)
            if ms.is_valid() and len(ms.errors) == 0:
                ms.save()
            else:
                print('ERROR: {}'.format(ms.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))
