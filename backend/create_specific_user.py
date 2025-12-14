import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
email = "shayan@pucit.edu.pk"
password = "emaan@123"

if not User.objects.filter(email=email).exists():
    print(f"Creating user {email}...")
    # Username is usually required, using email prefix or email itself depending on model
    # Assuming custom model using email as username or just email
    try:
        # Try creating with username=email if that field exists, or just email
        # Adjust logic based on User model. 
        # Safest is to check if username field exists.
        fields = {f.name for f in User._meta.get_fields()}
        
        user_data = {'email': email, 'password': password}
        if 'username' in fields:
             user_data['username'] = email.split('@')[0]
             
        user = User.objects.create_superuser(**user_data)
        print(f"User {email} created successfully.")
    except Exception as e:
        print(f"Error creating user: {e}")
else:
    print(f"User {email} already exists.")
