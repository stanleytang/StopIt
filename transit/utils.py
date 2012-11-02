def get_readable_time(hours, minutes):
    is_am = True
    if hours >= 12:
        is_am = False
    hours = hours % 12
    if hours == 0:
        hours = 12
    
    hours = str(hours) if hours >= 10 else "0%s" %str(hours)
    minutes = str(minutes) if minutes >= 10 else "0%s" %str(minutes)
    return "%s:%s%s" %(hours, minutes, "am" if is_am else "pm")