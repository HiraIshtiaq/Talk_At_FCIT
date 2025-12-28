import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from apps.discussions.views import PostListCreateView

factory = APIRequestFactory()
request = factory.get('/api/discussions/posts/', {'search': 'test'})
view = PostListCreateView.as_view()
response = view(request)

print(f"Status Code: {response.status_code}")
print(f"Data Type: {type(response.data)}")
if hasattr(response.data, 'keys'):
    print(f"Keys: {response.data.keys()}")
    if 'results' in response.data:
        print(f"Results Count: {len(response.data['results'])}")
else:
    print(f"Data: {response.data}")
