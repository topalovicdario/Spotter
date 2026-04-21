from django.apps import AppConfig


class SpotterConfig(AppConfig):
    name = 'spotter'

    def ready(self):
        import os
        from .models import User  # Use custom User model
        # Create superuser on startup if none exists (for development/production setup)
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD', 'changeme123')
            )
