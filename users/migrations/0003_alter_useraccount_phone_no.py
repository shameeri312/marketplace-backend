# Generated by Django 5.1.5 on 2025-01-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_useraccount_country_alter_useraccount_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='phone_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
