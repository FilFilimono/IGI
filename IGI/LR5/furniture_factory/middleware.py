import pytz
import logging
from django.utils import timezone

logger = logging.getLogger('django')


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz_name = None
        if request.user.is_authenticated:
            try:
                tz_name = request.user.profile.timezone
            except Exception:
                pass
        if not tz_name:
            tz_name = request.session.get('django_timezone', 'UTC')
        try:
            timezone.activate(pytz.timezone(tz_name))
        except Exception:
            timezone.deactivate()
        response = self.get_response(request)
        return response
