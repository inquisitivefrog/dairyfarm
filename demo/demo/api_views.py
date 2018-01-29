from django.contrib.auth.models import User

from demo.serializers import UserSerializer

from rest_framework.generics import CreateAPIView, RetrieveAPIView

class UserCreate(CreateAPIView):
    '''
    Create a User
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class UserDetail(RetrieveAPIView):
    '''
    Retrieve a User
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
