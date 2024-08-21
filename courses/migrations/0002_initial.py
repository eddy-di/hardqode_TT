# Generated by Django 4.2.10 on 2024-08-20 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcustomusers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='courses.course'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='group', through='courses.GroupCustomUsers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='groupcustomusers',
            unique_together={('group', 'user')},
        ),
    ]
