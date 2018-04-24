from django.db.models import Sum

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from assets.models import Cow, Event, Exercise, HealthRecord
from assets.models import Milk, Pasture, Seed
from assets.helpers import AssetTime
from assets.serializers import CowReadSerializer, CowWriteSerializer
from assets.serializers import EventReadSerializer, EventWriteSerializer
from assets.serializers import ExerciseReadSerializer, ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer
from assets.serializers import MilkReadSerializer, MilkWriteSerializer
from assets.serializers import MilkSummaryReadSerializer
from assets.serializers import PastureReadSerializer, PastureWriteSerializer
from assets.serializers import SeedReadSerializer, SeedWriteSerializer

class CowDetail(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update a Cow
    queryset = Cow.objects.all()

    def delete(self, *args, **kwargs):
        if self.kwargs:
            pk = self.kwargs['pk']
            kwargs = {'sell_date': AssetTime.get_today()}
            Cow.objects.filter(pk=pk).update(**kwargs)
            instance = Cow.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_BAD_REQUEST)

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
            end_date = AssetTime.edate_year_month(year, month)
            return Cow.objects.filter(sell_date__gte=end_date,
                                      purchase_date__lte=end_date)
        return Cow.objects.all()

class CowListByYear(generics.ListAPIView):
    # Get report of cows 
    serializer_class = CowReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            end_date = AssetTime.edate_year(year)
            return Cow.objects.filter(sell_date__gte=end_date,
                                      purchase_date__lte=end_date)
        return Cow.objects.all()

class EventDetail(generics.RetrieveAPIView):
    # Get an Event
    queryset = Event.objects.all()
    serializer_class = EventReadSerializer

class EventList(generics.ListCreateAPIView):
    # Get / Create Event
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class ExerciseDetail(generics.RetrieveAPIView):
    # Get an Exercise
    queryset = Exercise.objects.all()
    serializer_class = ExerciseReadSerializer

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

class HealthRecordListByMonth(generics.ListCreateAPIView):
    # Get report of cow health records
    serializer_class = HealthRecordReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            start_date = AssetTime.sdate_year_month(year, month)
            end_date = AssetTime.edate_year_month(year, month)
            return HealthRecord.objects.filter(inspection_time__gte=start_date,
                                               inspection_time__lte=end_date).order_by('cow')
        print('no kwargs')
        return HealthRecord.objects.all()

class HealthRecordIllCowsSummary(generics.ListAPIView):
    # Get summary of ill cows
    serializer_class = HealthRecordReadSerializer
    pagination_class = None

    def get_queryset(self):
        illnesses = ['Bacterial Illness', 'Viral Illness']
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            sdate = AssetTime.sdate_year_month(year, month)
            edate = AssetTime.edate_year_month(year, month)
          
            total_cows = HealthRecord.objects.filter(status__name__in=illnesses,
                                                     inspection_time__gte=sdate,
                                                     inspection_time__lte=edate).count()
        else:
            total_cows = HealthRecord.objects.all().count()
        print('total cows: {}'.format(total_cows))
        return [{'status': total_cows}]

class MilkDetail(generics.RetrieveAPIView):
    # Get a Milk
    queryset = Milk.objects.all()
    serializer_class = MilkReadSerializer

class MilkList(generics.ListCreateAPIView):
    # Get / Create Milk
    queryset = Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class MilkListByMonth(generics.ListAPIView):
    # Get list of milk production by month
    serializer_class = MilkReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            start_date = AssetTime.sdate_year_month(year, month)
            end_date = AssetTime.edate_year_month(year, month)
            return Milk.objects.filter(milking_time__gte=start_date,
                                       milking_time__lte=end_date)
        return Milk.objects.all()

class MilkSummaryByMonth(generics.ListAPIView):
    # Get summary of milk production
    serializer_class = MilkSummaryReadSerializer
    pagination_class = None

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            start_date = AssetTime.sdate_year_month(year, month)
            end_date = AssetTime.edate_year_month(year, month)
            total_gallons = Milk.objects.filter(milking_time__gte=start_date,
                                                milking_time__lte=end_date).aggregate(Sum('gallons'))['gallons__sum']
        else:
            total_gallons = (Milk.objects.all().aggregate(Sum('gallons')))
        return [{'gallons': total_gallons}]

class PastureDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Seed
    queryset = Pasture.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return PastureReadSerializer
        return PastureWriteSerializer

class PastureList(generics.ListCreateAPIView):
    # Get / Create pastures
    queryset = Pasture.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return PastureReadSerializer
        return PastureWriteSerializer

class SeedDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Seed
    queryset = Seed.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return SeedReadSerializer
        return SeedWriteSerializer

class SeedList(generics.ListCreateAPIView):
    # Get / Create pastures
    queryset = Seed.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return SeedReadSerializer
        return SeedWriteSerializer
