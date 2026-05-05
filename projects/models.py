from django.db import models
from django.conf import settings
import uuid

class Project(models.Model):
    #types de projet possibles
    TYPE_CHOICES = [
        ("back-end", "Back-end"),
        ("front-end", "Front-end"),
        ("iOS", "iOS"), 
        ("Android", "Android"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # Autheur
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_projects")
    # Horodatage
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.name

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta :
        # un utilisateur ne peut être contributeur qu'une seule fois sur le même projet
        unique_together = ("user", "project")
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.user.username} sur {self.project.name}"
    
class Issue(models.Model):
    #Menu deroulant
    PRIORITY_CHOICES = [
            ("LOW", "Low"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High"),
    ]
    TAG_CHOICES = [
            ("BUG", "Bug"),
            ("FEATURE", "Feature"),
            ("TASK", "Task")
    ]
    STATUS_CHOICES = [
            ("To Do", "To Do"),
            ("In Progress", "In Progress"),
            ("Finished", "Finished")  
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="LOW")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default="To Do")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_issues")

    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_issues")

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta : 
        ordering = ["-created_time"]

    def __str__(self):
        return self.name

class Comment(models.Model):
    # UUID généré automatiquement 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_comments")
    #je force la mise a jour
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"Commentaire sur {self.issue.name}"