# Generated by Django 3.0.8 on 2021-01-31 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210131_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_comment',
            field=models.TextField(blank=True, default=None),
        ),
    ]