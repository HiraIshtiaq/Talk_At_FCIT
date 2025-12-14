
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_users():
    users_data = [
        {"email": "alice@pucit.edu.pk", "first_name": "Alice", "last_name": "Wonder", "password": "password123"},
        {"email": "bob@pucit.edu.pk", "first_name": "Bob", "last_name": "Builder", "password": "password123"},
        {"email": "charlie@pucit.edu.pk", "first_name": "Charlie", "last_name": "Chaplin", "password": "password123"},
    ]

    for data in users_data:
        if not User.objects.filter(email=data["email"]).exists():
            User.objects.create_user(
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                role='user',
                is_verified=True
            )
            print(f"Created user: {data['email']}")
        else:
            print(f"User already exists: {data['email']}")

if __name__ == "__main__":
    create_users()
