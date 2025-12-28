import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

# Ensure Hira exists
if not User.objects.filter(first_name='Hira').exists():
    print("Creating user Hira...")
    User.objects.create_user(email='hira@pucit.edu.pk', password='password123', first_name='Hira', last_name='Khan')

hira = User.objects.get(email='hira@pucit.edu.pk')

client = APIClient()
client.force_authenticate(user=hira)
response = client.get('/api/search/users/', {'q': 'Hira'})

print(f"Status Code: {response.status_code}")
print(f"Data: {response.data}")
