from datetime import date, timedelta

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Project, Contributor

User = get_user_model()


def date_naissance_il_y_a(annees):
    """Retourne une date ISO correspondant à 'annees' années en arrière.
    Helper utilisé pour générer des âges dans les tests."""
    return (date.today() - timedelta(days=annees * 365)).isoformat()


class ProjectAPITestCase(APITestCase):
    """Tests sur l'API des projets : création, lecture, modification, permissions."""

    def setUp(self):
        """crée deux utilisateurs."""
        self.test1 = User.objects.create_user(
            username="test1",
            password="Azerty1234!",
            birth_date="1995-06-12",
        )
        self.test2 = User.objects.create_user(
            username="test2",
            password="Azerty1234!",
            birth_date="1990-03-25",
        )

    def test_user_non_authentifie_ne_peut_pas_lister_les_projets(self):
        """Sans token, GET /api/projects/ doit renvoyer 401."""
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authentifie_peut_creer_un_projet(self):
        """test1 crée un projet et devient automatiquement auteur ET contributeur."""
        self.client.force_authenticate(user=self.test1)
        data = {
            "name": "Mon premier projet",
            "description": "test projet",
            "type": "back-end",
        }
        response = self.client.post("/api/projects/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.author, self.test1)
        self.assertTrue(
            Contributor.objects.filter(user=self.test1, project=project).exists()
        )

    def test_user_non_contributeur_ne_voit_pas_les_projets_des_autres(self):
        """test2 ne voit pas le projet créé par test1."""
        project = Project.objects.create(
            name="Projet test1", type="back-end", author=self.test1
        )
        Contributor.objects.create(user=self.test1, project=project)

        self.client.force_authenticate(user=self.test2)
        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_user_non_auteur_ne_peut_pas_modifier_un_projet(self):
        """test2 ne peut pas modifier le projet de test1 (renvoie 404 car filtré)."""
        project = Project.objects.create(
            name="Projet test1", type="back-end", author=self.test1
        )
        Contributor.objects.create(user=self.test1, project=project)

        self.client.force_authenticate(user=self.test2)
        response = self.client.put(
            f"/api/projects/{project.id}/",
            {"name": "Hacké !", "type": "back-end"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auteur_peut_supprimer_son_projet(self):
        """test1 supprime son propre projet."""
        project = Project.objects.create(
            name="Projet test1", type="back-end", author=self.test1
        )
        Contributor.objects.create(user=self.test1, project=project)

        self.client.force_authenticate(user=self.test1)
        response = self.client.delete(f"/api/projects/{project.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)


class UserAPITestCase(APITestCase):
    """Tests sur l'API des utilisateurs : RGPD, inscription."""

    def test_user_de_moins_de_15_ans_ne_peut_pas_sinscrire(self):
        """Un mineur de moins de 15 ans est refusé (RGPD)."""
        data = {
            "username": "enfant",
            "password": "Azerty1234!",
            "birth_date": date_naissance_il_y_a(14),
        }
        response = self.client.post("/api/users/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data)

    def test_user_de_plus_de_15_ans_peut_sinscrire(self):
        """Un utilisateur de 16 ans s'inscrit normalement."""
        data = {
            "username": "ado",
            "password": "Azerty1234!",
            "birth_date": date_naissance_il_y_a(16),
        }
        response = self.client.post("/api/users/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)