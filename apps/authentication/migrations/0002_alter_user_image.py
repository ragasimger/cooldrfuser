# Generated by Django 4.0 on 2022-07-10 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='profile/photos'),
        ),
    ]
