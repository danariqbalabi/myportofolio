# Generated manually for the GalleryItem model.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_highlight"),
    ]

    operations = [
        migrations.CreateModel(
            name="GalleryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("caption", models.TextField(blank=True)),
                ("category", models.CharField(blank=True, max_length=100)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("year", models.PositiveIntegerField()),
                ("image", models.CharField(max_length=500)),
                ("featured", models.BooleanField(default=False)),
            ],
        ),
    ]
