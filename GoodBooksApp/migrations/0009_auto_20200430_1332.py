# Generated by Django 3.0.5 on 2020-04-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoodBooksApp', '0008_auto_20200430_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default_pic.jpg', upload_to='profile_pictures/'),
        ),
    ]
