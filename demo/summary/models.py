from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from rest_framework.reverse import django_reverse

from assets.models import Client, Cow, HealthRecord, Milk

from summary.constants import JAN, MONTHS, YEARS, Y2015
from summary.helpers import ReportTime, ReportStats

class Annual(models.Model):
    client = models.ForeignKey(Client,
                               null=True,
                               on_delete=models.CASCADE)
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
        kwargs = {'created_by': self.created_by,
                  'total_cows': ReportStats.get_total_cows(self.client,
                                                           self.year),
                  'aged_cows': ReportStats.get_aged_cows(self.client,
                                                         self.year),
                  'pregnant_cows': ReportStats.get_pregnant_cows(self.client,
                                                                 self.year),
                  'ill_cows': ReportStats.get_ill_cows(self.client,
                                                       self.year),
                  'injured_cows': ReportStats.get_injured_cows(self.client,
                                                                  self.year),
                  'gallons_milk': ReportStats.get_gallons_milk(self.client,
                                                               self.year)}
        try:
            self.instance = Annual.objects.get(client=self.client,
                                               year=self.year)
            Annual.objects.filter(pk=self.instance.pk).update(**kwargs)
            return
        except Annual.DoesNotExist:
            super(Annual, self).save()
            view_name = 'summary:monthly-client-year'
            kwargs.update({'client': self.client,
                           'link': django_reverse(view_name,
                                                  kwargs = {'pk': self.client.pk,
                                                            'year': self.year})})
            Annual.objects.filter(pk=self.pk).update(**kwargs)
            return

class Monthly(models.Model):
    client = models.ForeignKey(Client,
                               null=True,
                               on_delete=models.CASCADE)
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
        kwargs = {'created_by': self.created_by,
                  'total_cows': ReportStats.get_total_cows(self.client,
                                                           self.year,
                                                           self.month),
                  'aged_cows': ReportStats.get_aged_cows(self.client,
                                                         self.year,
                                                         self.month),
                  'pregnant_cows': ReportStats.get_pregnant_cows(self.client,
                                                                 self.year,
                                                                 self.month),
                  'ill_cows': ReportStats.get_ill_cows(self.client,
                                                       self.year,
                                                       self.month),
                  'injured_cows': ReportStats.get_injured_cows(self.client,
                                                               self.year,
                                                               self.month),
                  'gallons_milk': ReportStats.get_gallons_milk(self.client,
                                                               self.year,
                                                               self.month)}
        try:
            self.instance = Monthly.objects.get(client=self.client,
                                                year=self.year,
                                                month=self.month)
            Monthly.objects.filter(pk=self.instance.pk).update(**kwargs)
            return
        except Monthly.DoesNotExist:
            super(Monthly, self).save()
            view_name = 'summary:monthly-client-year-month'
            if self.month < 10:
                month = '0{}'.format(self.month)
                kwargs.update({'client': self.client,
                               'link': django_reverse(view_name,
                                                      kwargs = {'pk': self.client.pk,
                                                                'year': self.year,
                                                                'month': month})})
            else:
                kwargs.update({'client': self.client,
                               'link': django_reverse(view_name,
                                                      kwargs = {'pk': self.client.pk,
                                                                'year': self.year,
                                                                'month': self.month})})
            Monthly.objects.filter(pk=self.pk).update(**kwargs)
            return
