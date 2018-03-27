from django.contrib.auth.models import User

from rest_framework import serializers

from assets.models import Action, Age, Breed, CerealHay, Color
from assets.models import Cow, Event, Exercise, GrassHay, HealthRecord
from assets.models import Illness, Injury, LegumeHay, Milk, Pasture
from assets.models import Region, Season, Status, Vaccine

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Action
        read_only_fields = ('id', 'name')

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Age
        read_only_fields = ('id', 'name')

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'url')
        lookup_field = 'pk'
        model = Breed
        read_only_fields = ('id', 'name', 'url')

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Color
        read_only_fields = ('id', 'name')

class CowReadSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                slug_field='username')
    age = AgeSerializer(read_only=True)
    breed = BreedSerializer(read_only=True)
    color = ColorSerializer(read_only=True)

    class Meta:
        fields = ('id', 'rfid', 'purchased_by', 'purchase_date', 'age',
                  'breed', 'color', 'sell_date', 'link')
        lookup_field = 'pk'
        model = Cow
        read_only_fields = ('link',)

class CowWriteSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                slug_field='username')
    age = serializers.SlugRelatedField(queryset=Age.objects.all(),
                                       slug_field='name')
    breed = serializers.SlugRelatedField(queryset=Breed.objects.all(),
                                         slug_field='name')
    color = serializers.SlugRelatedField(queryset=Color.objects.all(),
                                         slug_field='name')

    class Meta:
        fields = ('id', 'rfid', 'purchased_by', 'purchase_date', 'age',
                  'breed', 'color')
        lookup_field = 'pk'
        model = Cow
        read_only_fields = ('rfid', 'link')

    def create(self, validated_data):
        age = validated_data.pop('age')
        breed = validated_data.pop('breed')
        color = validated_data.pop('color')
        cow = Cow.objects.create(age=age,
                                 breed=breed,
                                 color=color,
                                 **validated_data)
        return cow 
    
    # update() does not need to be overridden
    
class EventReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowReadSerializer(read_only=True)
    action = ActionSerializer(read_only=True)

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'action', 'link')
        lookup_field = 'pk'
        model = Event
        read_only_fields = ('link',)

class EventWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                          slug_field='rfid')
    action = serializers.SlugRelatedField(queryset=Action.objects.all(),
                                          slug_field='name')

    class Meta:
        fields = ('id', 'recorded_by', 'cow', 'action')
        lookup_field = 'pk'
        model = Event

    def create(self, validated_data):
        cow = validated_data.pop('cow')
        event = Event.objects.create(cow=cow, **validated_data)
        return event
    
    # update() does not need to be overridden
    
class HealthRecordReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowReadSerializer(read_only=True)
    illness = serializers.SlugRelatedField(queryset=Illness.objects.all(),
                                           slug_field='diagnosis',
                                           required=False)
    injury = serializers.SlugRelatedField(queryset=Injury.objects.all(),
                                           slug_field='diagnosis',
                                           required=False)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(),
                                          slug_field='name')
    vaccine = serializers.SlugRelatedField(queryset=Vaccine.objects.all(),
                                           slug_field='name')

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'temperature',
                  'respiratory_rate', 'heart_rate', 'blood_pressure', 'weight',
                  'body_condition_score', 'status', 'illness', 'injury',
                  'vaccine', 'link')
        lookup_field = 'pk'
        model = HealthRecord
        read_only_fields = ('link',)

class HealthRecordWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                          slug_field='rfid')
    illness = serializers.SlugRelatedField(queryset=Illness.objects.all(),
                                           slug_field='diagnosis',
                                           required=False)
    injury = serializers.SlugRelatedField(queryset=Injury.objects.all(),
                                           slug_field='diagnosis',
                                           required=False)
    status = serializers.SlugRelatedField(queryset=Status.objects.all(),
                                          slug_field='name')
    vaccine = serializers.SlugRelatedField(queryset=Vaccine.objects.all(),
                                           slug_field='name',
                                           required=False)

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'temperature',
                  'respiratory_rate', 'heart_rate', 'blood_pressure', 'weight',
                  'body_condition_score', 'status', 'illness', 'injury',
                  'vaccine', 'link')
        lookup_field = 'pk'
        model = HealthRecord

class MilkReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowReadSerializer(read_only=True)

    class Meta:
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'gallons', 'link')
        lookup_field = 'pk'
        model = Milk
        read_only_fields = ('link',)

class MilkWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                          slug_field='rfid')

    class Meta:
        fields = ('id', 'recorded_by', 'cow', 'gallons')
        lookup_field = 'pk'
        model = Milk

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
        fields = ('id', 'fallow', 'distance', 'seeded_by', 'region',
                  'year', 'season', 'cereal_hay', 'grass_hay', 'legume_hay', 'link')
        lookup_field = 'pk'
        model = Pasture
        read_only_fields = ('link',)

class ExerciseReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowReadSerializer(read_only=True)
    pasture = PastureSerializer(read_only=True)

    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'pasture',
                  'distance', 'link')
        read_only_fields = ('link',)

class ExerciseWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                          slug_field='rfid')
    pasture = serializers.SlugRelatedField(queryset=Pasture.objects.all(),
                                          slug_field='region_id')

    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'cow', 'pasture', 'distance')
