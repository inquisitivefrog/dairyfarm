from rest_framework import serializers

from assets.models import BreedImage, Cow, Event, Exercise, HealthRecord
from assets.models import Milk, Pasture

class BreedImageField(serializers.RelatedField):
    def to_representation(self, value):
        return value.breed.name

class CowSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(slug_field='username',
                                                read_only=True)
    age = serializers.SlugRelatedField(slug_field='name',
                                       read_only=True)
    color= serializers.SlugRelatedField(slug_field='name',
                                        read_only=True)
    image = BreedImageField(read_only=True)

    class Meta:
        model = Cow
        lookup_field = 'pk'
        fields = ('id', 'purchased_by', 'purchase_date', 'age', 'color', 'image')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'action')

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'pasture', 'distance')

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'temperature',
                  'respiratory_rate', 'heart_rate', 'blood_pressure', 'weight',
                  'body_condition_score', 'status', 'illness', 'injury')

class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        lookup_field = 'pk'
        fields = ('id', 'recorded_by', 'timestamp', 'cow', 'gallons')

class PastureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasture
        lookup_field = 'pk'
        fields = ('id', 'fallow', 'seeded_by', 'image', 'cereal_hay', 'grass_hay',
                  'legume_hay', 'season')
