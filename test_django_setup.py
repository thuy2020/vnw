# test_django_setup.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vnw.settings')
django.setup()

from people.models import Person

print("Django setup completed and Person model accessed successfully.")
