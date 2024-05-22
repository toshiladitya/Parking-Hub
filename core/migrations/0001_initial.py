# Generated by Django 5.0.6 on 2024-05-20 09:07

import core.models.admin_profile
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('super_admin', 'Super Admin'), ('admin', 'Admin'), ('sub_admin', 'Sub Admin')], max_length=30)),
                ('phone', models.CharField(max_length=10, unique=True, validators=[core.models.admin_profile.validate_phone])),
                ('password', models.CharField(max_length=50)),
                ('country_code', models.CharField(default='+91', max_length=5)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('intro', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=50)),
                ('super_admin', models.BooleanField(default=False)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('admins', models.ManyToManyField(blank=True, null=True, related_name='admins_profile_admins', to='core.adminprofile')),
            ],
            options={
                'db_table': 'admin_profile',
            },
        ),
    ]