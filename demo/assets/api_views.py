from django.views.defaults import bad_request

from rest_framework import generics

from assets.models import Cow, Event, Exercise, HealthRecord, Milk, Pasture
from assets.serializers import CowSerializer, EventSerializer
from assets.serializers import ExerciseSerializer, HealthRecordSerializer
from assets.serializers import MilkSerializer, PastureSerializer

class CowDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Cow
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

class CowList(generics.ListCreateAPIView):
    # Get / Create cows 
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

    #def get_initial(self):
    #    return {'purchased_by': self.request.user.username,
    #            'age': self.age.name,
    #            'color': self.color.name,
    #            'image': self.image.name}

class EventDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventList(generics.ListCreateAPIView):
    # Get / Create Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    #def get_initial(self):
    #    return {'recorded_by': self.request.user.username,
    #            'timestamp': self.timestamp,
    #            'cow': self.cow,
    #            'pasture': self.pasture,
    #            'distance': self.distance}

class ExerciseDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Exercise
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseList(generics.ListCreateAPIView):
    # Get / Create Exercise
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    #def get_initial(self):
    #    return {'recorded_by': self.request.user.username,
    #            'timestamp': self.timestamp,
    #            'cow': self.cow,
    #            'pasture': self.pasture,
    #            'distance': self.distance}

class HealthRecordDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a HealthRecord
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

class HealthRecordList(generics.ListCreateAPIView):
    # Get / Create HealthRecord
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

    #def get_initial(self):
    #    return {'recorded_by': self.request.user,
    #            'timestamp': self.timestamp,
    #            'cow': self.cow,
    #            'temperature': self.temperature,
    #            'respiratory_rate': self.respiratory_rate,
    #            'heart_rate': self.heart_rate,
    #            'blood_pressure': self.blood_pressure,
    #            'weight': self.weight,
    #            'body_condition_score': self.body_condition_score,
    #            'status': self.status.name,
    #            'illness': self.illness.diagnosis,
    #            'injury': self.injury.diagnosis}

class MilkDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Milk
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer

class MilkList(generics.ListCreateAPIView):
    # Get / Create Milk
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer

    #def get_initial(self):
    #    return {'recorded_by': self.request.user.username,
    #            'timestamp': self.timestamp,
    #            'cow': self.cow,
    #            'gallons': self.gallons}

class PastureDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Pasture
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer

class PastureList(generics.ListCreateAPIView):
    # Get / Create pastures 
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer

    #def get_initial(self):
    #    return {'seeded_by': self.request.user.username,
    #            'image': self.image.region.name,
    #            'cereal_hay': self.cereal_hay.name,
    #            'grass_hay': self.grass_hay.name,
    #            'legume_hay': self.legume_hay.name,
    #            'season': self.season.name}

