import time
import datetime

def FormatTime(time):
    # Extract whole seconds and milliseconds
    seconds = int(time)
    milliseconds = int((time - seconds) * 1000)

    # Compute Days
    days = seconds // (24 * 3600)
    
    # Compute hours, minutes, and seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60


    # Return including days
    if days != 0:
        return "%d:%d:%02d:%02d.%03d" % (days, hour, minutes, seconds, milliseconds)
    
    # Return including hours
    elif hour != 0:
        return "%d:%02d:%02d.%03d" % (hour, minutes, seconds, milliseconds)
    
    # Return including hours
    else:
        return "%02d:%02d.%03d" % (minutes, seconds, milliseconds)
    
def ConvertToUnixDate(date_str, format_str='%Y-%m-%d %H:%M:%S'):
    try:
        datetime_obj = datetime.strptime(date_str, format_str)
        unix_timestamp = time.mktime(datetime_obj.timetuple())
        return unix_timestamp
    except ValueError as e:
        return str(e)
    
def ConvertToFormattedDate(unix_timestamp, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Convert a Unix timestamp into a formatted date string.
    
    :param unix_timestamp: The Unix timestamp to convert.
    :param format_str: The format for the output date string.
    :return: Formatted date string corresponding to the given Unix timestamp.
    """
    datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
    formatted_date = datetime_obj.strftime(format_str)
    return formatted_date
