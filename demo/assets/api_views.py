from django.contrib.auth.models import User
from django.db.models import Sum
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from assets.models import Action, Age, Breed, CerealHay, Client, Color, Cow
from assets.models import Event, Exercise, GrassHay, HealthRecord, Illness
from assets.models import Injury, LegumeHay, Milk, Pasture, Season, Seed
from assets.models import Status, Treatment, Vaccine
from assets.helpers import AssetTime
from assets.serializers import AgeSerializer, ActionSerializer, BreedSerializer
from assets.serializers import CerealHaySerializer, ColorSerializer
from assets.serializers import ClientSerializer, GrassHaySerializer
from assets.serializers import LegumeHaySerializer, SeasonSerializer
from assets.serializers import IllnessSerializer, InjurySerializer
from assets.serializers import StatusSerializer, TreatmentSerializer
from assets.serializers import UserSerializer, VaccineSerializer
from assets.serializers import CowReadSerializer, CowWriteSerializer
from assets.serializers import EventReadSerializer, EventWriteSerializer
from assets.serializers import ExerciseReadSerializer, ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer
from assets.serializers import MilkReadSerializer, MilkWriteSerializer
from assets.serializers import MilkSummaryReadSerializer
from assets.serializers import PastureReadSerializer, PastureWriteSerializer
from assets.serializers import SeedReadSerializer, SeedWriteSerializer

from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # Temporarily bypass CSRF for debugging

class ActionListView(generics.ListAPIView):
    # Get available actions
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(ActionListView, self).dispatch(*args, **kwargs)

class AgeListView(generics.ListAPIView):
    # Get available ages
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(AgeListView, self).dispatch(*args, **kwargs)

class BreedListView(generics.ListAPIView):
    # Get available cattle breeds
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(BreedListView, self).dispatch(*args, **kwargs)

class CerealListView(generics.ListAPIView):
    # Get available cereal hays
    queryset = CerealHay.objects.all()
    serializer_class = CerealHaySerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(CerealListView, self).dispatch(*args, **kwargs)

class ClientListView(generics.ListAPIView):
    # Get available clients
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(ClientListView, self).dispatch(*args, **kwargs)

class ColorListView(generics.ListAPIView):
    # Get available cattle breed colors
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(ColorListView, self).dispatch(*args, **kwargs)

class CowDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Get / Update /Destroy a Cow
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

class CowListView(generics.ListCreateAPIView):
    # Get / Purchase cows 
    queryset = Cow.objects.all().order_by('client');
    # authentication_classes = (CsrfExemptSessionAuthentication,
    #                           BasicAuthentication)

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return CowReadSerializer
        return CowWriteSerializer

class CowListByClientView(generics.ListCreateAPIView):
    # Get / Purchase cows 
    # authentication_classes = (CsrfExemptSessionAuthentication,
    #                           BasicAuthentication)

    def get_queryset(self):
        today = AssetTime.get_today()
        if self.kwargs:
            pk = self.kwargs['pk']
            return Cow.objects.filter(client_id=pk,
                                      sell_date__gte=today)
        return Cow.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return CowReadSerializer
        return CowWriteSerializer

class CowListByMonthView(generics.ListAPIView):
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

class CowListByYearView(generics.ListAPIView):
    # Get report of cows 
    serializer_class = CowReadSerializer

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            end_date = AssetTime.edate_year(year)
            return Cow.objects.filter(sell_date__gte=end_date,
                                      purchase_date__lte=end_date)
        return Cow.objects.all()

class EventDetailView(generics.RetrieveUpdateAPIView):
    # Get an Event
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class EventListView(generics.ListCreateAPIView):
    # Get / Create Event
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class EventListByClientView(generics.ListCreateAPIView):
    # Get / Create Event

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return Event.objects.filter(client_id=pk)
        return Event.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return EventReadSerializer
        return EventWriteSerializer

class ExerciseDetailView(generics.RetrieveUpdateAPIView):
    # Get an Exercise
    queryset = Exercise.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ExerciseReadSerializer
        return ExerciseWriteSerializer

class ExerciseListView(generics.ListCreateAPIView):
    # Get / Create Exercise
    queryset = Exercise.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ExerciseReadSerializer
        return ExerciseWriteSerializer

