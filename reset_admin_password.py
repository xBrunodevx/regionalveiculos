#!/usr/bin/env python
"""
Script para resetar a senha do superusuário admin
"""
import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')
django.setup()

User = get_user_model()

def reset_admin_password():
    username = 'admin'
    new_password = 'RegionalVeiculos2024!'
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email = 'admin@regionalveiculos.com'
        user.save()
        
        print(f"✅ Senha do usuário '{username}' foi resetada com sucesso!")
        print(f"🔑 Nova senha: {new_password}")
        print(f"📧 Email: {user.email}")
        print(f"🌐 Teste em: http://127.0.0.1:8000/admin/")
        
    except User.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado!")

if __name__ == '__main__':
    reset_admin_password()