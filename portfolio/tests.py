from django.test import TestCase
from django.urls import reverse

from .models import Profile, Project


class HomeViewTests(TestCase):
    def setUp(self):
        Profile.objects.create(
            full_name="Test User",
            headline="DevOps Engineer",
            summary="Résumé de test.",
            years_experience=4,
        )
        Project.objects.create(
            title="Projet Test",
            summary="Résumé projet",
            stack="Docker · Kubernetes",
        )

    def test_home_page_returns_200(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_lists_project(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, "Projet Test")


class ProjectModelTests(TestCase):
    def test_stack_list_splits_on_separator(self):
        project = Project.objects.create(
            title="Exemple",
            summary="s",
            stack="Docker · Kubernetes · Terraform",
        )
        self.assertEqual(project.stack_list, ["Docker", "Kubernetes", "Terraform"])

    def test_slug_is_generated_from_title(self):
        project = Project.objects.create(title="Mon Super Projet", summary="s", stack="Docker")
        self.assertEqual(project.slug, "mon-super-projet")
