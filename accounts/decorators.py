from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def redirect_authenticated_user(func):
    """ Decorator to redirect authenticated users away from auth pages."""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
    return wrapper_func


# def vendor_required(function=None, 
#         redirect_field_name=REDIRECT_FIELD_NAME,
#         login_url='accounts:login'):
#     """
#     Decorator for views that checks that the logged in user is a vendor,
#     redirects to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_vendor,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# def verification_required(f):
#     return user_passes_test(
#         lambda u: u.vendor.is_verified,
#         login_url='/account/customer/verify/')(f)
