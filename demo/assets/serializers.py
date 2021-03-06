from django.contrib.auth.models import User

from rest_framework import serializers

from assets.models import Action, Age, Breed, CerealHay, Client, Color
from assets.models import Cow, Event, Exercise, GrassHay, HealthRecord
from assets.models import Illness, Injury, LegumeHay, Milk, Pasture
from assets.models import Season, Seed, Status, Treatment, Vaccine

# dependent serializers
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Action

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Age

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'url')
        lookup_field = 'pk'
        model = Breed

class ClientSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),
                                        slug_field='username')

    class Meta:
        fields = ('id', 'user', 'name', 'join_date', 'inactive_date')
        lookup_field = 'pk'
        model = Client

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Color

class CerealHaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = CerealHay

class GrassHaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = GrassHay

class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'diagnosis', 'treatment')
        lookup_field = 'pk'
        model = Illness

class InjurySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'diagnosis', 'treatment')
        lookup_field = 'pk'
        model = Injury

class LegumeHaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = LegumeHay

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Season

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Status

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Treatment 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        lookup_field = 'pk'
        model = User

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        lookup_field = 'pk'
        model = Vaccine

# independent serializers
class CowReadSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                slug_field='username')
    age = AgeSerializer(read_only=True)
    breed = BreedSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    color = ColorSerializer(read_only=True)

    class Meta:
        fields = ('id', 'rfid', 'client', 'purchased_by', 'purchase_date',
                  'age', 'breed', 'color', 'sell_date', 'link')
        lookup_field = 'pk'
        model = Cow
        read_only_fields = ('rfid', 'link',)

class CowWriteSerializer(serializers.ModelSerializer):
    purchased_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                                slug_field='username')
    age = serializers.SlugRelatedField(queryset=Age.objects.all(),
                                       slug_field='name')
    breed = serializers.SlugRelatedField(queryset=Breed.objects.all(),
                                         slug_field='name')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
    color = serializers.SlugRelatedField(queryset=Color.objects.all(),
                                         slug_field='name')

    class Meta:
        fields = ('id', 'rfid', 'client', 'purchased_by', 'purchase_date',
                  'age', 'breed', 'color', 'sell_date')
        lookup_field = 'pk'
        model = Cow

    def create(self, validated_data):
        age = validated_data.pop('age')
        breed = validated_data.pop('breed')
        client = validated_data.pop('client')
        color = validated_data.pop('color')
        cow = Cow.objects.create(age=age,
                                 breed=breed,
                                 client=client,
                                 color=color,
                                 **validated_data)
        return cow 
    
    # update() does not need to be overridden
    
class EventReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    client = ClientSerializer(read_only=True)
    cow = CowReadSerializer(read_only=True)
    action = ActionSerializer(read_only=True)

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'event_time', 'cow', 'action', 'link')
        lookup_field = 'pk'
        model = Event
        read_only_fields = ('link',)

class EventWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                       slug_field='rfid')
    action = serializers.SlugRelatedField(queryset=Action.objects.all(),
                                          slug_field='name')

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'event_time', 'cow', 'action')
        lookup_field = 'pk'
        model = Event

    def create(self, validated_data):
        client = validated_data.pop('client')
        cow = validated_data.pop('cow')
        action = validated_data.pop('action')
        event = Event.objects.create(client=client,
                                     cow=cow,
                                     action=action,
                                     **validated_data)
        return event
    
    # update() does not need to be overridden
    
class HealthRecordReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    client = ClientSerializer(read_only=True)
    cow = CowReadSerializer(read_only=True)
    illness = IllnessSerializer(read_only=True)
    injury = InjurySerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    treatment = TreatmentSerializer(read_only=True)
    vaccine = VaccineSerializer(read_only=True)

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'inspection_time', 'cow',
                  'temperature', 'respiratory_rate', 'heart_rate',
                  'blood_pressure', 'weight', 'body_condition_score', 'status',
                  'illness', 'injury', 'treatment', 'vaccine', 'link')
        lookup_field = 'pk'
        model = HealthRecord
        read_only_fields = ('link',)

class HealthRecordWriteSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
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
    treatment = serializers.SlugRelatedField(queryset=Treatment.objects.all(),
                                           slug_field='name',
                                           required=False)
    vaccine = serializers.SlugRelatedField(queryset=Vaccine.objects.all(),
                                           slug_field='name',
                                           required=False)

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'inspection_time', 'cow',
                  'temperature', 'respiratory_rate', 'heart_rate',
                  'blood_pressure', 'weight', 'body_condition_score', 'status',
                  'illness', 'injury', 'treatment', 'vaccine')
        lookup_field = 'pk'
        model = HealthRecord

    def create(self, validated_data):
        client = validated_data.pop('client')
        cow = validated_data.pop('cow')
        status = validated_data.pop('status')
        if 'illness' in validated_data: 
            illness = validated_data.pop('illness')
        else:
            illness = None
        if 'injury' in validated_data: 
            injury = validated_data.pop('injury')
        else:
            injury = None
        if 'treatment' in validated_data: 
            treatment = validated_data.pop('treatment')
        else:
            treatment = None
        if 'vaccine' in validated_data: 
            vaccine = validated_data.pop('vaccine')
        else:
            vaccine = None
        hr = HealthRecord.objects.create(client=client,
                                         cow=cow,
                                         illness=illness,
                                         injury=injury,
                                         status=status,
                                         treatment=treatment,
                                         vaccine=vaccine,
                                         **validated_data)
        return hr
    
    # update() does not need to be overridden
    
