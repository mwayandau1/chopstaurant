from django.db import models
from accounts.models import User, Profile
import uuid


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    ven_profile = models.OneToOneField(
        Profile, related_name='userprofile', on_delete=models.CASCADE)
    ven_name = models.CharField(max_length=120, null=True, blank=True)
    ven_license = models.ImageField(
        upload_to='vendor/license', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
