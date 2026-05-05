from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer,)
from .permission import IsAuthorOrReadOnly, IsProjectContributor



class ProjectViewSet (viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    # utilisateur connecté et respecte la regle auteur
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """ Filtre les projets pour ne retourner que ceux que l'utlisateur connecté est soit l'auteur soit un contributeur"""
        # Identité de l'utilisateur qui fait la requête
        user = self.request.user
        # Filtre BDD
        return Project.objects.filter(
            # condition 1 : il est auteur
            Q(author=user) |
            # COndition 2 : il est dans la liste des contributeurs du projet
            Q(contributors__user=user)
        ).select_related("author").prefetch_related("contributors").distinct() 

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ne retourne que les contributeurs des projets ou l'utilisateur participe"""
        user = self.request.user
        return Contributor.objects.filter(
            project__contributors__user=user
        ).select_related("user","project").distinct()

class IssueViewSet (viewsets.ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor,IsAuthorOrReadOnly]

    def get_queryset(self):
        """ Ne retroune que les Issue des projets dont l'utilisateur est contributeur"""
        user = self.request.user
        return Issue.objects.filter(
            project__contributors__user=user
        ).select_related("project","author","assignee").distinct()
    # Auteur est l'utilisateur connecté lors de la création
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class CommentViewSet(viewsets.ModelViewSet): 
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """ Ne retourne que les comments des issues ou l'itulisateur est contributeur"""
        user = self.request.user
        return Comment.objects.filter(
            issue__project__contributors__user=user
        ).select_related("issue","author").distinct()
    # Auteur est l'utilisateur connecté lors de la création
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

        