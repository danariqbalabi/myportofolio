from django.db import migrations


def create_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="Editor")


def delete_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Editor").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_project_starred_by"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_editor_group, delete_editor_group),
    ]
