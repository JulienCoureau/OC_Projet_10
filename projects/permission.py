from rest_framework import permissions
from .models import Contributor, Project, Issue, Comment

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission personnalisée : 
    - Autorise la lecture pour les utilisateurs connectés
    - n'autorise la modification ou la suppression que si l'uilisateur connecté est l'auteur """

    def has_object_permission(self, request, view, obj):
        # La requete est une simple lecture
        if request.method in permissions.SAFE_METHODS:
            return True
        # C'est une modification ou une supression, verifie l'identité, autorise si auteur = utilisateur
        return obj.author == request.user
    
class IsProjectContributor(permissions.BasePermission):
    """Verifie que l'utilisateur est contributeurt du projet associé à la ressource
    Fonctionne : Project, Issus, Comment"""

    def has_permission(self, request, view):
        """Verification : verifie accés au projet parent dès la liste"""
        # si pas de project ID dans l'url on est sur la racine / projects
        project_pk = view.kwargs.get("project_pk")
        if not project_pk:
            return True
        
        # sinon on vérifie que l'utilisateur est contributeur du projet
        return Contributor.objects.filter(
            project_id=project_pk, user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Recupère le projet selon le type d'objet
        if isinstance(obj, Project):
            project = obj
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project
        elif isinstance(obj, Contributor):
            project = obj.project
        else :
            return False
        
        # Verifie que l'utilisateur est contributeur de ce projet
        return Contributor.objects.filter(
            project=project, user=request.user
        ).exists()
    
class IsAdminOrSelf(permissions.BasePermission):
    """ Autorise l'accés si l'utilisateur connecté est un adminisstrateur ou si il consulte ses propres données"""
    def has_permission(self, request, view):
        user_pk = view.kwargs.get("user_pk")

        # Administrateur a accés à tout
        if request.user.is_staff:
            return True
        # L'utilisateur peut consulter que ses propres projets
        return str(request.user.pk) == (user_pk)