from notif_handler.utils import schedule_email as _schedule_email, \
      send_email as _send_email

def schedule_email(*args, **kwargs):
    return _schedule_email(*args, **kwargs)

def send_email(*args, **kwargs):
    return _send_email(*args, **kwargs)