# Generated by Django 3.2.12 on 2024-08-27 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changshaapp', '0005_authenticationextractionstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('file', models.URLField(blank=True, max_length=255)),
            ],
        ),
    ]
