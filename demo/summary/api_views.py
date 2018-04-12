from django.db.models import Max

from rest_framework import generics

from summary.models import Annual, Monthly
from summary.serializers import AnnualReadSerializer
from summary.serializers import AnnualWriteSerializer
from summary.serializers import MonthlyReadSerializer
from summary.serializers import MonthlyWriteSerializer

class AnnualSummary(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            obj = Annual.objects.filter(year=year).aggregate(Max('id'))
            return Annual.objects.filter(id=obj['id__max'])
        return Annual.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return AnnualReadSerializer
        return AnnualWriteSerializer

class MonthlySummary(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        if self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            obj = Monthly.objects.filter(year=year,
                                         month=month).aggregate(Max('id'))
            return Monthly.objects.filter(id=obj['id__max'])
        return Monthly.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MonthlyReadSerializer
        return MonthlyWriteSerializer
