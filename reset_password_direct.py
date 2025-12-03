#!/usr/bin/env python
"""
SCRIPT DIRETO PARA RESETAR SENHA - Execute este comando no console do Render
"""

# Cole este código direto no console do Render ou execute via shell

from django.contrib.auth import get_user_model
User = get_user_model()

# Resetar senha do admin
username = 'admin'
password = 'RegionalVeiculos2024!'
email = 'admin@regionalveiculos.com'

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)

user.set_password(password)
user.email = email
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print(f'✅ Superusuário "{username}" CRIADO!')
else:
    print(f'✅ Senha do "{username}" RESETADA!')

print(f'👤 Usuário: {username}')
print(f'🔑 Senha: {password}')
print(f'📧 Email: {email}')