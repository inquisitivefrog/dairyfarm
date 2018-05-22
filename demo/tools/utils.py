from random import randint

from django.conf import settings
from django.db.utils import IntegrityError
from django.utils.timezone import datetime, pytz

from sys import path

from assets.models import Action, Cow, Event, HealthRecord
from assets.models import Illness, Injury, Pasture
from assets.models import Seed, Status, Treatment, Vaccine
from assets.serializers import EventWriteSerializer
from assets.serializers import ExerciseWriteSerializer
from assets.serializers import HealthRecordWriteSerializer
from assets.serializers import MilkWriteSerializer

class ToolTime:
    @classmethod
    def get_date(cls):
        t = datetime.now()
        return datetime.date(t)

    @classmethod
    def add_time(cls, dt, t):
        pass

    @classmethod
    def get_year(cls, dt):
        return dt.year

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

    @classmethod
    def get_morning(cls, d):
        tmp = datetime.strptime('{} 04:00:00'.format(d), '%Y-%m-%d %H:%M:%S')
        return datetime(tmp.year,
                        tmp.month,
                        tmp.day,
                        tmp.hour,
                        tmp.minute,
                        tmp.second,
                        tmp.microsecond,
                        tzinfo=pytz.timezone(settings.TIME_ZONE))

    @classmethod
    def get_evening(cls, d):
        tmp = datetime.strptime('{} 16:00:00'.format(d), '%Y-%m-%d %H:%M:%S')
        return datetime(tmp.year,
                        tmp.month,
                        tmp.day,
                        tmp.hour,
                        tmp.minute,
                        tmp.second,
                        tmp.microsecond,
                        tzinfo=pytz.timezone(settings.TIME_ZONE))

class ToolData:
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
    def get_healthy_cow_data(cls, cow, dt, user):
        # ideal healthy temp range: 100.4 - 102.0
        temperature = randint(1004, 1020) * 10.0 / 100
        # ideal healthy resp range: 26 - 50
        respiratory_rate = randint(260, 500) * 10.0 / 100
        # ideal healthy HR range: 48 - 84
        heart_rate = randint(480, 840) * 10.0 / 100
        # ideal healthy BP range: 130 - 150
        blood_pressure = randint(1300, 1500) * 10 / 100
        # ideal healthy BCS range: 3.0 - 3.5
        body_condition_score = randint(30, 35) * 10.0 / 100
        # ideal healthy weight range: 450 - 550 
        weight = randint(450, 550)
        #pregnant = randint(1, 10)
        #if pregnant < 3:
        #    status = Status.objects.get(pk=2).name
        #else:
        status = Status.objects.get(pk=1).name
        return {'recorded_by': user,
                'inspection_time': dt,
                'cow': cow.rfid,
                'client': cow.client,
                'temperature': temperature,
                'respiratory_rate': respiratory_rate,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'weight': weight,
                'body_condition_score': body_condition_score,
                'status': status}

    @classmethod
    def _get_ill_injured_cow_data(cls, cow, dt, user):
        temperature = randint(960, 1050) * 10.0 / 100
        respiratory_rate = randint(250, 700) * 10.0 / 100
        heart_rate = randint(450, 900) * 10.0 / 100
        blood_pressure = randint(1150, 1750) * 10.0 / 100
        body_condition_score = randint(20, 40) * 10.0 / 100
        weight = randint(400, 650)
        return {'recorded_by': user,
                'inspection_time': dt,
                'cow': cow.rfid,
                'client': cow.client,
                'temperature': temperature,
                'respiratory_rate': respiratory_rate,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'weight': weight,
                'body_condition_score': body_condition_score}

    @classmethod
    def get_injured_cow_data(cls, cow, dt, user):
        injuries = [x.diagnosis for x in Injury.objects.all()]
        injury = injuries[randint(1, len(injuries) - 1)]
        treatments = [x.name for x in Treatment.objects.all()]
        treatment = treatments[randint(1, len(treatments) - 1)]
        data = cls._get_ill_injured_cow_data(cow, dt, user)
        data.update({'status': 'Injured',
                     'injury': injury,
                     'treatment': treatment})
        return data

    @classmethod
    def get_ill_cow_data(cls, cow, dt, user):
        status = Status.objects.get(pk=randint(4,5)).name
        illnesses = [x.diagnosis for x in Illness.objects.all()]
        illness = illnesses[randint(1, len(illnesses) - 1)]
        vaccines = [x.name for x in Vaccine.objects.all()]
        vaccine = vaccines[randint(1, len(vaccines) - 1)]
        data = cls._get_ill_injured_cow_data(cow, dt, user)
        data.update({'status': status,
                     'illness': illness,
                     'vaccine': vaccine})
        return data

    @classmethod
    def log_event(cls, action, cow, dt, user):
        try:
            a = Action.objects.get(name=action)
            c = Cow.objects.get(rfid=cow.rfid)
            data = {'recorded_by': user,
                    'event_time': dt,
                    'client': c.client,
                    'cow': c.rfid,
                    'action': action}
            es = EventWriteSerializer(data=data)
            if es.is_valid() and len(es.errors) == 0:
                es.save()
            else:
                print('EventWriteSerializer failed')
                print('ERROR: {}'.format(es.errors))
        except IntegrityError as e:
            print('Integrity error')
            print('ERROR: {}'.format(e))

    @classmethod
    def log_exercise(cls, pasture, cow, dt, user):
        try:
            data = {'recorded_by': user,
                    'exercise_time': dt,
                    'cow': cow.rfid,
                    'client': cow.client,
                    'pasture': pasture.name}
            es = ExerciseWriteSerializer(data=data)
            if es.is_valid() and len(es.errors) == 0:
                es.save()
            else:
                print('ERROR: {}'.format(es.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_healthrecord(cls, data, cow, dt, user):
        try:
            hrs = HealthRecordWriteSerializer(data=data)
            if hrs.is_valid() and len(hrs.errors) == 0:
                hrs.save()
            else:
                print('ERROR: {}'.format(hrs.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def log_milk(cls, gallons, cow, dt, user):
        try:
            data = {'recorded_by': user,
                    'milking_time': dt,
                    'cow': cow.rfid,
                    'client': cow.client,
                    'gallons': gallons}
            ms = MilkWriteSerializer(data=data)
            if ms.is_valid() and len(ms.errors) == 0:
                ms.save()
            else:
                print('ERROR: {}'.format(ms.errors))
        except IntegrityError as e:
            print('ERROR: {}'.format(e))

    @classmethod
    def convert_name(cls, name):
        new_name = []
        for word in name.split('_'):
            new_name.append(word.capitalize())
        return ' '.join(new_name)

    @classmethod
    def valid_pasture(cls, pasture, username):
        ff_pastures = ['North', 'West', 'South', 'East', 'Central North',
                       'Central West', 'Central South', 'Central East',
                       'North West', 'North East', 'South West',
                       'South East', 'Pen']
        b_pastures = ['Lot_1', 'Lot_2', 'Lot_3', 'Lot_4', 'Lot_5', 'Lot_6',
                      'Lot_7', 'Lot_8', 'Lot_9']
        if username == 'foster':
            if pasture in ff_pastures:
                return True
            else:
                return False
        if username == 'berkeley':
            if pasture in b_pastures:
                return True
            else:
                return False
