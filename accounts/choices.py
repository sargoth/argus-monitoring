from zoneinfo import available_timezones


def fetch_timezone_choices():
    return [(tz, tz) for tz in sorted(available_timezones())]
