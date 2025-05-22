import sqlite3
from django.conf import settings

# Імпортуємо Django, якщо треба (якщо запускаєш поза manage.py)
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medi_check.settings')  # заміни!
import django
django.setup()

# Отримуємо шлях до бази з settings.py
db_path = settings.DATABASES['default']['NAME']

conn = sqlite3.connect(db_path)
with open('schema.sql', 'w', encoding='utf-8') as f:
    for line in conn.iterdump():
        f.write(f'{line}\n')

print("✅ Схему збережено в schema.sql")
