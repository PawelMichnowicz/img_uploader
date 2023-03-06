# Generated by Django 4.1.7 on 2023-03-06 22:08

from django.db import migrations


def create_default_plans(apps, schema_editor):

    Plan = apps.get_model("users", "Plan")
    default_plans = [
        {
            "name": "Basic",
            "thumbnail_sizes": [200],
            "original_image_access": False,
            "expiring_image_access": False,
        },
        {
            "name": 'Premium"',
            "thumbnail_sizes": [200, 400],
            "original_image_access": True,
            "expiring_image_access": False,
        },
        {
            "name": "Enterprise",
            "thumbnail_sizes": [200, 400],
            "original_image_access": True,
            "expiring_image_access": True,
        },
    ]
    for plan in default_plans:
        plan_instance = Plan(
            name=plan["name"],
            thumbnail_sizes=plan["thumbnail_sizes"],
            original_image_access=plan["original_image_access"],
            expiring_image_access=plan["expiring_image_access"],
        )
        plan_instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_default_plans)]