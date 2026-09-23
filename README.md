# Portfolio DevOps & Multi-Cloud — Mohamed Nasser Mounchikpou Njiemessa

Site portfolio one-page construit avec Django, entièrement pilotable depuis
l'admin (compétences, expériences, projets, certifications), conteneurisé
avec Docker et pensé pour un déploiement AWS (ECS Fargate + RDS + ECR).

## Stack

- **Backend** : Django 5, Gunicorn, WhiteNoise (fichiers statiques)
- **Base de données** : PostgreSQL (SQLite en fallback local si aucune `DATABASE_URL` n'est fournie)
- **Conteneurisation** : Dockerfile multi-stage, utilisateur non-root, healthcheck
- **Reverse proxy** : Nginx (dev local via docker-compose)
- **CI/CD** : GitHub Actions — lint, tests, scan de vulnérabilités Trivy, build/push ECR, déploiement ECS
- **Infrastructure cible** : AWS (ECS Fargate, ECR, RDS PostgreSQL, Secrets Manager)

## 1. Développement local (sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

cp .env.example .env
# éditer .env : DJANGO_SECRET_KEY, DJANGO_DEBUG=True, etc.

python manage.py migrate
python manage.py seed_portfolio      # remplit le contenu à partir du CV
python manage.py createsuperuser     # pour accéder à /admin/
python manage.py runserver
```

Le site est disponible sur `http://127.0.0.1:8000/`, l'admin sur `/admin/`.
Tout le contenu (compétences, expériences, projets, certifications) est
ensuite modifiable depuis l'admin — aucune donnée n'est codée en dur dans
les templates.

## 2. Développement avec Docker (recommandé)

```bash
cp .env.example .env
# éditer .env, notamment POSTGRES_PASSWORD

docker compose up --build
```

- `web` : l'application Django servie par Gunicorn (migrations + collectstatic
  automatiques au démarrage via `deploy/entrypoint.sh`)
- `db` : PostgreSQL 16
- `nginx` : reverse proxy sur le port 80, sert `/static/` et `/media/` directement

Passez `SEED_PORTFOLIO_ON_START=true` dans `.env` pour peupler automatiquement
le contenu au premier démarrage.

Créer un compte admin dans le conteneur :

```bash
docker compose exec web python manage.py createsuperuser
```

## 3. Tests et qualité

```bash
python manage.py test
flake8 portfolio config
black --check -l 110 portfolio config
```

Ces trois commandes sont exécutées automatiquement par le pipeline CI/CD
avant tout build d'image.

## 4. Déploiement sur AWS

### Option retenue : ECS Fargate + ECR + RDS

1. **RDS PostgreSQL** : créer une instance `db.t4g.micro` (ou équivalent),
   dans un sous-réseau privé, groupe de sécurité limitant l'accès au SG
   des tâches ECS.
2. **Secrets Manager** : stocker `DJANGO_SECRET_KEY` et l'URL de connexion
   complète (`DATABASE_URL`) — référencés dans
   `deploy/ecs-task-definition.json` via `secrets`.
3. **ECR** : créer le repository `portfolio-app` (`aws ecr create-repository
   --repository-name portfolio-app`).
4. **IAM (OIDC)** : configurer un rôle IAM assumable par GitHub Actions via
   OpenID Connect (pas de clés d'accès long-lived stockées dans les secrets
   du repo) — stocker son ARN dans le secret GitHub `AWS_DEPLOY_ROLE_ARN`.
5. **ECS** : créer un cluster (`portfolio-cluster`), un service Fargate
   (`portfolio-service`) derrière un Application Load Balancer, à partir
   de `deploy/ecs-task-definition.json`.
6. **CI/CD** : chaque push sur `main` déclenche `.github/workflows/ci-cd.yml` :
   lint → tests → build de l'image → scan Trivy (bloquant sur CRITICAL/HIGH)
   → push vers ECR → déploiement ECS (avec l'environnement GitHub
   `production`, pour exiger une validation manuelle avant le déploiement).
7. **HTTPS** : certificat ACM attaché au Load Balancer, `DJANGO_SECURE_SSL_REDIRECT=True`
   et `DJANGO_CSRF_TRUSTED_ORIGINS` pointant vers le domaine final.

### Alternative plus simple : EC2 + Docker Compose

Pour une mise en ligne rapide sans ECS :

```bash
# Sur l'instance EC2 (Amazon Linux 2023 ou Ubuntu)
git clone <votre-repo>
cd portfolio_project
cp .env.example .env   # éditer avec les vraies valeurs de prod
docker compose up -d --build
```

Placer un certificat Let's Encrypt / ACM devant Nginx, ouvrir les ports
80/443 dans le security group, et pointer le domaine vers l'IP publique
(ou une Elastic IP).

## 5. Variables d'environnement clés

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django (obligatoire, longue et aléatoire en prod) |
| `DJANGO_DEBUG` | `False` en production |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés, séparés par des virgules |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origines HTTPS de confiance pour le CSRF |
| `DATABASE_URL` | URL de connexion PostgreSQL (format `postgres://user:pass@host:5432/db`) |
| `SEED_PORTFOLIO_ON_START` | `true` pour peupler le contenu au démarrage du conteneur |

## 6. Structure du projet

```
config/                  # settings, urls, wsgi/asgi
portfolio/                # app Django : modèles, vues, templates, static
  management/commands/    # seed_portfolio
  templates/portfolio/    # base.html, home.html
  static/portfolio/       # css/, js/
deploy/                   # entrypoint.sh, ecs-task-definition.json
nginx/                    # config du reverse proxy
.github/workflows/        # pipeline CI/CD
```

## 7. Mettre à jour le contenu

Tout le contenu affiché (profil, compétences, expériences, projets,
certifications) est géré depuis l'admin Django (`/admin/`) — aucune
modification de template n'est nécessaire pour ajouter un projet ou une
certification.
