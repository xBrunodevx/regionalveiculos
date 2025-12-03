"""
Configurações específicas para o Render - mídia e static files
"""
import os
from .settings import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Debug False para produção
DEBUG = False

# CORS e CSRF para produção
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://regional-veiculos.onrender.com',
]

# Configuração de arquivos estáticos para produção
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise para servir arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# CONFIGURAÇÃO CLOUDINARY PARA MÍDIA
# Usando CLOUDINARY_URL (mais simples)
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

# Storage para arquivos de mídia
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# URLs de mídia - usar Cloudinary
MEDIA_URL = '/media/'

# Adicionar cloudinary_storage aos INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'crispy_forms',
    'cloudinary_storage',
    'cloudinary',
    'core',
    'contato',
]

# Configurações de upload para permitir vários formatos
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024   # 50MB

# Formatos de imagem permitidos
ALLOWED_IMAGE_FORMATS = [
    'JPEG', 'PNG', 'GIF', 'BMP', 'WEBP', 'TIFF'
]

# Middleware atualizado
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise para static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações de segurança para produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Configuração de log para debug de mídia
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cloudinary': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}