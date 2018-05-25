from django.utils.timezone import datetime, pytz
from django.db.models import Sum

from assets.models import Cow, HealthRecord, Milk

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
    def edate_year_month(cls, y, m, dt=True):
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
        if dt:
            return datetime.date(datetime(t.year,
                                          t.month,
                                          t.day,
                                          tzinfo=pytz.timezone('UTC')))
        else:
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
    def sdate_year_month(cls, y, m, dt=True):
        t = datetime.strptime('{}-{}-01'.format(y, m),
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
                            t.hour,
                            t.minute,
                            t.second,
                            t.microsecond,
                            tzinfo=pytz.timezone('UTC'))

class ReportStats:
    @classmethod
    def get_cows(cls, client, year, month=None):
        if month:
            sdate = ReportTime.sdate_year_month(year,
                                                month,
                                                dt=True)
            edate = ReportTime.edate_year_month(year,
                                                month,
                                                dt=True)
            objs = Cow.objects.filter(purchase_date__lte=edate,
                                      sell_date__gt=edate,
                                      client=client)
        else:
            sdate = ReportTime.sdate_year(year,
                                          dt=True)
            edate = ReportTime.edate_year(year,
                                          dt=True)
            objs = Cow.objects.filter(purchase_date__lte=edate,
                                      sell_date__gt=edate,
                                      client=client)
        return objs

    @classmethod
    def get_total_cows(cls, client, year, month=None):
        objs = ReportStats.get_cows(client, year, month)
        return objs.count()

    @classmethod
    def get_aged_cows(cls, client, year, month=None):
        objs = ReportStats.get_cows(client, year, month)
        return objs.filter(age__name='5 years').count()

        hr_objs = HealthRecord.objects.filter(inspection_time__gte=sdate,
                                              inspection_time__lte=edate,
                                              client=client)
        milk_objs = Milk.objects.filter(milking_time__gte=sdate,
                                        milking_time__lte=edate,
                                        client=client)

    @classmethod
    def get_health_records(cls, client, year, month=None):
        if month:
            sdate = ReportTime.sdate_year_month(year,
                                                month,
                                                dt=False)
            edate = ReportTime.edate_year_month(year,
                                                month,
                                                dt=False)
        else:
            sdate = ReportTime.sdate_year(year,
                                          dt=False)
            edate = ReportTime.edate_year(year,
                                          dt=False)
        objs = HealthRecord.objects.filter(inspection_time__gte=sdate,
                                           inspection_time__lte=edate,
                                           client=client)
        return objs

    @classmethod
    def get_pregnant_cows(cls, client, year, month=None):
        # as HealthRecord measures twice a day, use set to eliminate duplicates
        objs = ReportStats.get_health_records(client,
                                              year,
                                              month)
        pregnant = set()
        [ pregnant.add(str(hr.cow.rfid)) for hr in objs.filter(status__name='Pregnant') ]
        return len(pregnant)

    @classmethod
    def get_ill_cows(cls, client, year, month=None):
        objs = ReportStats.get_health_records(client,
                                              year,
                                              month)
        illnesses = ['Bacterial Illness', 'Viral Illness']
        return objs.filter(status__name__in=illnesses).count()

    @classmethod
    def get_injured_cows(cls, client, year, month=None):
        objs = ReportStats.get_health_records(client,
                                              year,
                                              month)
        return objs.filter(status__name='Injured').count()

    @classmethod
    def get_milk_records(cls, client, year, month=None):
        if month:
            sdate = ReportTime.sdate_year_month(year,
                                                month,
                                                dt=False)
            edate = ReportTime.edate_year_month(year,
                                                month,
                                                dt=False)
        else:
            sdate = ReportTime.sdate_year(year,
                                          dt=False)
            edate = ReportTime.edate_year(year,
                                          dt=False)
        objs = Milk.objects.filter(milking_time__gte=sdate,
                                   milking_time__lte=edate,
                                   client=client)
        return objs

    @classmethod
    def get_gallons_milk(cls, client, year, month=None):
        objs = ReportStats.get_milk_records(client,
                                            year,
                                            month)
        if len(objs) > 0:
            return objs.aggregate(Sum('gallons'))['gallons__sum']
        else:
            return 0


