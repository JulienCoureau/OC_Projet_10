# SoftDesk Support

API RESTful Django permettant à des utilisateurs de créer des projets, d'y ajouter des contributeurs, de déclarer des problèmes (issues) et de les commenter. L'authentification est gérée par JSON Web Token (JWT). L'application respecte les règles RGPD et applique des permissions par auteur et par contributeur.

Projet réalisé dans le cadre de la formation Développeur d'Application Python sur OpenClassrooms.

## Fonctionnalités

* Authentification : inscription, connexion via JWT, vérification de l'âge à l'inscription (15 ans minimum).
* Projets : création, modification et suppression. L'auteur d'un projet en devient automatiquement contributeur.
* Issues : création par les contributeurs du projet, avec priorité (LOW, MEDIUM, HIGH), balise (BUG, FEATURE, TASK) et statut (To Do, In Progress, Finished).
* Commentaires : création par les contributeurs du projet, identifiés par UUID.
* Permissions : seuls les contributeurs d'un projet peuvent voir ses ressources, seul l'auteur peut modifier ou supprimer.
* Pagination des listes et optimisation des requêtes SQL.

## Technologies

* Python 3.12
* Django 6.0
* Django REST Framework
* djangorestframework-simplejwt
* SQLite

## Installation et exécution

### Prérequis
* Python 3.12+
* Pipenv

### Déploiement local

1. Clonez le dépôt :

        git clone <URL_DU_REPO>
        cd projet_10

2. Installez les dépendances et activez l'environnement virtuel :

        pipenv install
        pipenv shell

3. Appliquez les migrations :

        python manage.py migrate

4. Démarrez le serveur :

        python manage.py runserver

L'API est accessible à l'adresse : http://127.0.0.1:8000/

## Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/users/ | Inscription |
| POST | /api/login/ | Connexion (obtention du token JWT) |
| POST | /api/token/refresh/ | Rafraîchir l'access token |
| GET, POST | /api/projects/ | Lister ou créer un projet |
| GET, PUT, DELETE | /api/projects/{id}/ | Détail, modifier ou supprimer un projet |
| GET, POST | /api/contributors/ | Lister ou ajouter un contributeur |
| GET, POST | /api/issues/ | Lister ou créer une issue |
| GET, PUT, DELETE | /api/issues/{id}/ | Détail, modifier ou supprimer une issue |
| GET, POST | /api/comments/ | Lister ou créer un commentaire |
| GET, PUT, DELETE | /api/comments/{id}/ | Détail, modifier ou supprimer un commentaire |

Pour les endpoints protégés, ajouter le header `Authorization: Bearer <access_token>`.

## Étapes du projet

Le projet a été développé en suivant les six étapes du cahier des charges :

1. **Configuration du projet.** Mise en place de Django et Django REST Framework, gestion des dépendances avec Pipenv, versionnement sur GitHub.
2. **Modèle User.** Création d'un modèle utilisateur personnalisé incluant les champs RGPD (date de naissance, `can_be_contacted`, `can_data_be_shared`) et la validation de l'âge à l'inscription.
3. **Modèles Project et Contributor.** Création des projets (back-end, front-end, iOS, Android) et du système de contributeurs liant utilisateurs et projets.
4. **Modèles Issue et Comment.** Ajout des issues (priorité, balise, statut) et des commentaires identifiés par UUID.
5. **Permissions.** Authentification JWT, permission `IsAuthorOrReadOnly` (seul l'auteur peut modifier ou supprimer), permission `IsProjectContributor` (accès aux ressources d'un projet réservé à ses contributeurs), filtrage des querysets par utilisateur. Activation de Dependabot sur le dépôt GitHub.
6. **Green code et optimisation.** Mise en place de la pagination (10 éléments par page) et utilisation de `select_related` et `prefetch_related` pour limiter le nombre de requêtes SQL.

## Tests

Une suite de tests automatisés couvre les permissions, la création des ressources et la conformité RGPD.

Pour exécuter les tests :

    python manage.py test

## Auteur

Julien Coureau - Formation OpenClassrooms Développeur d'Application Python