class MilkReadSerializer(serializers.ModelSerializer):
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    client = ClientSerializer(read_only=True)
    cow = CowReadSerializer(read_only=True)

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'milking_time', 'cow',
                  'gallons', 'link')
        lookup_field = 'pk'
        model = Milk
        read_only_fields = ('link',)

class MilkSummaryReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('gallons',)
        lookup_field = 'pk'
        model = Milk

class MilkWriteSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                       slug_field='rfid')

    class Meta:
        fields = ('id', 'client', 'recorded_by', 'milking_time', 'cow',
                  'gallons')
        lookup_field = 'pk'
        model = Milk

    def create(self, validated_data):
        client = validated_data.pop('client')
        cow = validated_data.pop('cow')
        milk = Milk.objects.create(client=client,
                                   cow=cow,
                                   **validated_data)
        return milk
    
    # update() does not need to be overridden

class PastureReadSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        fields = ('id', 'client', 'name', 'url', 'fallow', 'distance', 'link')
        lookup_field = 'pk'
        model = Pasture
        read_only_fields = ('link',)

class PastureWriteSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')

    class Meta:
        fields = ('id', 'client', 'name', 'url', 'fallow', 'distance')
        lookup_field = 'pk'
        model = Pasture

    def create(self, validated_data):
        client = validated_data.pop('client')
        pasture = Pasture.objects.create(client=client,
                                         **validated_data)
        return pasture
    
    # update() does not need to be overridden

class SeedReadSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    seeded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')
    pasture = PastureReadSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    cereal_hay = CerealHaySerializer(read_only=True)
    grass_hay = GrassHaySerializer(read_only=True)
    legume_hay = LegumeHaySerializer(read_only=True)

    class Meta:
        fields = ('id', 'client', 'seeded_by', 'pasture', 'season', 'year',
                  'cereal_hay', 'grass_hay', 'legume_hay', 'link')
        lookup_field = 'pk'
        model = Seed
        read_only_fields = ('link',)

class SeedWriteSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
    seeded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')
    pasture = serializers.SlugRelatedField(queryset=Pasture.objects.all(),
                                           slug_field='name')
    season = serializers.SlugRelatedField(queryset=Season.objects.all(),
                                          slug_field='name')
    cereal_hay = serializers.SlugRelatedField(queryset=CerealHay.objects.all(),
                                              slug_field='name')
    grass_hay = serializers.SlugRelatedField(queryset=GrassHay.objects.all(),
                                             slug_field='name')
    legume_hay = serializers.SlugRelatedField(queryset=LegumeHay.objects.all(),
                                              slug_field='name')

    class Meta:
        fields = ('id', 'client', 'seeded_by', 'pasture', 'season', 'year',
                  'cereal_hay', 'grass_hay', 'legume_hay')
        lookup_field = 'pk'
        model = Seed

    def create(self, validated_data):
        client = validated_data.pop('client')
        pasture = validated_data.pop('pasture')
        season = validated_data.pop('season')
        cereal_hay = validated_data.pop('cereal_hay')
        grass_hay = validated_data.pop('grass_hay')
        legume_hay = validated_data.pop('legume_hay')
        seeded_by = validated_data.pop('seeded_by')
        year = validated_data.pop('year')
        seed = Seed.objects.create(client=client,
                                   pasture=pasture,
                                   season=season,
                                   cereal_hay=cereal_hay,
                                   grass_hay=grass_hay,
                                   legume_hay=legume_hay,
                                   seeded_by=seeded_by,
                                   year=year)
                                   #**validated_data)
        return seed
    
    # update() does not need to be overridden

class ExerciseReadSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = CowReadSerializer(read_only=True)
    pasture = PastureReadSerializer(read_only=True)

    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'client', 'recorded_by', 'exercise_time', 'cow',
                  'pasture', 'link')
        read_only_fields = ('link',)

class ExerciseWriteSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
                                         slug_field='name')
    recorded_by = serializers.SlugRelatedField(queryset=User.objects.all(),
                                               slug_field='username')
    cow = serializers.SlugRelatedField(queryset=Cow.objects.all(),
                                       slug_field='rfid')
    pasture = serializers.SlugRelatedField(queryset=Pasture.objects.all(),
                                          slug_field='name')

    class Meta:
        model = Exercise
        lookup_field = 'pk'
        fields = ('id', 'client', 'recorded_by', 'exercise_time', 'cow',
                  'pasture')

    def create(self, validated_data):
        client = validated_data.pop('client')
        cow = validated_data.pop('cow')
        pasture = validated_data.pop('pasture')
        exercise = Exercise.objects.create(client=client,
                                           cow=cow,
                                           pasture=pasture,
                                           **validated_data)
        return exercise
    
    # update() does not need to be overridden
