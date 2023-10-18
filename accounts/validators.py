from django.core.exceptions import ValidationError
import os


def validateImages(value):
    ext = os.path.splitext(value.name)[1]
    valid_exts = ['jpg', 'jpeg', 'png', 'webp']
    if not ext.lower() in valid_exts:
        raise ValidationError(
            "Unsupported file format! Please upload a valid file extension like " + str(valid_exts))
