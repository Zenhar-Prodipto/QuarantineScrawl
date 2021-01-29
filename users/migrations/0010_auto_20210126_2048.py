# Generated by Django 3.0.8 on 2021-01-26 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_followmodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followmodel',
            name='followers',
        ),
        migrations.AddField(
            model_name='followmodel',
            name='followers',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='followmodel',
            name='follows',
        ),
        migrations.AddField(
            model_name='followmodel',
            name='follows',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
