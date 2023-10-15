

def getAccountUrl(request):
    if request.user.role == 1:
        redirectUrl = 'vendor-dashboard'
        return redirectUrl
    elif request.user.role == 2:
        redirectUrl = 'customer-dashboard'
        return redirectUrl
    elif request.user.role == None and request.user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
