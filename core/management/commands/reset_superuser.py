from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Cria ou reseta a senha do superusuário de forma simples'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = 'admin'
        password = 'RegionalVeiculos2024!'
        email = 'admin@regionalveiculos.com'
        
        try:
            # Pegar ou criar usuário
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            # Sempre resetar a senha
            user.set_password(password)
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superusuário "{username}" CRIADO com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Senha do "{username}" RESETADA com sucesso!')
                )
            
            self.stdout.write(f'👤 Usuário: {username}')
            self.stdout.write(f'🔑 Senha: {password}')
            self.stdout.write(f'📧 Email: {email}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {e}')
            )