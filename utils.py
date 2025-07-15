from datetime import datetime
import pytz


def get_india_timestamp():
    utc_now = datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = pytz.utc.localize(utc_now).astimezone(ist)
    return ist_now.strftime("%Y-%m-%d %H:%M:%S")
