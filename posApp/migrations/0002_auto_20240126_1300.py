# Generated by Django 3.2.3 on 2024-01-26 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.RemoveField(
            model_name='products',
            name='user',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='user',
        ),
        migrations.RemoveField(
            model_name='salesitems',
            name='user',
        ),
    ]
