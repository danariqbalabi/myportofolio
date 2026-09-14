# this ppage was generated manually for the highlight model.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Highlight",
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
                ("description", models.TextField()),
                ("category", models.CharField(max_length=100)),
                ("year", models.PositiveIntegerField()),
                ("thumbnail", models.URLField(blank=True, null=True)),
            ],
        ),
    ]
