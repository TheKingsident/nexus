from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser for Railway deployment'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from arguments or environment variables
        username = options.get('username') or os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = options.get('email') or os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = options.get('password') or os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists!')
            )
            return
        
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!')
            )
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Password: {"*" * len(password)}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to create superuser: {e}')
            )
