# Generated by Django 3.0.5 on 2020-04-29 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GoodBooksApp', '0004_auto_20200429_1736'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set(),
        ),
    ]
