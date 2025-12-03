from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings

def reset_admin_view(request):
    """
    View temporária para resetar senha do admin
    IMPORTANTE: Remover após usar!
    """
    
    # Permitir em desenvolvimento OU se senha especial for fornecida
    senha_especial = request.GET.get('senha')
    if not settings.DEBUG and senha_especial != 'RegionalVeiculos2024Reset':
        return HttpResponse("❌ Esta função só funciona em desenvolvimento ou com senha especial", status=403)
    
    User = get_user_model()
    
    try:
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
        
        status = "CRIADO" if created else "RESETADO"
        
        html = f"""
        <html>
        <head><title>Reset Senha Admin</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h2>✅ Superusuário {status} com sucesso!</h2>
            <p><strong>👤 Usuário:</strong> {username}</p>
            <p><strong>🔑 Senha:</strong> {password}</p>
            <p><strong>📧 Email:</strong> {email}</p>
            <br>
            <p><a href="/admin/" style="background: #007cba; color: white; padding: 10px; text-decoration: none;">🚀 Ir para Admin</a></p>
            <br>
            <p style="color: #666; font-size: 12px;">⚠️ IMPORTANTE: Remova esta URL após usar!</p>
        </body>
        </html>
        """
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"❌ Erro: {e}", status=500)