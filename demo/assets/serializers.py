from django.contrib.auth.models import User

from rest_framework import serializers

from assets.models import Action, Age, Breed, BreedImage, CerealHay, Color
from assets.models import Cow, Event, Exercise, GrassHay, HealthRecord
from assets.models import Illness, Injury, LegumeHay, Milk, Pasture
from assets.models import Region, Season, Status

class CowSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                slug_field='username')
    age = serializers.SlugRelatedField(queryset=Age.objects.all(),
                                       slug_field='name')
    breed = serializers.SlugRelatedField(queryset=Breed.objects.all(),
                                         slug_field='name')
    color = serializers.SlugRelatedField(queryset=Color.objects.all(),
                                        slug_field='name')
    image = serializers.SlugRelatedField(queryset=BreedImage.objects.all(),
                                         slug_field='url')

    class Meta:
        fields = ('id', 'purchased_by', 'purchase_date', 'age', 'breed',
                  'color', 'image', 'link')
        lookup_field = 'pk'
        model = Cow
        read_only_fields = ('link',)

class EventSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowSerializer(read_only=True)
    action = serializers.SlugRelatedField(queryset=Action.objects.all(),
                                          slug_field='name')

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'action', 'link')
        lookup_field = 'pk'
        model = Event
        read_only_fields = ('cow', 'link',)

class HealthRecordSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowSerializer(read_only=True)
    illness = serializers.SlugRelatedField(queryset=Illness.objects.all(),
                                           slug_field='diagnosis')
    injury = serializers.SlugRelatedField(queryset=Injury.objects.all(),
                                           slug_field='diagnosis')
    status = serializers.SlugRelatedField(queryset=Status.objects.all(),
                                          slug_field='name')

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'temperature',
                  'respiratory_rate', 'heart_rate', 'blood_pressure', 'weight',
                  'body_condition_score', 'status', 'illness', 'injury', 'link')
        lookup_field = 'pk'
        model = HealthRecord
        read_only_fields = ('link',)

class MilkSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowSerializer(read_only=True)

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'gallons', 'link')
        lookup_field = 'pk'
        model = Milk
        read_only_fields = ('link',)

class PastureSerializer(serializers.ModelSerializer):
    seeded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')
    cereal_hay = serializers.SlugRelatedField(queryset=CerealHay.objects.all(),
                                              slug_field='name')
    grass_hay = serializers.SlugRelatedField(queryset=GrassHay.objects.all(),
                                             slug_field='name')
    legume_hay = serializers.SlugRelatedField(queryset=LegumeHay.objects.all(),
                                             slug_field='name')
    region = serializers.SlugRelatedField(queryset=Region.objects.all(),
                                          slug_field='name')
    season = serializers.SlugRelatedField(queryset=Season.objects.all(),
                                          slug_field='name')

    class Meta:
        fields = ('id', 'fallow', 'seeded_by', 'image', 'region', 'cereal_hay',
                  'grass_hay', 'legume_hay', 'season', 'link')
        lookup_field = 'pk'
        model = Pasture
        read_only_fields = ('link',)

class ExerciseSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowSerializer(read_only=True)
    pasture = PastureSerializer(read_only=True)

    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'pasture',
                  'distance', 'link')
        read_only_fields = ('link',)
