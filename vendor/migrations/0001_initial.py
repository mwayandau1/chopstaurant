# Generated by Django 4.2.6 on 2023-10-14 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('vendor_name', models.CharField(blank=True, max_length=120, null=True)),
                ('vendor_license', models.ImageField(blank=True, null=True, upload_to='vendor/license')),
                ('is_approved', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('ven_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='accounts.profile')),
            ],
        ),
    ]
