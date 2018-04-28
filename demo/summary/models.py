from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from rest_framework.reverse import django_reverse

from assets.models import Cow, HealthRecord, Milk

from summary.helpers import ReportTime

class Annual(models.Model):
    Y2015 = 2015
    Y2016 = 2016
    Y2017 = 2017
    Y2018 = 2018

    YEARS = (
        (Y2015, '2015'),
        (Y2016, '2016'),
        (Y2017, '2017'),
        (Y2018, '2018')
    )
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    year = models.SmallIntegerField(choices=YEARS,
                                    default=Y2015)
    total_cows = models.SmallIntegerField(default=0)
    aged_cows = models.SmallIntegerField(default=0)
    pregnant_cows = models.SmallIntegerField(default=0)
    ill_cows = models.SmallIntegerField(default=0)
    injured_cows = models.SmallIntegerField(default=0)
    gallons_milk = models.SmallIntegerField(default=0)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def _get_total_cows(self, objs):
        return objs.count()

    def _get_aged_cows(self, objs):
        return objs.filter(age__name='5 years').count()

    def _get_pregnant_cows(self, objs):
        # as HealthRecord measures twice a day, use set to eliminate duplicates
        pregnant = set()
        [ pregnant.add(str(hr.cow.rfid)) for hr in objs.filter(status__name='Pregnant') ]
        return len(pregnant)

    def _get_ill_cows(self, objs):
        illnesses = ['Bacterial Illness', 'Viral Illness']
        return objs.filter(status__name__in=illnesses).count()

    def _get_injured_cows(self, objs):
        return objs.filter(status__name='Injured').count()

    def _get_gallons_milk(self, objs):
        if len(objs) > 0:
            return objs.aggregate(Sum('gallons'))['gallons__sum']
        else:
            return 0

    def __str__(self):
        if self.id:
            return str(self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Annual, self).save(*args, **kwargs)
        sdate = ReportTime.sdate_year(self.year)
        edate = ReportTime.edate_year(self.year)
        cow_objs = Cow.objects.filter(purchase_date__lte=edate,
                                      sell_date__gt=edate)
        sdate = ReportTime.sdate_year(self.year, dt=False)
        edate = ReportTime.edate_year(self.year, dt=False)
        hr_objs = HealthRecord.objects.filter(inspection_time__gte=sdate,
                                              inspection_time__lte=edate)
        milk_objs = Milk.objects.filter(milking_time__gte=sdate,
                                        milking_time__lte=edate)
        kwargs = {'link': django_reverse('summary:monthly-by-year',
                                         kwargs = {'year': self.year}),
                  'total_cows': self._get_total_cows(cow_objs),
                  'aged_cows': self._get_aged_cows(cow_objs),
                  'pregnant_cows': self._get_pregnant_cows(hr_objs),
                  'ill_cows': self._get_ill_cows(hr_objs),
                  'injured_cows': self._get_injured_cows(hr_objs),
                  'gallons_milk': self._get_gallons_milk(milk_objs)}
        Annual.objects.filter(pk=self.pk).update(**kwargs)
        return

class Monthly(models.Model):
    Y2015 = 2015
    Y2016 = 2016
    Y2017 = 2017
    Y2018 = 2018

    YEARS = (
        (Y2015, '2015'),
        (Y2016, '2016'),
        (Y2017, '2017'),
        (Y2018, '2018')
    )
    JAN = 1
    FEB = 2 
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8 
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12

    MONTHS = (
        (JAN, 'January'),
        (FEB, 'February'),
        (MAR, 'March'),
        (APR, 'April'),
        (MAY, 'May'),
        (JUN, 'June'),
        (JUL, 'July'),
        (AUG, 'August'),
        (SEP, 'September'),
        (OCT, 'October'),
        (NOV, 'November'),
        (DEC, 'December')
    )
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    year = models.SmallIntegerField(choices=YEARS,
                                    default=Y2015)
    month = models.SmallIntegerField(choices=MONTHS,
                                     default=JAN)
    total_cows = models.SmallIntegerField(default=0)
    aged_cows = models.SmallIntegerField(default=0)
    pregnant_cows = models.SmallIntegerField(default=0)
    ill_cows = models.SmallIntegerField(default=0)
    injured_cows = models.SmallIntegerField(default=0)
    gallons_milk = models.SmallIntegerField(default=0)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def _get_total_cows(self, objs):
        return objs.count()

    def _get_aged_cows(self, objs):
        return objs.filter(age__name='5 years').count()

    def _get_pregnant_cows(self, objs):
        # as HealthRecord measures twice a day, use set to eliminate duplicates
        pregnant = set()
        [ pregnant.add(str(hr.cow.rfid)) for hr in objs.filter(status__name='Pregnant') ]
        return len(pregnant)

    def _get_ill_cows(self, objs):
        illnesses = ['Bacterial Illness', 'Viral Illness']
        return objs.filter(status__name__in=illnesses).count()

    def _get_injured_cows(self, objs):
        return objs.filter(status__name='Injured').count()

    def _get_gallons_milk(self, objs):
        if len(objs) > 0:
            return objs.aggregate(Sum('gallons'))['gallons__sum']
        else:
            return 0

    def __str__(self):
        if self.id:
            return str(self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Monthly, self).save(*args, **kwargs)
        sdate = ReportTime.sdate_year_month(self.year,
                                            self.month)
        edate = ReportTime.edate_year_month(self.year,
                                            self.month)
        cow_objs = Cow.objects.filter(purchase_date__lte=edate,
                                      sell_date__gt=edate)
        sdate = ReportTime.sdate_year_month(self.year,
                                            self.month)
        edate = ReportTime.edate_year_month(self.year,
                                            self.month)
        hr_objs = HealthRecord.objects.filter(inspection_time__gte=sdate,
                                              inspection_time__lte=edate)
        milk_objs = Milk.objects.filter(milking_time__gte=sdate,
                                        milking_time__lte=edate)
        kwargs = {'total_cows': self._get_total_cows(cow_objs),
                  'aged_cows': self._get_aged_cows(cow_objs),
                  'pregnant_cows': self._get_pregnant_cows(hr_objs),
                  'ill_cows': self._get_ill_cows(hr_objs),
                  'injured_cows': self._get_injured_cows(hr_objs),
                  'gallons_milk': self._get_gallons_milk(milk_objs)}
        if isinstance(self.month, int) and self.month < 10:
            kwargs.update({'link': django_reverse('summary:monthly',
                                                  kwargs = {'year': self.year,
                                                            'month': '0{}'.format(self.month)})})
        else:
            kwargs.update({'link': django_reverse('summary:monthly',
                                                  kwargs = {'year': self.year,
                                                            'month': self.month})})
        Monthly.objects.filter(pk=self.pk).update(**kwargs)
        return
