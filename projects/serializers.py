from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]
        #auteur = lecture seule
        read_only_fields = ["author", "created_time"]

    def create(self, validated_data):
        # utilisateur qui fait la requête
        user = self.context["request"].user
        # utilisateur = auteur du projet
        project = Project.objects.create(author=user, **validated_data)
        # Auteur devient automatiquement contributeur
        Contributor.objects.create(user=user, project=project)

        return project 
    
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["created_time"]

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "name", "description", "priority", "tag", "status", "project", "author", "assignee", "created_time"]
        # Auteur, projet, date gérés automatiqument
        read_only_fields = ["author", "created_time"]

    def validate(self, data):
        """ Verifie les données avant de les sauvegarder """
        # On recupere le projet cible
        project = data.get("project")
        if not project and self.instance:
            project = self.instance.project
            
        # On recupere la personne
        assignee = data.get("assignee")
        
        # si on essaie d'assigner quelqu'un il doit etre contributeur 
        if assignee and project:
            # Cherche dans la bdd un lien
            est_contributeur = Contributor.objects.filter(project=project, user=assignee).exists()
            # Si lien n'existe pas
            if not est_contributeur:
                raise serializers.ValidationError({
                    "assignee": "Impossible, L'utilisateur n'est pas contributeur du projet"
                })
                
        # SI OK
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","description", "issue", "author", "created_time"]
        #ID et UUID auto-généré
        read_only_fields = ["id", "author", "created_time"]

