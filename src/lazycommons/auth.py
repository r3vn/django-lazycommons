import base64

from django.http import HttpResponse 
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

def require_basicauth(view):
    """
    Decorator that enforces HTTP Basic Authentication on a Django views.    
    """
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode(
                        "utf8"
                    ).split(':', 1)
                    user = authenticate(username=uname, password=passwd)

                    if user is not None and user.is_active:
                        request.user = user

                        # Update last_login on django
                        update_last_login(None, user)

                        # Auth ok, return response
                        return view(request, *args, **kwargs)
        
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format(
            ""
        )
        return response
    return wrap
