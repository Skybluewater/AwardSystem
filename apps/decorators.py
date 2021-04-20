from django.contrib.auth.decorators import login_required, user_passes_test
import AwardSystem.settings as settings


def superuser_required(login_url=None):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url=login_url)


def anonymous_required(function=None, anonymous_url=None, redirect_url=None):
    if not anonymous_url:
        anonymous_url = settings.ANONYMOUS_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=anonymous_url,
        redirect_field_name=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


from django.core.exceptions import PermissionDenied


def superuser_only(function):
    """Limit view to superusers only."""

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner
