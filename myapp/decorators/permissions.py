
from functools import wraps

from django.core.exceptions import PermissionDenied


def has_role_permission(role_names):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.groups.filter(name__in=role_names).exists():
                return dispatch(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return request_decorator
