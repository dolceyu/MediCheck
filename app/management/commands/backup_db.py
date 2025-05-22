import os
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Створює резервну копію бази даних у форматі .json'

    def handle(self, *args, **kwargs):
        now = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backup_{now}.json'
        path = os.path.join('backups', filename)

        os.makedirs('backups', exist_ok=True)

        os.system(f'python manage.py dumpdata --indent 2 > {path}')
        self.stdout.write(self.style.SUCCESS(f'✅ Бекап збережено як {path}'))
