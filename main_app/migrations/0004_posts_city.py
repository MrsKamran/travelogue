# Generated by Django 3.1.1 on 2020-11-13 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='city',
            field=models.CharField(default='city', max_length=100),
            preserve_default=False,
        ),
    ]