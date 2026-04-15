# generate_django_secret_key.py
from django.core.management.utils import get_random_secret_key

# Generate and print a secure SECRET_KEY
print(get_random_secret_key())
