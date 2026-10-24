from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("portfolio", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="project",
            name="repo_private",
            field=models.BooleanField(
                default=False,
                help_text="Affiche « lien privé » à la place du lien du dépôt.",
            ),
        ),
    ]
