# Generated by Django 3.0.8 on 2020-08-13 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_dog_app', '0017_auto_20200810_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogname',
            name='owner_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='test_dog_app.Profile'),
            preserve_default=False,
        ),
    ]
