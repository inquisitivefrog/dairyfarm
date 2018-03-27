from django.utils.timezone import datetime, localtime, pytz

class InvalidTime(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class AssetTime:
    @classmethod
    def convert_date(cls, d):
        return datetime.strftime(d, '%Y-%m-%d')

    @classmethod
    def sdate_year(cls, y):
        return '{}-01-01'.format(y)

    @classmethod
    def sdate_year_month(cls, y, m):
        return '{}-{}-01'.format(y, m)

    @classmethod
    def edate_year_month(cls, y, m):
        if m == '12':
            y = int(y) + 1
            m = '01'
            return '{}-{}-01'.format(y, m)
        elif m.startswith('0'):
            m = int(m[1:]) + 1
            if m < 10:
                return '{}-0{}-01'.format(y, m)
            else:
                return '{}-{}-01'.format(y, m)
        else:
            m = int(m) + 1
            return '{}-{}-01'.format(y, m)

    @classmethod
    def edate_year(cls, y):
        y = int(y) + 1
        return '{}-01-01'.format(y)

