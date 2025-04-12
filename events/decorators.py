from functools import wraps
from django.shortcuts import render

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'events,access_denied.html')
        return view_func(request, *args, **kwargs)
    return wrapper