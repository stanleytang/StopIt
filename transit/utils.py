def get_readable_time(hours, minutes):
    is_am = True
    if hours >= 12:
        is_am = False
    hours = hours % 12
    if hours == 0:
        hours = 12
    
    return "%s:%s%s" %(str(hours), str(minutes), "am" if is_am else "pm")