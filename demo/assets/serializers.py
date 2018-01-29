from rest_framework import serializers

from assets.models import Age, Breed, Color, Cow, Image

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        lookup_field = 'pk'
        fields = ('id', 'name')

    def get_initial(self):
        ages = Age.objects.all()
        if len(ages) > 0:
            return {'name': ages[0].name}
        else:
            return {'name': None}

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        lookup_field = 'pk'
        fields = ('id', 'name')

    def get_initial(self):
        breeds = Breed.objects.all()
        if len(breeds) > 0:
            return {'name': breeds[0].name}
        else:
            return {'name': None}

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        lookup_field = 'pk'
        fields = ('id', 'breed', 'name')

    def get_initial(self):
        colors = Color.objects.all()
        if len(colors) > 0:
            return {'name': colors[0].name,
                    'breed': colors[0].breed}
        else:
            return {'name': None}

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        lookup_field = 'pk'
        fields = ('id', 'breed', 'url')

    def get_initial(self):
        images = Image.objects.all()
        if len(images) > 0:
            return {'url': images[0].url}
        else:
            return {'url': None}

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        lookup_field = 'pk'
        fields = ('id', 'purchased_by', 'purchase_date', 'breed', 'color', 'age', 'image')

    def get_initial(self):
        return {'breed': Cow.breed.name,
                'color': Cow.color.name,
                'age': Cow.age.name,
                'image': Cow.image.name,
                'purchased_by': self.request.user}
