from django.db import migrations
import os


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    if not username or not password:
        # required env not present; skip
        return
    try:
        u = User.objects.filter(username=username).first()
        if u:
            u.set_password(password)
            if email:
                u.email = email
            u.is_staff = True
            u.is_superuser = True
            u.save()
        else:
            User.objects.create_superuser(username=username, email=email or '', password=password)
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
