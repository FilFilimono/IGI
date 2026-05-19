from django.utils import timezone
import calendar
import pytz


def global_context(request):
    now = timezone.now()
    user_tz_name = 'UTC'
    if request.user.is_authenticated:
        try:
            user_tz_name = request.user.profile.timezone
        except Exception:
            pass
    try:
        user_tz = pytz.timezone(user_tz_name)
        user_now = now.astimezone(user_tz)
    except Exception:
        user_now = now

    cal = calendar.TextCalendar(calendar.MONDAY)
    cal_text = cal.formatmonth(user_now.year, user_now.month)

    return {
        'utc_now': now,
        'user_now': user_now,
        'user_timezone': user_tz_name,
        'calendar_text': cal_text,
        'current_date_formatted': user_now.strftime('%d/%m/%Y'),
    }
