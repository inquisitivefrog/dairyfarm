from django.contrib.auth.models import User

from rest_framework import serializers

from assets.models import Client
from summary.models import Annual, Monthly

# independent serializers
class AnnualReadSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                          slug_field='name')
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')
    class Meta:
        fields = ('id', 'client', 'created_by', 'year', 'total_cows', 'aged_cows',
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

    def create(self, validated_data):
        created_by = validated_data.pop('created_by')
        client = Client.objects.get(user=created_by)
        year = validated_data.pop('year')
        return Annual.objects.create(created_by=created_by,
                                     client=client,
                                     year=year,
                                     **validated_data)

class MonthlyReadSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                          slug_field='name')
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                              slug_field='username')
    class Meta:
        fields = ('id', 'client', 'created_by', 'year', 'month', 'total_cows',
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

    def create(self, validated_data):
        created_by = validated_data.pop('created_by')
        client = Client.objects.get(user=created_by)
        year = validated_data.pop('year')
        month = validated_data.pop('month')
        return Monthly.objects.create(created_by=created_by,
                                      client=client,
                                      year=year,
                                      month=month,
                                      **validated_data)
