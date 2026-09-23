from itertools import groupby

from django.shortcuts import render

from .models import Certification, Experience, Profile, Project, Skill, SkillCategory


def home(request):
    profile = Profile.objects.first()

    skills = Skill.objects.all()
    skills_by_category = []
    for key, group in groupby(skills, key=lambda s: s.category):
        skills_by_category.append(
            {
                "label": SkillCategory(key).label,
                "items": list(group),
            }
        )

    context = {
        "profile": profile,
        "skills_by_category": skills_by_category,
        "experiences": Experience.objects.prefetch_related("highlights"),
        "projects": Project.objects.all(),
        "certifications": Certification.objects.all(),
    }
    return render(request, "portfolio/home.html", context)
