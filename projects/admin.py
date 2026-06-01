from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "author", "created_time")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "created_time")
    list_filter = ("project",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "priority", "tag", "status", "author")
    list_filter = ("priority", "tag", "status", "project")
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "issue", "author", "created_time")