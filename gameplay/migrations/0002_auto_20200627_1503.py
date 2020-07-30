# Generated by Django 3.0.7 on 2020-06-27 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('name', 'sport'), name='unique team'),
        ),
    ]