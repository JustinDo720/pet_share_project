# Generated by Django 3.0.8 on 2020-08-01 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_dog_app', '0012_auto_20200801_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogname',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]