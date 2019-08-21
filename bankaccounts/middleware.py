from .utils import set_audit_user


class AuditUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        audit_user = request.user
        if audit_user is not None:
            set_audit_user(audit_user)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
