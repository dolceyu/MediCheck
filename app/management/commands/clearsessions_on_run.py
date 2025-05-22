from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Очищає всі сесії при запуску'

    def handle(self, *args, **kwargs):
        Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Сесії очищено."))
