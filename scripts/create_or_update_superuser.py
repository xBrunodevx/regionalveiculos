import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
password = 'S3nh@F0rte!2025'
email = 'admin@regionalveiculos.local'

user, created = User.objects.update_or_create(
    username=username,
    defaults={
        'email': email,
        'is_superuser': True,
        'is_staff': True,
        'is_active': True,
    }
)
user.set_password(password)
user.save()

print(('created' if created else 'updated') + ' ' + user.username)
print('USERNAME:', username)
print('PASSWORD:', password)
