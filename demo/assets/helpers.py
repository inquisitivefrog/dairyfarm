from django.utils.timezone import datetime, pytz

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
    def get_today(cls):
        t = datetime.today()
        return cls.convert_date(t)

    @classmethod
    def sdate_year_month(cls, y, m):
        t = datetime.strptime('{}-{}-01'.format(y, m),
                              '%Y-%m-%d')
        return datetime(t.year,
                        t.month,
                        t.day,
                        t.hour,
                        t.minute,
                        t.second,
                        t.microsecond,
                        tzinfo=pytz.timezone('UTC'))

    @classmethod
    def edate_year_month(cls, y, m):
        if m == '12':
            y = int(y) + 1
            m = '01'
            t = datetime.strptime('{}-{}-01'.format(y, m),
                                  '%Y-%m-%d')
        elif m.startswith('0'):
            m = int(m[1:]) + 1
            if m < 10:
                t = datetime.strptime('{}-0{}-01'.format(y, m),
                                      '%Y-%m-%d')
            else:
                t = datetime.strptime('{}-{}-01'.format(y, m),
                                      '%Y-%m-%d')
        else:
            m = int(m) + 1
            t = datetime.strptime('{}-{}-01'.format(y, m),
                                  '%Y-%m-%d')
        return datetime(t.year,
                        t.month,
                        t.day,
                        t.hour,
                        t.minute,
                        t.second,
                        t.microsecond,
                        tzinfo=pytz.timezone('UTC'))

    @classmethod
    def edate_year(cls, y):
        y = int(y) + 1
        return '{}-01-01'.format(y)

    @classmethod
    def get_datetime(cls, y, m):
        t = datetime.strptime('{}-{}-01'.format(y, m),
                              '%Y-%m-%d')
        return datetime(t.year,
                        t.month,
                        t.day,
                        t.hour,
                        t.minute,
                        t.second,
                        t.microsecond,
                        tzinfo=pytz.timezone('UTC'))
