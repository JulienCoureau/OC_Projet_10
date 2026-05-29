from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]
        #auteur = lecture seule
        read_only_fields = ["author", "created_time"]
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["project", "created_time"]

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "name", "description", "priority", "tag", "status", "project", "author", "assignee", "created_time"]
        # Auteur, projet, date gérés automatiqument
        read_only_fields = ["author","project", "created_time"]

    def validate_assignee(self, value):
        """ Verifie que l'assignee est cntributeur du projet """
        if value is None:
            return value
        
        #recupère le project via l'url
        project_pk = self.context["view"].kwargs.get("project_pk")
        if not project_pk:
            return value
        
        est_contributeur = Contributor.objects.filter(
            project_id=project_pk, user=value
        ).exists()
        if not est_contributeur :
            raise serializers.ValidationError(
                "L'utilisateur n'est pas contributeur de ce projet"
            )
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","description", "issue", "author", "created_time"]
        #ID et UUID auto-généré
        read_only_fields = ["id", "author", "issue", "created_time"]
