# Generated by Django 3.2.11 on 2022-02-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20220202_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
