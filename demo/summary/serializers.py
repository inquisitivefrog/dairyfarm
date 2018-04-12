from django.contrib.auth.models import User

from rest_framework import serializers

from summary.models import Annual, Monthly

# independent serializers
class AnnualReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')
    class Meta:
        fields = ('id', 'created_by', 'year', 'total_cows', 'aged_cows',
                  'pregnant_cows', 'ill_cows', 'injured_cows', 'gallons_milk',
                  'link')
        lookup_field = 'year'
        model = Annual
        read_only_fields = ('link',)

class AnnualWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')
    class Meta:
        fields = ('id', 'created_by', 'year')
        model = Annual

class MonthlyReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')
    class Meta:
        fields = ('id', 'created_by', 'year', 'month', 'total_cows',
                  'aged_cows', 'pregnant_cows', 'ill_cows', 'injured_cows',
                  'gallons_milk', 'link')
        lookup_field = 'pk'
        model = Monthly
        read_only_fields = ('link',)

class MonthlyWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')

    class Meta:
        fields = ('id', 'created_by', 'year', 'month')
        model = Monthly
