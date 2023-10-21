from django.conf import settings
from vendor.models import Vendor


def getVendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_google_api_key(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
