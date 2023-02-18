# Generated by Django 4.0 on 2023-02-17 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("books", "0005_remove_book_author_book_authors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="book",
                to="auth.user",
            ),
        ),
    ]
