from django.db import models
from accounts.models import User, Profile
import uuid

from accounts.utils import send_email_approval


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

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                email_template = 'accounts/email/send-email-approval.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    mail_subject = "Congratulations! Your restaurant has been approved for service"
                    send_email_approval(
                        mail_subject=mail_subject, email_template=email_template, context=context)
                else:
                    mail_subject = "We're sorry, Your restaurant has not been approved for service!"
                    send_email_approval(
                        mail_subject=mail_subject, email_template=email_template, context=context)

        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.firstName
