from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


class CheckCompleteProfile:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user

        if user.is_authenticated:

            if not user.first_name and not user.last_name and not user.username:
                return redirect(f"/v1/account/profile/{request.user.id}")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response