from django.db import migrations
import os


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    if not username or not password:
        print('⚠️ Variáveis de ambiente do superusuário não encontradas, pulando criação...')
        return
        
    try:
        u = User.objects.filter(username=username).first()
        if u:
            print(f'🔄 Atualizando superusuário "{username}"...')
            u.set_password(password)
            if email:
                u.email = email
            u.is_staff = True
            u.is_superuser = True
            u.is_active = True
            u.save()
            print(f'✅ Superusuário "{username}" atualizado com sucesso!')
        else:
            print(f'🆕 Criando superusuário "{username}"...')
            User.objects.create_superuser(username=username, email=email or '', password=password)
            print(f'✅ Superusuário "{username}" criado com sucesso!')
    except Exception as e:
        import traceback
        print('❌ ERROR creating/updating superuser:', e)
        traceback.print_exc()
        return


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_imagem_site_model'),
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse_code=migrations.RunPython.noop),
    ]
