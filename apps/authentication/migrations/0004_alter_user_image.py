# Generated by Django 4.0 on 2022-07-10 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='profile/photos/default.png', null=True, upload_to='profile/photos'),
        ),
    ]
