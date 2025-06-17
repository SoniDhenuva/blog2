from datetime import datetime

def timeStamp():
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d%H%M%S")

    year = timestamp_str[:4]    # First 4 characters (YYYY)
    month = timestamp_str[4:6]  # Next 2 characters (MM)
    day = timestamp_str[6:8]    # Next 2 characters (DD)
    hour = timestamp_str[8:10]  # Next 2 characters (HH)
    minute = timestamp_str[10:12] # Next 2 characters (MM)
    second = timestamp_str[12:14] # Last 2 characters (SS)

    return f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}"

hello = timeStamp()
print(hello)
