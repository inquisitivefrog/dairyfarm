from random import randint
from uuid import uuid4

from django.utils.timezone import datetime, localtime, pytz
from django.contrib.auth.models import User

class TestData:
    @classmethod
    def get_allowed_methods(cls):
        return 'GET, POST, HEAD, OPTIONS'

    @classmethod
    def get_content_type(cls):
        return 'text/html; charset=utf-8'

    @classmethod
    def get_format(cls):
        return 'application/json'

    @classmethod
    def get_annual_read_keys(cls):
        return ['id', 'created_by', 'year', 'total_cows', 'pregnant_cows',
                'ill_cows', 'injured_cows', 'gallons_milk', 'link']

    @classmethod
    def get_annual_write_keys(cls):
        return ['id', 'created_by', 'year']

    @classmethod
    def get_monthly_read_keys(cls):
        return ['id', 'created_by', 'year', 'month', 'total_cows',
                'pregnant_cows', 'ill_cows', 'injured_cows',
                'gallons_milk', 'link']

    @classmethod
    def get_monthly_write_keys(cls):
        return ['id', 'created_by', 'year', 'month']

    @classmethod
    def get_random_username(cls):
        users = [ u.username for u in User.objects.all() ]
        return users[randint(0, len(users) - 1)]

class TestTime:
    @classmethod
    def get_random_year(cls):
        year = randint(2015, 2018)
        return str(year)

    @classmethod
    def get_random_month(cls):
        month = randint(1, 12)
        if month < 10:
            return '0{}'.format(month)
        return str(month)

    @classmethod
    def get_random_month_int(cls):
        month = randint(1, 12)
        return month
