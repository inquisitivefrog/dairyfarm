from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from rest_framework.reverse import reverse

from assets.helpers import AssetTime

class Action(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return '{}'.format(self.name)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Age(models.Model):
    name = models.CharField(max_length=10,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return '{}'.format(self.name)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Color(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Breed(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=False)
    url = models.CharField(max_length=50,
                           null=False,
                           blank=False,
                           unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class CerealHay(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Cow(models.Model):
    rfid = models.UUIDField(default=uuid4(),
                            unique=True)
    purchased_by = models.ForeignKey(User,
                                     on_delete=models.CASCADE)
    purchase_date = models.DateField()
    age = models.ForeignKey(Age,
                            on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed,
                              on_delete=models.CASCADE)
    color = models.ForeignKey(Color,
                              on_delete=models.CASCADE)
    sell_date = models.DateField(null=False,
                                 default='2100-12-31')
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)
 
    def __str__(self):
        if self.id:
            return str(self.rfid)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  str(self.rfid))
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Cow, self).save(*args, **kwargs)
        tmp = []
        for word in self.breed.name.split(' '):
            tmp.append(word.lower())
        b_name = '_'.join(tmp)
        kwargs = {'link': reverse('assets:cow-detail',
                                  kwargs = {'pk': self.pk})}
        Cow.objects.filter(pk=self.pk).update(**kwargs)
        return

class Event(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            null=False,
                            on_delete=models.CASCADE)
    action = models.ForeignKey(Action,
                               null=False,
                               on_delete=models.CASCADE)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}'.format(self.recorded_by.username,
                                           self.timestamp,
                                           self.cow.rfid,
                                           self.action.name)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        kwargs = {'link': reverse('assets:event-detail',
                                  kwargs = {'pk': self.pk})}
        Event.objects.filter(pk=self.pk).update(**kwargs)
        return

class GrassHay(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Illness(models.Model):
    diagnosis = models.CharField(max_length=20,
                                 null=False,
                                 blank=False,
                                 unique=True)
    treatment = models.CharField(max_length=50,
                                 null=False,
                                 blank=False)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.diagnosis,
                                   self.treatment)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Injury(models.Model):
    diagnosis = models.CharField(max_length=20,
                                 null=False,
                                 blank=False,
                                 unique=True)
    treatment = models.CharField(max_length=40,
                                 null=False,
                                 blank=False,
                                 unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.diagnosis,
                                   self.treatment)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class LegumeHay(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Region(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)
    url = models.CharField(max_length=50,
                           null=False,
                           blank=False,
                           unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Season(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Status(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Treatment(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Vaccine(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return self.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class HealthRecord(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            on_delete=models.CASCADE)
    temperature = models.FloatField(default=1.00,
                                    null=False,
                                    blank=False)
    respiratory_rate = models.FloatField(default=1.00,
                                         null=False,
                                         blank=False)
    heart_rate = models.FloatField(default=1.00,
                                   null=False,
                                   blank=False)
    blood_pressure = models.FloatField(default=1.00,
                                       null=False,
                                       blank=False)
    weight = models.IntegerField(default=0,
                                 null=False,
                                 blank=False)
    body_condition_score = models.FloatField(default=1.00,
                                             null=False,
                                             blank=False)
    status = models.ForeignKey(Status,
                               on_delete=models.CASCADE)
    illness = models.ForeignKey(Illness,
                                null=True,
                                blank=False,
                                on_delete=models.CASCADE)
    injury = models.ForeignKey(Injury,
                               null=True,
                               blank=False,
                               on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine,
                                null=True,
                                blank=False,
                                on_delete=models.CASCADE)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def __str__(self):
        if self.id and self.illness:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                               self.timestamp,
                                                                               self.cow.age.name,
                                                                               self.cow.breed.name,
                                                                               self.cow.color.name,
                                                                               self.temperature,
                                                                               self.respiratory_rate,
                                                                               self.heart_rate,
                                                                               self.blood_pressure,
                                                                               self.weight,
                                                                               self.body_condition_score,
                                                                               self.status.name,
                                                                               self.illness.diagnosis)
        elif self.id and self.injury:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                               self.timestamp,
                                                                               self.cow.age.name,
                                                                               self.cow.breed.name,
                                                                               self.cow.color.name,
                                                                               self.temperature,
                                                                               self.respiratory_rate,
                                                                               self.heart_rate,
                                                                               self.blood_pressure,
                                                                               self.weight,
                                                                               self.body_condition_score,
                                                                               self.status.name,
                                                                               self.injury.diagnosis)
        elif self.id and self.vaccine:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                                   self.timestamp,
                                                                                   self.cow.age.name,
                                                                                   self.cow.breed.name,
                                                                                   self.cow.color.name,
                                                                                   self.temperature,
                                                                                   self.respiratory_rate,
                                                                                   self.heart_rate,
                                                                                   self.blood_pressure,
                                                                                   self.weight,
                                                                                   self.body_condition_score,
                                                                                   self.status.name,
                                                                                   self.illness.diagnosis,
                                                                                   self.vaccine.name)
        elif self.id:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                           self.timestamp,
                                                                           self.cow.age.name,
                                                                           self.cow.breed.name,
                                                                           self.cow.color.name,
                                                                           self.temperature,
                                                                           self.respiratory_rate,
                                                                           self.heart_rate,
                                                                           self.blood_pressure,
                                                                           self.weight,
                                                                           self.body_condition_score,
                                                                           self.status.name)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(HealthRecord, self).save(*args, **kwargs)
        kwargs = {'link': reverse('assets:healthrecord-detail',
                                  kwargs = {'pk': self.pk})}
        HealthRecord.objects.filter(pk=self.pk).update(**kwargs)
        return

class Milk(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            on_delete=models.CASCADE)
    gallons = models.SmallIntegerField(default=0)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                   self.timestamp,
                                                   self.cow.age.name,
                                                   self.cow.breed.name,
                                                   self.cow.color.name,
                                                   self.gallons)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Milk, self).save(*args, **kwargs)
        kwargs = {'link': reverse('assets:milk-detail',
                                  kwargs = {'pk': self.pk})}
        Milk.objects.filter(pk=self.pk).update(**kwargs)
        return

