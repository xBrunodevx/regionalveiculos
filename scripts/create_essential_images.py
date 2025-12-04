#!/usr/bin/env python
"""
Script para criar imagens essenciais que faltam no static
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_favicon():
    """Criar favicon básico"""
    # Criar favicon 32x32
    img = Image.new('RGB', (32, 32), color='#dc3545')
    draw = ImageDraw.Draw(img)
    
    # Desenhar "RV" no favicon
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "RV"
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (32 - text_width) // 2
        y = (32 - text_height) // 2
        draw.text((x, y), text, fill='white', font=font)
    
    return img

def create_logo():
    """Criar logo básico"""
    img = Image.new('RGB', (200, 60), color='#dc3545')
    draw = ImageDraw.Draw(img)
    
    # Desenhar texto do logo
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "REGIONAL VEÍCULOS"
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (200 - text_width) // 2
        y = (60 - text_height) // 2
        draw.text((x, y), text, fill='white', font=font)
    
    return img

def create_essential_images():
    """Criar imagens essenciais para o static"""
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    static_images_dir = project_dir / 'static' / 'images'
    
    print("🔧 Criando imagens essenciais para static...")
    
    # Criar favicon 32x32
    favicon_32 = create_favicon()
    favicon_32.save(static_images_dir / 'favicon-32x32.png', 'PNG')
    print("✅ favicon-32x32.png criado")
    
    # Criar favicon 16x16 (redimensionar)
    favicon_16 = favicon_32.resize((16, 16), Image.Resampling.LANCZOS)
    favicon_16.save(static_images_dir / 'favicon-16x16.png', 'PNG')
    print("✅ favicon-16x16.png criado")
    
    # Criar apple-touch-icon (180x180)
    apple_icon = favicon_32.resize((180, 180), Image.Resampling.LANCZOS)
    apple_icon.save(static_images_dir / 'apple-touch-icon.png', 'PNG')
    print("✅ apple-touch-icon.png criado")
    
    # Criar logo
    logo = create_logo()
    logo.save(static_images_dir / 'logo-regional-veiculos.png', 'PNG')
    print("✅ logo-regional-veiculos.png criado")
    
    # Criar imagem para social media
    social_img = Image.new('RGB', (1200, 630), color='#dc3545')
    draw = ImageDraw.Draw(social_img)
    
    text = "REGIONAL VEÍCULOS"
    subtitle = "Carros Seminovos e Novos"
    
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    if font:
        # Título principal
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1200 - text_width) // 2
        y = 250
        draw.text((x, y), text, fill='white', font=font)
        
        # Subtítulo
        bbox = draw.textbbox((0, 0), subtitle, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1200 - text_width) // 2
        y = 300
        draw.text((x, y), subtitle, fill='white', font=font)
    
    social_img.save(static_images_dir / 'regional-veiculos-twitter.jpg', 'JPEG', quality=95)
    social_img.save(static_images_dir / 'regional-veiculos-fachada.jpg', 'JPEG', quality=95)
    print("✅ Imagens para redes sociais criadas")
    
    print("\n🎉 Todas as imagens essenciais foram criadas!")

if __name__ == "__main__":
    create_essential_images()