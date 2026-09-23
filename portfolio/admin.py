from django.contrib import admin

from .models import (
    Certification,
    Experience,
    ExperienceHighlight,
    Profile,
    Project,
    Skill,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "location")

    def has_add_permission(self, request):
        # Une seule instance de profil autorisée.
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order")
    list_filter = ("category",)
    list_editable = ("proficiency", "order")
    ordering = ("category", "order")


class ExperienceHighlightInline(admin.TabularInline):
    model = ExperienceHighlight
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "start_date", "end_date", "order")
    inlines = [ExperienceHighlightInline]
    ordering = ("order", "-start_date")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "order")
    list_editable = ("is_featured", "order")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "status", "date_obtained", "order")
    list_filter = ("status", "issuer")
    list_editable = ("order",)
