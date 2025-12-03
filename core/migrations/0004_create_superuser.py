from django.db import migrations
import os


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = 'admin'
    email = 'admin@regionalveiculos.com'
    password = 'RegionalVeiculos2024!'  # Nova senha mais segura
    
    try:
        u = User.objects.filter(username=username).first()
        if u:
            u.set_password(password)
            if email:
                u.email = email
            u.is_staff = True
            u.is_superuser = True
            u.is_active = True
            u.save()
            print(f'✅ Superusuário "{username}" atualizado!')
        else:
            User.objects.create_superuser(username=username, email=email or '', password=password)
            print(f'✅ Superusuário "{username}" criado!')
    except Exception as e:
        # Print traceback so deployment logs capture the root cause (helps debugging on Railway)
        import traceback
        print('ERROR creating/updating superuser:', e)
        traceback.print_exc()
        # don't re-raise to avoid failing the whole migration; operator can inspect logs
        return


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_imagem_site_model'),
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse_code=migrations.RunPython.noop),
    ]