class Pasture(models.Model):
    fallow = models.BooleanField(default=False)
    distance = models.IntegerField(default=0,
                                   null=False,
                                   blank=False)
    year = models.SmallIntegerField(default=2015)
    season = models.ForeignKey(Season,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    seeded_by = models.ForeignKey(User,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE)
    region = models.ForeignKey(Region,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    cereal_hay = models.ForeignKey(CerealHay,
                                   null=True,
                                   blank=False,
                                   default=None,
                                   on_delete=models.CASCADE)
    grass_hay = models.ForeignKey(GrassHay,
                                  null=True,
                                  blank=False,
                                  default=None,
                                  on_delete=models.CASCADE)
    legume_hay = models.ForeignKey(LegumeHay,
                                   null=True,
                                   blank=False,
                                   default=None,
                                   on_delete=models.CASCADE)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def __str__(self):
        if self.id:
            return self.region.name
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Pasture, self).save(*args, **kwargs)
        tmp = []
        for word in self.region.name.split(' '):
            tmp.append(word.lower())
        r_name = '/{}.png'.format( '_'.join(tmp))
        kwargs = {'link': reverse('assets:pasture-detail',
                                  kwargs = {'pk': self.pk})}
        Pasture.objects.filter(pk=self.pk).update(**kwargs)
        return

class Exercise(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            on_delete=models.CASCADE)
    pasture = models.ForeignKey(Pasture,
                                on_delete=models.CASCADE)
    distance = models.IntegerField(default=0)
    link = models.URLField(max_length=50,
                           null=True,
                           blank=False)

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                       self.timestamp,
                                                       self.cow.age.name,
                                                       self.cow.breed.name,
                                                       self.cow.color.name,
                                                       self.pasture.region.name,
                                                       self.distance)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

    def save(self, *args, **kwargs):
        super(Exercise, self).save(*args, **kwargs)
        kwargs = {'link': reverse('assets:exercise-detail',
                                  kwargs = {'pk': self.pk})}
        Exercise.objects.filter(pk=self.pk).update(**kwargs)
        return
