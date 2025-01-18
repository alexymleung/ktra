import os
from django.core.management.base import BaseCommand
from services.models import Service  # Replace with your actual model
from urllib.request import urlopen
from urllib.error import URLError

class Command(BaseCommand):
    help = 'Check if the image file exists and update the database if it does not'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.stdout.write(f'Base directory: {base_dir}')

        for instance in Service.objects.all():
            updated = False
            for field in ['photo_1', 'photo_2', 'photo_3', 'photo_4']:
                photo = getattr(instance, field)
                if photo:
                    self.stdout.write(f'Checking {field} for instance {instance.id}: {photo.url}')
                    if photo.url.startswith('/media/'):
                        # Check local file path
                        file_path = os.path.join(base_dir, "../..",photo.url.lstrip('/'))
                        self.stdout.write(f'Local file path: {file_path}')
                        if os.path.exists(file_path):
                            self.stdout.write(self.style.SUCCESS(f'Image file exists for {instance.id} ({field})'))
                        else:
                            setattr(instance, field, None)  # Set to None or any value as needed
                            self.stdout.write(self.style.ERROR(f'Updated record for {instance.id} ({field}), image file not found'))
                            updated = True
                    else:
                        # Check remote URL
                        try:
                            urlopen(photo.url)
                            self.stdout.write(self.style.SUCCESS(f'Image file exists for {instance.id} ({field})'))
                        except URLError:
                            setattr(instance, field, None)  # Set to None or any value as needed
                            self.stdout.write(self.style.ERROR(f'Updated record for {instance.id} ({field}), image file not found'))
                            updated = True
            if updated:
                instance.save()
