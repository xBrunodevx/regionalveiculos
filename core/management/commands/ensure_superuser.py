import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Cria ou atualiza o superusuário usando variáveis de ambiente'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not username or not password:
            self.stdout.write(
                self.style.WARNING('⚠️ Variáveis DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD são obrigatórias')
            )
            return
        
        try:
            user = User.objects.filter(username=username).first()
            
            if user:
                self.stdout.write(f'🔄 Atualizando superusuário "{username}"...')
                user.set_password(password)
                if email:
                    user.email = email
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superusuário "{username}" atualizado com sucesso!')
                )
            else:
                self.stdout.write(f'🆕 Criando superusuário "{username}"...')
                User.objects.create_superuser(
                    username=username,
                    email=email or '',
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superusuário "{username}" criado com sucesso!')
                )
                
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write('🌐 Acesse: /admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao criar/atualizar superusuário: {e}')
            )
            import traceback
            traceback.print_exc()