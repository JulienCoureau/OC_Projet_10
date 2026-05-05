from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet (viewsets.ModelViewSet) :
    """ API Endpoint qui permet de voir ou d'éditer les utilisateurs"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


