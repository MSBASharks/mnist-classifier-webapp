from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Creates the required instructor account (username 'dan') if it doesn't
    already exist. Safe to run every time the container starts — it's a
    no-op if the account is already there, so it won't reset the password
    on every restart or error out on a second run.

    This satisfies the assignment's explicit requirement:
    "Create an account for me with username: dan and password: Optimization1234"
    """
    help = "Creates the instructor account (dan) if it doesn't already exist."

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'dan'
        password = 'Optimization1234'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"User '{username}' already exists — skipping."))
            return

        User.objects.create_superuser(username=username, password=password, email='')
        self.stdout.write(self.style.SUCCESS(f"Created instructor account '{username}'."))
