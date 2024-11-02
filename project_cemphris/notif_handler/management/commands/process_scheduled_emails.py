from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import ScheduledEmail
from ...utils import send_scheduled_email

class Command(BaseCommand):
    help = 'Send scheduled emails that are due'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Perform a dry run')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        due_emails = ScheduledEmail.objects.filter(
            scheduled_time__lte=timezone.now(),
            status='PENDING'
        )
        
        self.stdout.write(f"Found {due_emails.count()} emails to send")
        
        for email in due_emails:
            if not dry_run:
                send_scheduled_email(email)
                self.stdout.write(f"Sent email {email.id}")
            else:
                self.stdout.write(f"Would send email {email.id}")