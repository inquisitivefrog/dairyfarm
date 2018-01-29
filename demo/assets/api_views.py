from django.views.defaults import bad_request

from rest_framework import generics

from assets.models import Age, Breed, Color, Cow, Image
from assets.serializers import AgeSerializer, BreedSerializer, CowSerializer
from assets.serializers import ColorSerializer, CowSerializer, ImageSerializer

class AgeDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Age 
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

class AgeList(generics.ListCreateAPIView):
    # Get / Create ages
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

class BreedDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Breed
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class BreedList(generics.ListCreateAPIView):
    # Get / Create breeds 
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class ColorDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Color
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ColorList(generics.ListCreateAPIView):
    # Get / Create colors 
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(ColorList, self).create(request, *args, **kwargs)
        except IntegrityError:
            return bad_request(request)

class CowDetail(generics.RetrieveUpdateAPIView):
    # Get / Update a Cow
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

class CowList(generics.ListCreateAPIView):
    # Get / Create cows 
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

class ImageDetail(generics.RetrieveUpdateAPIView):
    # Get / Update an Image
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageList(generics.ListCreateAPIView):
    # Get / Create images
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
