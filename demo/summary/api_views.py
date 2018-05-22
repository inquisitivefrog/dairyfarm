from django.db.models import Max

from rest_framework import generics

from summary.models import Annual, Monthly
from summary.serializers import AnnualReadSerializer
from summary.serializers import AnnualWriteSerializer
from summary.serializers import MonthlyReadSerializer
from summary.serializers import MonthlyWriteSerializer

class AnnualSummaryByClientView(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            if 'year' in self.kwargs:
                year = self.kwargs['year']
                return Annual.objects.filter(client_id=pk,
                                             year=year)
            else:
                return Annual.objects.filter(client_id=pk)
        return []

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return AnnualReadSerializer
        return AnnualWriteSerializer

class MonthlySummaryByClientView(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        if self.kwargs:
            pk = self.kwargs['pk']
            year = self.kwargs['year']
            if 'month' in self.kwargs:
                month = self.kwargs['month']
                objs = Monthly.objects.filter(client_id=pk,
                                              year=year,
                                              month=month)
                for o in objs:
                    o.month = o.get_month_display()
                return objs
            else:
                objs = Monthly.objects.filter(client_id=pk,
                                              year=year)
                for o in objs:
                    o.month = o.get_month_display()
                return objs
        return []

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return MonthlyReadSerializer
        return MonthlyWriteSerializer
