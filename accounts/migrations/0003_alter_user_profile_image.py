# Generated by Django 3.2.13 on 2023-05-24 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_like_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='accounts/avatar.png', upload_to=''),
        ),
    ]
