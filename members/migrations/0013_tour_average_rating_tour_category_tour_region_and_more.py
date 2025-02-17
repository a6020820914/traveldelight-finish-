# Generated by Django 5.1.1 on 2024-10-24 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0012_subscriber"),
    ]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="average_rating",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name="tour",
            name="category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="tour",
            name="region",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="tour",
            name="season",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="tour",
            name="tags",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="tour",
            name="view_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="UserBehavior",
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
                ("action_type", models.CharField(max_length=20)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="members.tour"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
