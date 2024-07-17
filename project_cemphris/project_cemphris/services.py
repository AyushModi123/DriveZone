from notif_handler.utils import schedule_email as _schedule_email
from notif_handler.tasks import send_email

def schedule_email(*args, **kwargs):
    return _schedule_email(*args, **kwargs)
