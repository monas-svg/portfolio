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
        self._seed_certifications()
        self.stdout.write(self.style.SUCCESS("Contenu du portfolio initialisé."))

    def _seed_profile(self):
        Profile.objects.update_or_create(
            pk=1,
            defaults=dict(
                full_name="Mohamed Nasser Mounchikpou Njiemessa",
                headline="Ingénieur DevOps & Cloud Engineer — AWS & Azure Certified | IA Générative Appliquée",
                location="Douala, Cameroun",
                email="mohamednassernjiemessa@gmail.com",
                phone="+237 690 87 29 82",
                github_url="https://github.com/monassvg",
                linkedin_url="https://linkedin.com/in/mohamed-nasser-mounchikpou",
                years_experience=4,
                summary=(
                    "DevOps et Multi-Cloud avec plus de 4 ans d'expérience dans la coordination de "
                    "projets IT et le développement backend. En cours de certification AWS Solutions "
                    "Architect Associate (SAA-C03), et récemment certifié Microsoft Azure Developer "
                    "Associate (AZ-204), Microsoft Azure Fundamentals (AZ-900) et AWS Cloud Practitioner "
                    "(CLF-C02), je combine une forte expertise en développement Python/Django avec "
                    "l'administration d'infrastructures cloud hybrides et scalables. Spécialiste de la "
                    "conteneurisation (Docker), de l'orchestration Kubernetes (Helm) et de "
                    "l'infrastructure as code (Terraform), des environnements Linux et de "
                    "l'automatisation de pipelines CI/CD (GitHub Actions). Fort de mes certifications "
                    "Google AI Professional, Google Prompting Essentials, ainsi que Claude Code 101 et "
                    "Claude Platform 101 (Anthropic), j'intègre activement l'IA générative — y compris "
                    "les outils IA agentiques comme Claude — pour accélérer le développement, optimiser "
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
            ("CI/CD — GitHub Actions", SkillCategory.CLOUD_DEVOPS, 5, 6),
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
                "Développement et déploiement d'APIs REST (Django) sur serveurs Linux — Nginx, SSL, variables d'env.",
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
                title="SwingBot — Infrastructure DevOps & Multi-Cloud",
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
                repo_url="https://github.com/KenmogneThimotee/swingbot",
                is_featured=True,
                order=1,
            ),
            dict(
                title="SecurAuth-API",
                summary="API d'authentification JWT déployée sur IBM Cloud.",
                description=(
                    "Configuration serveur Linux, gestion des variables d'environnement, reverse proxy "
                    "et monitoring des logs."
                ),
                stack="IBM Cloud · Linux · JWT · API REST · Python",
                repo_url="https://github.com/monas-svg/SecurAuth-API",
                is_featured=False,
                order=2,
            ),
            dict(
                title="Pharma-API",
                summary="API REST complète avec déploiement automatisé sur AWS EC2.",
                description="Gestion des environnements via variables d'environnement et documentation technique.",
                stack="Python · Django · API REST · CI/CD · AWS EC2",
                repo_url="https://github.com/monas-svg/Pharma-API",
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
                repo_url="https://github.com/monas-svg/certifPro",
                is_featured=False,
                order=4,
            ),
            dict(
                title="Déployez une application Django",
                summary="Mise en pratique du déploiement d'une application Django en production (OpenClassrooms).",
                description="",
                stack="Python · Django · Déploiement",
                repo_url="https://github.com/monas-svg/deployez_une_application_django",
                is_featured=False,
                order=5,
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
