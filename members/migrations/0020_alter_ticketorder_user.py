# Generated by Django 5.1.2 on 2024-10-27 03:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0019_alter_ticketorder_order_sum_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketorder",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
