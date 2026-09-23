from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """Instance unique : identité et pitch affichés dans le hero et le footer."""

    full_name = models.CharField(max_length=120)
    headline = models.CharField(
        max_length=200,
        help_text="Ligne de statut affichée sous le nom (ex. rôle + spécialités).",
    )
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    summary = models.TextField(help_text="Paragraphe de présentation (profil professionnel).")
    years_experience = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # Empêche la création de plusieurs profils : un portfolio, une identité.
        self.pk = 1
        super().save(*args, **kwargs)


class SkillCategory(models.TextChoices):
    CLOUD_DEVOPS = "cloud_devops", "Cloud & DevOps"
    LINUX_SCRIPTING = "linux_scripting", "Linux & Scripting"
    NETWORK_SECURITY = "network_security", "Réseau & Sécurité"
    DEVELOPMENT = "development", "Développement"
    AI_PROMPTING = "ai_prompting", "IA & Prompting"
    PROJECT_MGMT = "project_mgmt", "Gestion de projet"


class Skill(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=30, choices=SkillCategory.choices)
    proficiency = models.PositiveSmallIntegerField(
        default=4,
        help_text="Niveau de maîtrise indicatif, de 1 (notions) à 5 (expert).",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Laisser vide si poste actuel.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"

    def __str__(self):
        return f"{self.role} — {self.organization}"

    @property
    def is_current(self):
        return self.end_date is None


class ExperienceHighlight(models.Model):
    experience = models.ForeignKey(Experience, related_name="highlights", on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Point clé d'expérience"
        verbose_name_plural = "Points clés d'expérience"

    def __str__(self):
        return self.text[:60]


class Project(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    summary = models.CharField(max_length=280, help_text="Résumé court affiché sur la carte projet.")
    description = models.TextField(blank=True, help_text="Description détaillée (optionnelle).")
    stack = models.CharField(
        max_length=300, help_text="Technologies séparées par ' · ' (ex. Kubernetes · Helm · Terraform)."
    )
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-is_featured", "title"]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def stack_list(self):
        return [item.strip() for item in self.stack.split("·") if item.strip()]


class CertificationStatus(models.TextChoices):
    OBTAINED = "obtained", "Obtenue"
    IN_PROGRESS = "in_progress", "En cours"


class Certification(models.Model):
    name = models.CharField(max_length=180)
    issuer = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20, choices=CertificationStatus.choices, default=CertificationStatus.OBTAINED
    )
    date_obtained = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=80, blank=True)
    credential_url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date_obtained"]
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return self.name
