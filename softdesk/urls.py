"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet
from projects.views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
    UserProjectsViewset,
)

# Router racine pour les ressources de haut niveau
router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("projects", ProjectViewSet, basename="projects")

# Routr imbriqué sous /user/{ID}/
users_router = nested_routers.NestedSimpleRouter(
    router, r"users", lookup="user"
)
users_router.register(
    r"projects", UserProjectsViewset, basename="user-projects" 
)

# Router imbriqué sous /projects/{ID}/
projects_router = nested_routers.NestedSimpleRouter(
    router, r"projects", lookup="project"
)
projects_router.register(r"users", ContributorViewSet, basename="project-users")
projects_router.register(r"issues", IssueViewSet, basename="project-issues")

# Router imbriqué sous /projects/{ID}/issues/{ID}/
issues_router = nested_routers.NestedSimpleRouter(
    projects_router, r"issues", lookup="issue"
)
issues_router.register(r"comments", CommentViewSet, basename="issue-comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include (users_router.urls)),
    path("api/", include(projects_router.urls)),
    path("api/", include(issues_router.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
]
