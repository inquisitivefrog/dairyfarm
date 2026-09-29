from django.contrib.auth.models import User

from demo.serializers import UserSerializer

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser

class UserCreate(CreateAPIView):
    '''
    Create a user from an authenticated staff-only workflow.
    '''
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

class UserDetail(RetrieveAPIView):
    '''
    Retrieve a user from an authenticated staff-only workflow.
    '''
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
