#!/usr/bin/env python
"""
Script para garantir que o superusuário existe no ambiente de produção
"""
import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')
django.setup()

User = get_user_model()

# Dados do superusuário para produção
username = 'admin'
email = 'admin@regionalveiculos.com'
password = 'RegionalVeiculos2024!'  # Nova senha mais segura

try:
    # Verificar se o usuário já existe
    user = User.objects.filter(username=username).first()
    
    if user:
        print(f'🔄 Atualizando superusuário "{username}"...')
        user.set_password(password)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print(f'✅ Superusuário "{username}" atualizado com sucesso!')
    else:
        print(f'🆕 Criando novo superusuário "{username}"...')
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Superusuário "{username}" criado com sucesso!')
    
    print(f'📧 Email: {email}')
    print(f'🔑 Nova senha: {password}')
    print(f'🌐 URL Admin: https://regional-veiculos.onrender.com/admin/')
    
except Exception as e:
    print(f'❌ Erro ao criar/atualizar superusuário: {e}')
    import traceback
    traceback.print_exc()