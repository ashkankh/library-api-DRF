# Generated by Django 4.0 on 2023-02-13 17:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("title", models.CharField(blank=True, max_length=250)),
                ("subtitle", models.CharField(blank=True, max_length=250)),
                ("author", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
        ),
    ]