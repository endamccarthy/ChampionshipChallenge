# Generated by Django 3.0.7 on 2020-06-29 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0004_entry_finalists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='finalists',
        ),
        migrations.AddField(
            model_name='result',
            name='final_result',
            field=models.BooleanField(default=False),
        ),
    ]