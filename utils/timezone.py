import datetime
from zoneinfo import ZoneInfo

def format_kolkata_time(dt_input) -> str:
    """
    Formats a datetime object or timestamp string into Asia/Kolkata time format:
    Example: '11-Aug-2026 08:55 PM'
    """
    if not dt_input:
        return "N/A"

    dt_obj = None
    if isinstance(dt_input, datetime.datetime):
        dt_obj = dt_input
    elif isinstance(dt_input, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                dt_obj = datetime.datetime.strptime(dt_input.split(".")[0], fmt)
                break
            except Exception:
                pass

    if not dt_obj:
        return str(dt_input)

    # Convert/Attach Asia/Kolkata timezone
    try:
        kolkata_tz = ZoneInfo("Asia/Kolkata")
        if dt_obj.tzinfo is None:
            dt_obj = dt_obj.replace(tzinfo=datetime.timezone.utc).astimezone(kolkata_tz)
        else:
            dt_obj = dt_obj.astimezone(kolkata_tz)
    except Exception:
        pass

    return dt_obj.strftime("%d-%b-%Y %I:%M %p")
