# Generated by Django 4.1.3 on 2023-02-12 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_customuser_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="number_of_attempts",
            field=models.DecimalField(decimal_places=0, default=5, max_digits=1),
        ),
    ]
