# Generated by Django 3.0.8 on 2020-10-10 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='poseidon.jpg', upload_to='profile_pics'),
        ),
    ]
