from django.contrib.auth.models import User
from django.db import models

class Age(models.Model):
    name = models.CharField(max_length=10,
                            null=False,
                            blank=False,
                            unique=True)

    def __unicode__(self):
        return '{}: {}'.format(self.age, self.id)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Breed(models.Model):
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)

    def __unicode__(self):
        return '{}: {}'.format(self.breed, self.id)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Color(models.Model):
    breed = models.ForeignKey(Breed,
                              null=True,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False)

    def __unicode__(self):
        return '{}: {}'.format(self.color, self.id)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Image(models.Model):
    breed = models.ForeignKey(Breed,
                              on_delete=models.CASCADE)
    url = models.CharField(max_length=50,
                           null=False,
                           blank=False,
                           unique=True)

    def __unicode__(self):
        return '{}: {}'.format(self.url, self.id)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Cow(models.Model):
    purchased_by = models.ForeignKey(User,
                                     on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    age = models.ForeignKey(Age,
                            on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed,
                              on_delete=models.CASCADE)
    color = models.ForeignKey(Color,
                              on_delete=models.CASCADE)
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE)
 
    def __unicode__(self):
        return '{}: {}'.format(self.breed, self.id)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)
