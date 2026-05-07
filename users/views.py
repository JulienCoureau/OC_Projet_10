from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import User
from .serializers import UserSerializer


class IsSelfOrCreate(BasePermission):
    """ Autorise l'inscription (POST) pour tous
    Restreint la lecture, la modification et la suppression au propriétaire du compte """

    def has_permission(self, request, view):
        # POST (inscription) : accessible sans authentification
        if view.action == "create":
            return True
        # Toutes les autres actions : utilisateur doit être authentifié
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # On ne peut voir, modifier ou supprimer que son propre compte
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    """ API Endpoint utilisateur = Post / Get / Put / Delete"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrCreate]