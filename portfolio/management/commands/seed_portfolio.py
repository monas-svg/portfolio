from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    Certification,
    CertificationStatus,
    Experience,
    ExperienceHighlight,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


class Command(BaseCommand):
    help = "Peuple la base avec le contenu initial du portfolio (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        self._seed_profile()
        self._seed_skills()
        self._seed_experiences()
        self._seed_projects()
        self._seed_project_details()
        self._seed_project_visuals()
        self._seed_mpahmum_infra()
        self._seed_certifications()
        self.stdout.write(self.style.SUCCESS("Contenu du portfolio initialisé."))

    def _seed_profile(self):
        Profile.objects.update_or_create(
            pk=1,
            defaults=dict(
                full_name="Mohamed Nasser Mounchikpou Njiemessa",
                headline="Ingénieur DevOps & Cloud Engineer | AWS & Azure | IA générative",
                location="Douala, Cameroun",
                email="devops@mohamednasser.site",
                phone="+237 690 87 29 82",
                github_url="https://github.com/monassvg",
                linkedin_url="https://linkedin.com/in/mohamed-nasser-mounchikpou",
                years_experience=4,
                summary=(
    "Ingénieur DevOps et Multi-Cloud avec plus de 4 ans d'expérience dans la coordination de "
    "projets IT et le développement backend. En cours de certification AWS Solutions "
    "Architect Associate (SAA-C03), et récemment certifié Microsoft Azure Developer "
    "Associate (AZ-204), Microsoft Azure Fundamentals (AZ-900) et AWS Cloud Practitioner "
    "(CLF-C02), je combine une forte expertise en développement Python/Django avec "
    "l'administration d'infrastructures cloud hybrides et scalables. Spécialiste de la "
    "conteneurisation (Docker), de l'orchestration Kubernetes (Helm) et de "
    "l'infrastructure as code (Terraform), des environnements Linux et de "
    "l'automatisation de pipelines CI/CD (GitHub Actions). Fort de mes certifications "
    "Google AI Professional, Google Prompting Essentials, ainsi que Claude Code 101 et "
    "Claude Platform 101 (Anthropic), j'intègre activement l'IA générative, y compris "
    "les outils IA agentiques comme Claude, pour accélérer le développement, optimiser "
    "l'analyse de données et fiabiliser les workflows opérationnels."
),
            ),
        )

    def _seed_skills(self):
        skills = [
            # (nom, catégorie, niveau, ordre)
            ("AWS (Cloud Practitioner, SAA-C03 en cours)", SkillCategory.CLOUD_DEVOPS, 4, 1),
            ("Microsoft Azure (AZ-900 & AZ-204 certifiés)", SkillCategory.CLOUD_DEVOPS, 5, 2),
            ("Kubernetes (Helm)", SkillCategory.CLOUD_DEVOPS, 4, 3),
            ("Terraform (IaC)", SkillCategory.CLOUD_DEVOPS, 4, 4),
            ("Docker (multi-stage, hardening)", SkillCategory.CLOUD_DEVOPS, 5, 5),
            ("CI/CD (GitHub Actions)", SkillCategory.CLOUD_DEVOPS, 5, 6),
            ("IBM Cloud", SkillCategory.CLOUD_DEVOPS, 3, 7),
            ("Sécurité applicative (Trivy, gestion CVE)", SkillCategory.CLOUD_DEVOPS, 4, 8),
            ("Ubuntu / Debian", SkillCategory.LINUX_SCRIPTING, 5, 1),
            ("Bash scripting", SkillCategory.LINUX_SCRIPTING, 5, 2),
            ("Cron & gestion des processus", SkillCategory.LINUX_SCRIPTING, 4, 3),
            ("TCP/IP, HTTP/HTTPS", SkillCategory.NETWORK_SECURITY, 4, 1),
            ("API REST & JWT", SkillCategory.NETWORK_SECURITY, 5, 2),
            ("Nginx & SSL/TLS", SkillCategory.NETWORK_SECURITY, 4, 3),
            ("Python & Django", SkillCategory.DEVELOPMENT, 5, 1),
            ("Node.js / Express", SkillCategory.DEVELOPMENT, 3, 2),
            ("PostgreSQL", SkillCategory.DEVELOPMENT, 4, 3),
            ("Git / GitHub", SkillCategory.DEVELOPMENT, 5, 4),
            ("Google AI Professional Certificate", SkillCategory.AI_PROMPTING, 4, 1),
            ("Google Prompting Essentials", SkillCategory.AI_PROMPTING, 4, 2),
            ("Claude Code 101 & Claude Platform 101 (Anthropic)", SkillCategory.AI_PROMPTING, 4, 3),
            ("Prompt engineering & agents IA (vibe coding)", SkillCategory.AI_PROMPTING, 4, 4),
            ("Intégration IA dans les workflows DevOps", SkillCategory.AI_PROMPTING, 4, 5),
            ("SCRUM / Agile", SkillCategory.PROJECT_MGMT, 4, 1),
            ("Jira / Trello", SkillCategory.PROJECT_MGMT, 4, 2),
            ("Management d'équipes", SkillCategory.PROJECT_MGMT, 4, 3),
        ]
        for name, category, proficiency, order in skills:
            Skill.objects.update_or_create(
                name=name,
                defaults=dict(category=category, proficiency=proficiency, order=order),
            )

    def _seed_experiences(self):
        exp1, _ = Experience.objects.update_or_create(
            role="Directeur des Opérations & Consultant IT",
            organization="TEAM SOLUTIONS Sarl",
            defaults=dict(
                location="Douala",
                start_date=date(2024, 10, 1),
                end_date=date(2025, 12, 31),
                order=1,
            ),
        )
        exp1.highlights.all().delete()
        for i, text in enumerate(
            [
                "Coordination de projets IT sous Linux : déploiement, maintenance et monitoring d'applications web",
                "Mise en place de pipelines CI/CD sur GitHub Actions + Docker pour la livraison continue",
                "Administration d'instances cloud AWS EC2 et IBM Cloud : provisionnement, sécurisation, mises à jour",
                "Scripting Bash pour l'automatisation des déploiements, sauvegardes et tâches récurrentes",
                "Management d'équipes pluridisciplinaires en méthodologie SCRUM/Agile + reporting direction",
                "Gestion des incidents de production et documentation technique",
            ]
        ):
            ExperienceHighlight.objects.create(experience=exp1, text=text, order=i)

        exp2, _ = Experience.objects.update_or_create(
            role="Développeur Web & Coordinateur de Projets",
            organization="Société Pharmaceutique",
            defaults=dict(
                location="Douala",
                start_date=date(2021, 6, 1),
                end_date=date(2023, 7, 31),
                order=2,
            ),
        )
        exp2.highlights.all().delete()
        for i, text in enumerate(
            [
                "Développement et déploiement d'APIs REST (Django) sur serveurs Linux, avec Nginx, SSL et variables d'env.",
                "Intégration continue : automatisation des tests et déploiements via scripts Bash et Git hooks",
                "Administration PostgreSQL : modélisation, optimisation des requêtes, sauvegardes automatisées",
                "Conteneurisation des applications avec Docker ; gestion des dépendances et environnements",
                "Coordination Agile des équipes et livraison dans les délais",
            ]
        ):
            ExperienceHighlight.objects.create(experience=exp2, text=text, order=i)

        exp3, _ = Experience.objects.update_or_create(
            role="Responsable de Projet",
            organization="MBCODE",
            defaults=dict(
                location="Douala",
                start_date=date(2021, 4, 1),
                end_date=date(2021, 6, 30),
                order=3,
            ),
        )
        exp3.highlights.all().delete()
        for i, text in enumerate(
            [
                "Planification et suivi de projets de formation en développement (Coding School for Kids)",
                "Coordination du partenariat avec l'Institut Panafricain de Développement d'Afrique Centrale (IPD-AC)",
            ]
        ):
            ExperienceHighlight.objects.create(experience=exp3, text=text, order=i)

    def _seed_projects(self):
        projects = [
            dict(
                title="SwingBot : Infrastructure DevOps & Multi-Cloud",
                summary=(
                    "Contribution freelance à la chaîne DevOps complète d'une application de trading "
                    "(API FastAPI, worker Python, frontend React)."
                ),
                description=(
                    "Conteneurisation Docker multi-stage durcie (utilisateurs non-root, healthchecks, "
                    "réduction de la surface de vulnérabilités), orchestration Kubernetes via un chart "
                    "Helm (autoscaling, PodDisruptionBudget, NetworkPolicy, secrets AWS Secrets Manager), "
                    "infrastructure AWS as code avec Terraform (VPC, EKS, ECR, RDS, IAM/OIDC), et pipelines "
                    "CI/CD GitHub Actions (lint, tests automatisés, scan de vulnérabilités Trivy, déploiement "
                    "avec validation manuelle). Diagnostic et correction de vulnérabilités réelles, dont un "
                    "incident de chaîne d'approvisionnement logiciel, en recompilant les outils concernés "
                    "depuis leurs sources pour les reproduire fidèlement."
                ),
                stack="Kubernetes · Helm · Terraform · AWS (EKS, ECR, RDS, IAM) · Docker · GitHub Actions · Trivy",
                repo_url="",
                repo_private=True,
                is_featured=True,
                order=1,
            ),
            dict(
                title="MBC ERP",
                summary="Application de gestion d'un centre : coworking, camps de formation pour enfants et formations en IA.",
                description=(
                    "Application web couvrant les clients, la facturation (espèces, Orange Money, MTN Mobile Money), "
                    "la location d'espaces, les inscriptions aux camps et formations avec paiement échelonné, les "
                    "dépenses et charges fixes, la clôture de caisse journalière et des rapports (revenus, marge, "
                    "taux d'occupation) avec graphiques SVG générés côté serveur. Rôles et permissions, verrouillage "
                    "des enregistrements sensibles, API REST sécurisée par JWT. Conteneurisée avec Docker "
                    "(utilisateur non privilégié), CI GitHub Actions (lint, tests, scan de sécurité), manifestes "
                    "Kubernetes et infrastructure Azure (AKS, ACR) décrite avec Terraform."
                ),
                stack="Python · Django · Django REST Framework · JWT · PostgreSQL · Docker · Kubernetes · Terraform · Azure · GitHub Actions",
                repo_url="",
                live_url="https://www.mbcerp.site",
                is_featured=False,
                order=2,
            ),
            dict(
                title="Mpahmum",
                summary="Livre d'or numérique personnalisable pour les événements, avec modération et tableau de bord.",
                description=(
                    "Application de livre d'or et d'hommage numérique : les invités déposent des témoignages "
                    "personnalisés avec photos grâce à des sessions sécurisées par jeton, et l'administration "
                    "modère, épingle et analyse les messages depuis un tableau de bord protégé. Front React et "
                    "TypeScript, API Express durcie (liste blanche des champs, limitation de débit, réactions "
                    "atomiques), base PostgreSQL via Prisma, génération de livrets PDF, déploiement Docker Compose."
                ),
                stack="React · TypeScript · Vite · Express · Prisma · PostgreSQL · Tailwind CSS · Docker",
                repo_url="",
                live_url="https://www.mpahmum.site",
                is_featured=False,
                order=3,
            ),
            dict(
                title="CertifPro",
                summary="Plateforme de vente de coupons pour formations et certifications.",
                description=(
                    "Backend Node/Express sécurisé intégrant un agrégateur de paiement, conteneurisé "
                    "avec Docker, avec notifications automatiques (e-mail + WhatsApp)."
                ),
                stack="Node.js · Express · Docker · API de paiement · HTML",
                repo_url="",
                live_url="https://www.certipro.site",
                is_featured=False,
                order=4,
            ),
            dict(
                title="SecurAuth-API",
                summary="API d'authentification JWT (Django REST Framework) avec rôles et e-mails, déployée sur IBM Cloud.",
                description=(
                    "API d'authentification complète : inscription et connexion JWT (SimpleJWT) avec rotation et "
                    "révocation des refresh tokens, gestion des rôles (admin, manager, utilisateur), profil "
                    "utilisateur, réinitialisation de mot de passe par e-mail (SendGrid) et journalisation des "
                    "connexions. Interface web de connexion, inscription et profil refondue. Conteneurisée avec "
                    "Docker, déployée sur IBM Cloud Code Engine avec PostgreSQL et IBM Container Registry."
                ),
                stack="Python · Django · Django REST Framework · SimpleJWT · PostgreSQL · IBM Cloud Code Engine · Docker · SendGrid",
                repo_url="",
                repo_private=True,
                is_featured=False,
                order=5,
            ),
            dict(
                title="Pharma-API",
                summary="API REST complète avec déploiement automatisé sur AWS EC2.",
                description="Gestion des environnements via variables d'environnement et documentation technique.",
                stack="Python · Django · API REST · CI/CD · AWS EC2",
                repo_url="",
                repo_private=True,
                is_featured=False,
                order=6,
            ),
            dict(
                title="Déployez une application Django",
                summary="Mise en pratique du déploiement d'une application Django en production (OpenClassrooms).",
                description="",
                stack="Python · Django · Déploiement",
                repo_url="",
                repo_private=True,
                is_featured=False,
                order=7,
            ),
        ]
        for data in projects:
            Project.objects.update_or_create(title=data["title"], defaults=data)

    def _seed_certifications(self):
        certifications = [
            (
                "Claude Platform 101",
                "Anthropic",
                CertificationStatus.OBTAINED,
                date(2026, 9, 1),
                "",
                1,
            ),
            (
                "Claude Code 101",
                "Anthropic",
                CertificationStatus.OBTAINED,
                date(2026, 9, 1),
                "",
                2,
            ),
            (
                "Microsoft Azure Developer Associate (AZ-204)",
                "DataCamp",
                CertificationStatus.OBTAINED,
                date(2026, 9, 1),
                "#943,429",
                3,
            ),
            (
                "AWS Solutions Architect – Associate (SAA-C03)",
                "AWS Training & Certification",
                CertificationStatus.IN_PROGRESS,
                None,
                "",
                4,
            ),
            (
                "Microsoft Azure Fundamentals (AZ-900)",
                "DataCamp",
                CertificationStatus.OBTAINED,
                date(2026, 8, 1),
                "#923,230",
                5,
            ),
            (
                "AWS Cloud Practitioner (CLF-C02)",
                "DataCamp",
                CertificationStatus.OBTAINED,
                date(2026, 8, 1),
                "#919,723",
                6,
            ),
            (
                "Google AI Professional Certificate",
                "Google / Coursera",
                CertificationStatus.OBTAINED,
                date(2026, 7, 1),
                "BPMPJU4YNTLG",
                7,
            ),
            (
                "Google Prompting Essentials",
                "Google / Coursera",
                CertificationStatus.OBTAINED,
                date(2026, 7, 1),
                "BS5PQYQINQ0R",
                8,
            ),
            (
                "IBM DevOps and Software Engineering Certificate",
                "IBM / Coursera",
                CertificationStatus.IN_PROGRESS,
                None,
                "",
                9,
            ),
            (
                "Google Project Management Certificate",
                "Google / Coursera",
                CertificationStatus.IN_PROGRESS,
                None,
                "",
                10,
            ),
            (
                "Administration Linux",
                "OpenClassrooms",
                CertificationStatus.OBTAINED,
                date(2026, 6, 1),
                "",
                11,
            ),
            (
                "Développeur Python – Génie logiciel",
                "OpenClassrooms",
                CertificationStatus.OBTAINED,
                date(2026, 1, 1),
                "",
                12,
            ),
            (
                "Développeur Django – Génie logiciel",
                "OpenClassrooms",
                CertificationStatus.OBTAINED,
                date(2026, 1, 1),
                "",
                13,
            ),
            (
                "Intégration et conception des API",
                "OpenClassrooms",
                CertificationStatus.OBTAINED,
                date(2026, 1, 1),
                "",
                14,
            ),
        ]
        for name, issuer, status, date_obtained, credential_id, order in certifications:
            Certification.objects.update_or_create(
                name=name,
                defaults=dict(
                    issuer=issuer,
                    status=status,
                    date_obtained=date_obtained,
                    credential_id=credential_id,
                    order=order,
                ),
            )


    def _seed_project_details(self):
        """Contexte, problème résolu et cartographie d'infrastructure de chaque projet."""
        details = {
            "SwingBot : Infrastructure DevOps & Multi-Cloud": dict(
                context=(
                    "Application de trading composée d'une API FastAPI, d'un worker Python et d'un "
                    "frontend React, à déployer sur AWS dans le cadre d'une mission freelance."
                ),
                problem_solved=(
                    "Livrer l'application de façon reproductible et sécurisée : images Docker durcies, "
                    "déploiement Kubernetes automatisé, infrastructure décrite en code, pipeline CI/CD avec "
                    "scan de vulnérabilités et validation manuelle avant production, et correction de "
                    "vulnérabilités réelles, dont un incident de chaîne d'approvisionnement logiciel."
                ),
                infra_diagram="""flowchart LR
  Dev["Développeur"] --> GH["GitHub Actions : lint, tests, Trivy"]
  GH --> ECR["AWS ECR"]
  ECR --> EKS["AWS EKS via Helm"]
  EKS --> API["API FastAPI"]
  EKS --> WK["Worker Python"]
  EKS --> FE["Frontend React"]
  API --> RDS[("AWS RDS")]
  WK --> RDS
  SM["AWS Secrets Manager"] --> EKS
  TF["Terraform"] -.-> EKS
  TF -.-> RDS
""",
                infra_components=[
                    {"couche": "Application", "outils": ["FastAPI", "Worker Python", "React"]},
                    {"couche": "Conteneurs", "outils": ["Docker multi-stage", "Utilisateurs non-root", "Healthchecks"]},
                    {"couche": "Orchestration", "outils": ["Kubernetes", "Helm", "Autoscaling", "PodDisruptionBudget", "NetworkPolicy"]},
                    {"couche": "Cloud AWS", "outils": ["VPC", "EKS", "ECR", "RDS", "IAM/OIDC", "Secrets Manager"]},
                    {"couche": "Infrastructure as code", "outils": ["Terraform"]},
                    {"couche": "CI/CD et sécurité", "outils": ["GitHub Actions", "Trivy"]},
                ],
            ),
            "MBC ERP": dict(
                context=(
                    "Un centre qui propose du coworking, des camps de formation pour enfants et des formations "
                    "en IA avait besoin d'un outil unique pour piloter ses activités et ses encaissements."
                ),
                problem_solved=(
                    "Centraliser clients, facturation (espèces, Orange Money, MTN Mobile Money), location "
                    "d'espaces, inscriptions avec paiement échelonné, dépenses et clôture de caisse, avec des "
                    "rapports fiables (revenus, marge, taux d'occupation) et des accès contrôlés par rôle."
                ),
                infra_diagram="""flowchart LR
  U["Équipe du centre"] --> W["Application Django + API REST JWT"]
  W --> DB[("PostgreSQL")]
  W --> PAY["Paiements : espèces, Orange Money, MTN MoMo"]
  GH["GitHub Actions : lint, tests, scan"] --> ACR["Azure ACR"]
  ACR --> AKS["Azure AKS"]
  AKS --> W
  TF["Terraform"] -.-> AKS
  TF -.-> ACR
""",
                infra_components=[
                    {"couche": "Application", "outils": ["Django", "Django REST Framework", "JWT", "PostgreSQL"]},
                    {"couche": "Conteneurs", "outils": ["Docker", "Utilisateur non privilégié"]},
                    {"couche": "Orchestration", "outils": ["Manifestes Kubernetes"]},
                    {"couche": "Cloud Azure", "outils": ["AKS", "ACR"]},
                    {"couche": "Infrastructure as code", "outils": ["Terraform"]},
                    {"couche": "CI/CD et sécurité", "outils": ["GitHub Actions", "Lint", "Tests", "Scan de sécurité"]},
                ],
            ),
            "Mpahmum": dict(
                context=(
                    "Les événements (hommages, cérémonies) manquaient d'un moyen simple de recueillir les "
                    "témoignages et les photos des invités, et de les conserver."
                ),
                problem_solved=(
                    "Permettre aux invités de déposer des témoignages personnalisés avec photos via des "
                    "sessions sécurisées par jeton, et à l'administration de modérer, épingler et analyser les "
                    "messages, avec une API durcie (liste blanche des champs, limitation de débit) et la "
                    "génération de livrets PDF."
                ),
                infra_diagram="""flowchart LR
  G["Invités"] --> F["Front React + TypeScript"]
  A["Administrateur"] --> F
  F --> API["API Express durcie"]
  API --> PR["Prisma"]
  PR --> DB[("PostgreSQL")]
  API --> PDF["Génération de livrets PDF"]
  subgraph Docker["Docker Compose"]
    F
    API
    DB
  end
""",
                infra_components=[
                    {"couche": "Front", "outils": ["React", "TypeScript", "Vite", "Tailwind CSS"]},
                    {"couche": "API", "outils": ["Express", "Liste blanche des champs", "Limitation de débit"]},
                    {"couche": "Données", "outils": ["Prisma", "PostgreSQL"]},
                    {"couche": "Déploiement", "outils": ["Docker Compose"]},
                ],
            ),
            "CertifPro": dict(
                context=(
                    "Vendre en ligne des coupons pour des formations et des certifications nécessitait "
                    "d'encaisser en sécurité et de livrer automatiquement le coupon à l'acheteur."
                ),
                problem_solved=(
                    "Automatiser l'achat de bout en bout : encaissement via un agrégateur de paiement, puis "
                    "notification automatique de l'acheteur par e-mail et WhatsApp."
                ),
                infra_diagram="""flowchart LR
  C["Client"] --> W["Site HTML"]
  W --> API["Backend Node + Express sécurisé"]
  API --> PAY["Agrégateur de paiement"]
  PAY -->|"confirmation"| API
  API --> M["Notification e-mail"]
  API --> WA["Notification WhatsApp"]
  subgraph Docker
    API
  end
""",
                infra_components=[
                    {"couche": "Application", "outils": ["Node.js", "Express", "HTML"]},
                    {"couche": "Paiement", "outils": ["API de paiement"]},
                    {"couche": "Notifications", "outils": ["E-mail", "WhatsApp"]},
                    {"couche": "Conteneurs", "outils": ["Docker"]},
                ],
            ),
            "SecurAuth-API": dict(
                context=(
                    "Les applications avaient besoin d'une brique d'authentification réutilisable, sécurisée "
                    "et déployable dans le cloud."
                ),
                problem_solved=(
                    "Fournir inscription et connexion JWT avec rotation et révocation des refresh tokens, "
                    "gestion des rôles (admin, manager, utilisateur), réinitialisation de mot de passe par "
                    "e-mail et journalisation des connexions."
                ),
                infra_diagram="""flowchart LR
  U["Client ou application"] --> API["Django REST Framework + SimpleJWT"]
  API --> DB[("PostgreSQL")]
  API --> SG["SendGrid : e-mails"]
  D["Image Docker"] --> ICR["IBM Container Registry"]
  ICR --> CE["IBM Cloud Code Engine"]
  CE --> API
""",
                infra_components=[
                    {"couche": "Application", "outils": ["Django", "Django REST Framework", "SimpleJWT"]},
                    {"couche": "Données", "outils": ["PostgreSQL"]},
                    {"couche": "E-mails", "outils": ["SendGrid"]},
                    {"couche": "Conteneurs", "outils": ["Docker", "IBM Container Registry"]},
                    {"couche": "Cloud IBM", "outils": ["Code Engine"]},
                ],
            ),
            "Pharma-API": dict(
                context=(
                    "API REST réalisée dans un contexte pharmaceutique, avec une exigence de déploiement "
                    "fiable et reproductible."
                ),
                problem_solved=(
                    "Automatiser le déploiement de l'API sur AWS EC2 et gérer proprement la configuration par "
                    "environnement via des variables d'environnement, avec une documentation technique."
                ),
                infra_diagram="""flowchart LR
  Dev["Développeur"] --> CI["Pipeline CI/CD"]
  CI --> EC2["AWS EC2"]
  EC2 --> API["API REST Django"]
  ENV["Variables d'environnement"] -.-> API
""",
                infra_components=[
                    {"couche": "Application", "outils": ["Python", "Django", "API REST"]},
                    {"couche": "Cloud AWS", "outils": ["EC2"]},
                    {"couche": "Livraison", "outils": ["CI/CD", "Variables d'environnement"]},
                ],
            ),
            "Déployez une application Django": dict(
                context="Parcours OpenClassrooms : mettre en pratique la mise en production d'une application Django.",
                problem_solved="Passer d'une application Django exécutée en local à une application déployée en production.",
                infra_diagram="",
                infra_components=[
                    {"couche": "Application", "outils": ["Python", "Django"]},
                    {"couche": "Déploiement", "outils": ["Mise en production"]},
                ],
            ),
        }
        for title, data in details.items():
            Project.objects.filter(title=title).update(**data)


    def _seed_project_visuals(self):
        """Schéma d'infrastructure et description du problème résolu de chaque projet."""
        visuals = {
            "SwingBot : Infrastructure DevOps & Multi-Cloud": (
                "swingbot",
                "Une application de trading (API, worker, frontend) est difficile à livrer de façon fiable "
                "et sécurisée sans chaîne industrialisée. Cette infrastructure y répond : environnement AWS "
                "reproductible grâce à Terraform, images Docker durcies, déploiement Kubernetes piloté par "
                "Helm avec autoscaling et isolation réseau, secrets gérés par AWS Secrets Manager, et "
                "pipeline CI/CD qui bloque les images vulnérables (Trivy) avant une validation manuelle de "
                "la mise en production.",
            ),
            "MBC ERP": (
                "mbc-erp",
                "Piloter un centre qui cumule coworking, camps pour enfants et formations en IA oblige à "
                "suivre des encaissements multiples (espèces, Orange Money, MTN Mobile Money), des paiements "
                "échelonnés, des dépenses et la caisse du jour. L'ERP centralise ces flux, verrouille les "
                "enregistrements sensibles, produit les rapports (revenus, marge, taux d'occupation) et "
                "s'exécute sur une infrastructure Azure reproductible (AKS, ACR, Terraform).",
            ),
            "Mpahmum": (
                "mpahmum",
                "Recueillir et conserver les témoignages et les photos des invités d'un événement est "
                "difficile sans outil dédié, et un formulaire public s'expose aux abus. L'application "
                "permet aux invités de déposer leur message via une session sécurisée par jeton, à "
                "l'administration de modérer et d'épingler les contributions, et protège l'API (liste "
                "blanche des champs, limitation de débit, réactions atomiques). Le tout tourne dans "
                "Docker Compose et produit des livrets PDF.",
            ),
            "CertifPro": (
                "certifpro",
                "Vendre des coupons de formation en ligne suppose d'encaisser en sécurité puis de livrer "
                "sans délai. Le backend Node.js/Express, conteneurisé avec Docker, s'appuie sur un "
                "agrégateur de paiement et notifie automatiquement l'acheteur par e-mail et WhatsApp, "
                "sans intervention manuelle.",
            ),
            "SecurAuth-API": (
                "securauth-api",
                "Chaque application qui gère des comptes doit sinon réinventer l'authentification. "
                "SecurAuth-API fournit une brique réutilisable : connexion JWT avec rotation et "
                "révocation des refresh tokens, rôles (admin, manager, utilisateur), réinitialisation du "
                "mot de passe par e-mail et journal des connexions, déployée de façon conteneurisée sur "
                "IBM Cloud Code Engine.",
            ),
            "Pharma-API": (
                "pharma-api",
                "Livrer une API REST de manière fiable demande d'automatiser le déploiement et de ne pas "
                "mélanger configuration et code. Le déploiement sur AWS EC2 est automatisé et la "
                "configuration de chaque environnement passe par des variables d'environnement, avec une "
                "documentation technique associée.",
            ),
            "Déployez une application Django": (
                "deployez-django",
                "Passer d'une application Django qui fonctionne en local à une application réellement "
                "servie en production : configuration, sécurité et mise en ligne.",
            ),
        }
        for title, (image, problem) in visuals.items():
            Project.objects.filter(title=title).update(
                infra_image=f"portfolio/img/infra/{image}.svg",
                problem_solved=problem,
            )


    def _seed_mpahmum_infra(self):
        """Infrastructure réelle de mpahmum.site (AWS eu-west-3, état au 3 octobre 2026)."""
        Project.objects.filter(title="Mpahmum").update(
            stack=(
                "React · TypeScript · Vite · Express · Prisma · PostgreSQL 16 · Docker Compose · "
                "Caddy · AWS (EC2, EBS, CloudWatch, SSM) · Tailwind CSS"
            ),
            problem_solved=(
                "Recueillir et conserver les témoignages et les photos des invités d'un événement est "
                "difficile sans outil dédié, et un formulaire public s'expose aux abus. L'application "
                "permet aux invités de déposer leur message via une session sécurisée par jeton, à "
                "l'administration de modérer et d'épingler les contributions, et protège l'API (helmet, "
                "liste blanche des champs, limitation de débit, réactions atomiques). Elle tourne sur une "
                "instance AWS EC2 unique derrière Caddy (HTTPS automatique), avec des snapshots EBS "
                "quotidiens, une supervision CloudWatch avec alerte par e-mail et un accès administrateur "
                "par Session Manager, sans SSH ouvert."
            ),
            infra_components=[
                {"couche": "Réseau", "outils": ["DNS LWS", "Elastic IP", "Caddy (TLS automatique, Let's Encrypt)"]},
                {"couche": "Calcul", "outils": ["AWS EC2 Ubuntu", "volume EBS gp3 20 Go", "Docker Compose"]},
                {"couche": "Application", "outils": ["Node 20", "Express", "React (build Vite)", "helmet", "limiteurs de débit"]},
                {"couche": "Données", "outils": ["PostgreSQL 16", "Prisma", "volume Docker"]},
                {"couche": "Sauvegarde", "outils": ["Snapshots EBS (DLM) quotidiens", "7 conservés"]},
                {"couche": "Supervision", "outils": ["CloudWatch (agent, alarme disque ≥ 80 %)", "SNS", "e-mail"]},
                {"couche": "Administration", "outils": ["Systems Manager (Session Manager)", "sans SSH"]},
                {"couche": "IA", "outils": ["API Google Gemini"]},
            ],
        )
