from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
import os

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


def test_media_view(request):
    """
    View para testar se os arquivos de mídia estão sendo servidos corretamente
    """
    
    # Só permitir em desenvolvimento
    if not settings.DEBUG:
        senha_especial = request.GET.get('senha')
        if senha_especial != 'TestMedia2024':
            return HttpResponse("❌ Esta função só funciona em desenvolvimento", status=403)
    
    # Verificar configurações de mídia
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    media_url = getattr(settings, 'MEDIA_URL', None)
    static_root = getattr(settings, 'STATIC_ROOT', None)
    static_url = getattr(settings, 'STATIC_URL', None)
    
    # Listar arquivos de mídia
    media_files = []
    if media_root and os.path.exists(media_root):
        for root, dirs, files in os.walk(media_root):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), media_root)
                media_files.append(rel_path.replace('\\', '/'))
    
    # Listar arquivos estáticos
    static_files = []
    static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
    if os.path.exists(static_images_dir):
        for file in os.listdir(static_images_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
                static_files.append(f'images/{file}')
    
    html = f"""
    <html>
    <head><title>Teste de Mídia</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>🔍 Diagnóstico de Mídia e Imagens</h2>
        
        <h3>📋 Configurações:</h3>
        <p><strong>MEDIA_ROOT:</strong> {media_root}</p>
        <p><strong>MEDIA_URL:</strong> {media_url}</p>
        <p><strong>STATIC_ROOT:</strong> {static_root}</p>
        <p><strong>STATIC_URL:</strong> {static_url}</p>
        <p><strong>DEBUG:</strong> {settings.DEBUG}</p>
        
        <h3>📂 Arquivos de Mídia:</h3>
        <ul>
            {''.join([f'<li><a href="{media_url}{file}" target="_blank">{file}</a></li>' for file in media_files[:20]])}
        </ul>
        
        <h3>🖼️ Arquivos Estáticos (Imagens):</h3>
        <ul>
            {''.join([f'<li><a href="{static_url}{file}" target="_blank">{file}</a></li>' for file in static_files[:20]])}
        </ul>
        
        <h3>🧪 Teste de Imagens:</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            {''.join([f'<img src="{static_url}{file}" alt="{file}" style="max-width: 100px; max-height: 100px; border: 1px solid #ccc;">' for file in static_files[:10]])}
        </div>
        
        <br>
        <p><a href="/admin/" style="background: #007cba; color: white; padding: 10px; text-decoration: none;">🚀 Ir para Admin</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)