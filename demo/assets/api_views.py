from django.views.defaults import bad_request

from rest_framework import generics

from assets.models import Cow, Event, Exercise, HealthRecord, Milk, Pasture
from assets.helpers import AssetTime
from assets.serializers import CowReadSerializer, CowWriteSerializer, EventReadSerializer
from assets.serializers import EventWriteSerializer, ExerciseReadSerializer
from assets.serializers import ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer
from assets.serializers import MilkReadSerializer, MilkWriteSerializer
from assets.serializers import PastureSerializer

class CowDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update a Cow
    queryset = Cow.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return CowReadSerializer
        return CowWriteSerializer

class CowList(generics.ListCreateAPIView):
    # Get / Create cows 
    queryset = Cow.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return CowReadSerializer
        return CowWriteSerializer

class CowListByMonth(generics.ListAPIView):
    # Get report of cows 
    serializer_class = CowReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            start_date = AssetTime.sdate_year_month(year, month)
            end_date = AssetTime.edate_year_month(year, month)
            print('start_date: {}'.format(start_date))
            print('end_date: {}'.format(end_date))
            return Cow.objects.filter(sell_date__gt=end_date,
                                      purchase_date__lte=start_date)
        return Cow.objects.all()

class CowListByYear(generics.ListAPIView):
    # Get report of cows 
    serializer_class = CowReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            start_date = AssetTime.sdate_year(year)
            end_date = AssetTime.edate_year(year)
            print('start_date: {}'.format(start_date))
            print('end_date: {}'.format(end_date))
            return Cow.objects.filter(sell_date__gte=end_date,
                                      purchase_date__lte=start_date)
        return Cow.objects.all()

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update / Destroy an Event
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

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update / Destroy an Exercise
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

class HealthRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update / Destroy a HealthRecord
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

class MilkDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update a Milk
    # Get / Update / Destroy a Milk
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

class PastureDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update / Destroy a Pasture
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer

class PastureList(generics.ListCreateAPIView):
    # Get / Create pastures 
    queryset = Pasture.objects.all()
    serializer_class = PastureSerializer
