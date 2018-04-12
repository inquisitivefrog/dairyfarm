from django.utils.timezone import datetime, pytz

class InvalidTime(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ReportTime:
    @classmethod
    def convert_date(cls, d):
        return datetime.strftime(d, '%Y-%m-%d')

    @classmethod
    def edate_year(cls, y, dt=True):
        y = int(y) + 1
        t = datetime.strptime('{}-01-01'.format(y),
                              '%Y-%m-%d')
        if dt:
            return datetime.date(datetime(t.year,
                                          t.month,
                                          t.day,
                                          tzinfo=pytz.timezone('UTC')))
        else:
            return datetime(t.year,
                            t.month,
                            t.day,
                            tzinfo=pytz.timezone('UTC'))

    @classmethod
    def edate_year_month(cls, y, m):
        if isinstance(y, int):
            y = str(y)
        if isinstance(m, int):
            m = str(m)
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

    @classmethod
    def sdate_year(cls, y, dt=True):
        t = datetime.strptime('{}-01-01'.format(y),
                              '%Y-%m-%d')
        if dt:
            return datetime.date(datetime(t.year,
                                          t.month,
                                          t.day,
                                          tzinfo=pytz.timezone('UTC')))
        else:
            return datetime(t.year,
                            t.month,
                            t.day,
                            tzinfo=pytz.timezone('UTC'))

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