class ExerciseListByClientView(generics.ListCreateAPIView):
    # Get / Create Exercise

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return Exercise.objects.filter(client_id=pk)
        return Exercise.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ExerciseReadSerializer
        return ExerciseWriteSerializer

class GrassListView(generics.ListAPIView):
    # Get available grass hays
    queryset = GrassHay.objects.all()
    serializer_class = GrassHaySerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(GrassListView, self).dispatch(*args, **kwargs)

class IllnessListView(generics.ListAPIView):
    # Get available illnesses
    queryset = Illness.objects.all()
    serializer_class = IllnessSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(IllnessListView, self).dispatch(*args, **kwargs)

class InjuryListView(generics.ListAPIView):
    # Get available injuries
    queryset = Injury.objects.all()
    serializer_class = InjurySerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(InjuryListView, self).dispatch(*args, **kwargs)

class HealthRecordDetailView(generics.RetrieveUpdateAPIView):
    # Get / Update a HealthRecord
    queryset = HealthRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return HealthRecordReadSerializer
        return HealthRecordWriteSerializer

class HealthRecordListView(generics.ListCreateAPIView):
    # Get / Create HealthRecord
    queryset = HealthRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return HealthRecordReadSerializer
        return HealthRecordWriteSerializer

class HealthRecordListByClientView(generics.ListCreateAPIView):
    # Get / Create HealthRecord

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return HealthRecord.objects.filter(client_id=pk)
        return HealthRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return HealthRecordReadSerializer
        return HealthRecordWriteSerializer

class HealthRecordListByMonthView(generics.ListCreateAPIView):
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

class HealthRecordIllCowsSummaryView(generics.ListAPIView):
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

class LegumeListView(generics.ListAPIView):
    # Get available legume hays
    queryset = LegumeHay.objects.all()
    serializer_class = LegumeHaySerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(LegumeListView, self).dispatch(*args, **kwargs)

class MilkDetailView(generics.RetrieveUpdateAPIView):
    # Get a Milk
    queryset = Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class MilkListView(generics.ListCreateAPIView):
    # Get / Create Milk
    queryset = Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class MilkListByClientView(generics.ListCreateAPIView):
    # Get / Create Milk
    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return Milk.objects.filter(client_id=pk)
        return Milk.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MilkReadSerializer
        return MilkWriteSerializer

class MilkListByMonthView(generics.ListAPIView):
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

class MilkSummaryByMonthView(generics.ListAPIView):
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

class PastureDetailView(generics.RetrieveUpdateAPIView):
    # Get / Update a Seed
    queryset = Pasture.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return PastureReadSerializer
        return PastureWriteSerializer

class PastureListView(generics.ListCreateAPIView):
    # Get / Create pastures
    queryset = Pasture.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return PastureReadSerializer
        return PastureWriteSerializer

class PastureListByClientView(generics.ListCreateAPIView):
    # Get / Create pastures

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return Pasture.objects.filter(client_id=pk)
        return Pasture.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return PastureReadSerializer
        return PastureWriteSerializer

class SeasonListView(generics.ListAPIView):
    # Get available seasons
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(SeasonListView, self).dispatch(*args, **kwargs)

class SeedDetailView(generics.RetrieveUpdateAPIView):
    # Get / Update a Seed
    queryset = Seed.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return SeedReadSerializer
        return SeedWriteSerializer

class SeedListView(generics.ListCreateAPIView):
    # Get / Create pastures
    queryset = Seed.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return SeedReadSerializer
        return SeedWriteSerializer

class SeedListByClientView(generics.ListCreateAPIView):
    # Get / Create pastures

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            return Seed.objects.filter(client_id=pk)
        return Seed.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return SeedReadSerializer
        return SeedWriteSerializer

class StatusListView(generics.ListAPIView):
    # Get available statuses
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(StatusListView, self).dispatch(*args, **kwargs)

class TreatmentListView(generics.ListAPIView):
    # Get available treatments
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(TreatmentListView, self).dispatch(*args, **kwargs)
 
class UserListView(generics.ListAPIView):
    # Get and cache available users 
    queryset = User.objects.filter(is_active=True).values('id',
                                                          'username',
                                                          'first_name',
                                                          'last_name',
                                                          'email')
    serializer_class = UserSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

class VaccineListView(generics.ListAPIView):
    # Get available vaccines
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(VaccineListView, self).dispatch(*args, **kwargs)

