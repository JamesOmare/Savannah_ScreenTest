# Generated by Django 5.0.6 on 2024-06-23 18:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0002_rename_first_name_customer_username_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customer",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
