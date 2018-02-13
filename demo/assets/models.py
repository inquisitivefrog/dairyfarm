from django.contrib.auth.models import User
from django.db import models

class Action(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
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
                            unique=True)
    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class BreedImage(models.Model):
    breed = models.ForeignKey(Breed,
                              on_delete=models.CASCADE)
    url = models.CharField(max_length=50,
                           null=False,
                           blank=False,
                           unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}: {}'.format(self.breed.name,
                                       self.url,
                                       self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Color(models.Model):
    breed = models.ForeignKey(Breed,
                              null=True,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.breed.name,
                                   self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Cow(models.Model):
    purchased_by = models.ForeignKey(User,
                                     on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=False)
    age = models.ForeignKey(Age,
                            on_delete=models.CASCADE)
    color = models.ForeignKey(Color,
                              on_delete=models.CASCADE)
    image = models.ForeignKey(BreedImage,
                              on_delete=models.CASCADE)
 
    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}'.format(self.age.name,
                                           self.color.name,
                                           self.image.breed.name,
                                           self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Event(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            on_delete=models.CASCADE)
    action = models.ForeignKey(Action,
                               on_delete=models.CASCADE)

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                               self.timestamp,
                                               self.cow,
                                               self.action.name,
                                               self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class GrassHay(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.id)
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
                                   self.treatment,
                                   self.id)
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
                                   self.treatment,
                                   self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
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

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class RegionImage(models.Model):
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE)
    url = models.CharField(max_length=50,
                           null=False,
                           blank=False,
                           unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}: {}'.format(self.region.name,
                                       self.url,
                                       self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Season(models.Model):
    name = models.CharField(max_length=10,
                            null=False,
                            blank=False,
                            unique=True)

    def __str__(self):
        if self.id:
            return '{}: {}'.format(self.name,
                                   self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
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
            return '{}: {}'.format(self.name,
                                   self.id)
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
    timestamp = models.DateTimeField('%Y-%m-%d %H:%M:%S')
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

    def __str__(self):
        if self.id and self.illness:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                           self.timestamp,
                                                                           self.cow,
                                                                           self.temperature,
                                                                           self.respiratory_rate,
                                                                           self.heart_rate,
                                                                           self.blood_pressure,
                                                                           self.weight,
                                                                           self.body_condition_score,
                                                                           self.status.name,
                                                                           self.illness.diagnosis,
                                                                           self.id)
        elif self.id and self.injury:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                           self.timestamp,
                                                                           self.cow,
                                                                           self.temperature,
                                                                           self.respiratory_rate,
                                                                           self.heart_rate,
                                                                           self.blood_pressure,
                                                                           self.weight,
                                                                           self.body_condition_score,
                                                                           self.status.name,
                                                                           self.injury.diagnosis,
                                                                           self.id)
        elif self.id and self.vaccine:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                               self.timestamp,
                                                                               self.cow,
                                                                               self.temperature,
                                                                               self.respiratory_rate,
                                                                               self.heart_rate,
                                                                               self.blood_pressure,
                                                                               self.weight,
                                                                               self.body_condition_score,
                                                                               self.status.name,
                                                                               self.illness.diagnosis,
                                                                               self.vaccine.name,
                                                                               self.id)
        elif self.id:
            return '{}: {}: {}: {}: {}: {}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                                       self.timestamp,
                                                                       self.cow,
                                                                       self.temperature,
                                                                       self.respiratory_rate,
                                                                       self.heart_rate,
                                                                       self.blood_pressure,
                                                                       self.weight,
                                                                       self.body_condition_score,
                                                                       self.status.name,
                                                                       self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Milk(models.Model):
    recorded_by = models.ForeignKey(User,
                                    null=False,
                                    blank=False,
                                    on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow,
                            on_delete=models.CASCADE)
    gallons = models.SmallIntegerField(default=0)

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                               self.timestamp,
                                               self.cow,
                                               self.gallons,
                                               self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

class Pasture(models.Model):
    fallow = models.BooleanField(default=False)
    distance = models.IntegerField(default=0,
                                   null=False,
                                   blank=False)
    seeded_by = models.ForeignKey(User,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE)
    image = models.ForeignKey(RegionImage,
                              null=True,
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
    season = models.ForeignKey(Season,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)

    def __str__(self):
        if self.id:
            if self.fallow:
                return '{}: {}: {}: {}'.format(self.fallow,
                                               self.seeded_by.username,
                                               self.image.region.name,
                                               self.season.name,
                                               self.id)
            else:
                return '{}: {}: {}: {}: {}: {}: {}'.format(self.seeded_by.username,
                                                           self.image.region.name,
                                                           self.cereal_hay.name,
                                                           self.grass_hay.name,
                                                           self.legume_hay.name,
                                                           self.season.name,
                                                           self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)

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

    def __str__(self):
        if self.id:
            return '{}: {}: {}: {}: {}: {}'.format(self.recorded_by.username,
                                                   self.timestamp,
                                                   self.cow,
                                                   self.pasture.image.region.name,
                                                   self.distance,
                                                   self.id)
        else:
            return '{}'.format(self.__class__)

    def __repr__(self):
        if self.id:
            return '{}:{}'.format(self.__class__,
                                  self.id)
        else:
            return '{}'.format(self.__class__)
