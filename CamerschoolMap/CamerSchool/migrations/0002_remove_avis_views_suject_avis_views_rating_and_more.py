# Generated by Django 4.2.17 on 2025-03-13 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CamerSchool', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avis_views',
            name='suject',
        ),
        migrations.AddField(
            model_name='avis_views',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='avis_views',
            name='type_avis',
            field=models.CharField(choices=[('site', 'Site en général'), ('etablissement', 'Établissement spécifique')], max_length=20),
        ),
    ]
