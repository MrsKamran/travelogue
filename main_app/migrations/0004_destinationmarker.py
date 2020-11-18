# Generated by Django 3.1.1 on 2020-11-18 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20201116_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=12)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.posts')),
            ],
        ),
    ]
