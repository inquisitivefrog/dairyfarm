from django.views.defaults import bad_request

from rest_framework import generics

from assets.models import Cow, Event, Exercise, HealthRecord, Milk, Pasture
from assets.serializers import CowSerializer, EventReadSerializer
from assets.serializers import EventWriteSerializer, ExerciseReadSerializer
from assets.serializers import ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer
from assets.serializers import MilkReadSerializer, MilkWriteSerializer
from assets.serializers import PastureSerializer

class CowDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Cow
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

class CowList(generics.ListCreateAPIView):
    # Get / Create cows 
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

class EventDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Event
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class EventList(generics.ListCreateAPIView):
    # Get / Create Event
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class ExerciseDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Exercise
    queryset = Exercise.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ExerciseReadSerializer
        return ExerciseWriteSerializer

class ExerciseList(generics.ListCreateAPIView):
    # Get / Create Exercise
    queryset = Exercise.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ExerciseReadSerializer
        return ExerciseWriteSerializer

class HealthRecordDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a HealthRecord
    queryset = HealthRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return HealthRecordReadSerializer
        return HealthRecordWriteSerializer

class HealthRecordList(generics.ListCreateAPIView):
    # Get / Create HealthRecord
    queryset = HealthRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return HealthRecordReadSerializer
        return HealthRecordWriteSerializer

class MilkDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Milk
    queryset = Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class MilkList(generics.ListCreateAPIView):
    # Get / Create Milk
    queryset = Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class PastureDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Pasture
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer

class PastureList(generics.ListCreateAPIView):
    # Get / Create pastures 
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer
