from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer,)
from .permission import IsAuthorOrReadOnly, IsProjectContributor, IsAdminOrSelf

class ProjectViewSet (viewsets.ModelViewSet):
    """ Endpoint racine : Liste les projets dont l'utilisateur est auteur ou contributeur"""

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
    
    def perform_create(self, serializer):
        """A la creation d'un projet, l'auteur est l'utilisateur connecté et il devient contributeur"""
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project) 

class ContributorViewSet(viewsets.ModelViewSet):
    """ Endpoint imbriqué : Liste les contributeurs d'un projet"""
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_project(self):
        """Récupère le projet parent depuis l'URL, ou lève 404."""
        return get_object_or_404(Project, pk=self.kwargs["project_pk"])

    def get_queryset(self):
        project = self.get_project()
        return Contributor.objects.filter(project=project).select_related(
            "user", "project"
        )

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    """ Endpoint imbriqué : Liste les issues d'un projet """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_pk"])

    def get_queryset(self):
        project = self.get_project()
        return Issue.objects.filter(project=project).select_related(
            "project", "author", "assignee"
        )

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """ Endpoint imbriqué : Liste les comments d'une issue"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_issue(self):
        """Récupère l'issue parente depuis l'URL, en vérifiant la cohérence
        project_ID / issue_ID pour empêcher les accès croisés."""
        return get_object_or_404(
            Issue,
            pk=self.kwargs["issue_pk"],
            project__pk=self.kwargs["project_pk"],
        )

    def get_queryset(self):
        issue = self.get_issue()
        return Comment.objects.filter(issue=issue).select_related(
            "issue", "author"
        )

    def perform_create(self, serializer):
        issue = self.get_issue()
        serializer.save(author=self.request.user, issue=issue)

class UserProjectsViewset(viewsets.ReadOnlyModelViewSet):
    """ Endpoint imbriqué : listes les projets auxquels un utilisateur contribue"""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        user_pk = self.kwargs["user_pk"]
        return (
            Project.objects.filter(contributors__user_id=user_pk)
            .select_related("author")
            .prefetch_related("contributors")
            .distinct()
        )
    