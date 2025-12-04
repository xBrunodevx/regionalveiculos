#!/usr/bin/env python
"""
Script para garantir que sempre há imagens básicas no Django
"""
import os
import sys
import django
from pathlib import Path
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont

# Configurar Django
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')

django.setup()

from core.models import ImagemSite

def create_default_image(text, width=400, height=300, color='#007bff'):
    """Criar uma imagem padrão com texto"""
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Tentar usar uma fonte melhor
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calcular posição do texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Desenhar texto
    draw.text((x, y), text, fill='white', font=font)
    
    return img

def ensure_default_images():
    """Garantir que existem imagens padrão para o site"""
    
    print("🖼️ GARANTINDO IMAGENS PADRÃO DO DJANGO\n")
    
    # Definir imagens necessárias
    default_images = {
        'carro_flutuante': {
            'nome': 'Carro Flutuante Padrão',
            'descricao': 'Imagem padrão para o carro flutuante da home',
            'text': 'CARRO\nEM DESTAQUE',
            'color': '#dc3545'  # vermelho
        },
        'sobre_loja': {
            'nome': 'Fachada da Loja Padrão',
            'descricao': 'Imagem padrão da fachada para página sobre',
            'text': 'REGIONAL\nVEÍCULOS',
            'color': '#28a745'  # verde
        },
        'banner_home': {
            'nome': 'Banner Principal Padrão',
            'descricao': 'Banner padrão para página inicial',
            'text': 'BANNER\nPRINCIPAL',
            'color': '#6f42c1'  # roxo
        }
    }
    
    media_dir = current_dir / 'media' / 'site_images'
    media_dir.mkdir(parents=True, exist_ok=True)
    
    for tipo, config in default_images.items():
        # Verificar se já existe uma imagem ativa deste tipo
        existing = ImagemSite.objects.filter(tipo=tipo, ativo=True).first()
        
        if existing and existing.imagem:
            # Verificar se o arquivo existe fisicamente
            file_path = current_dir / 'media' / str(existing.imagem)
            if file_path.exists():
                print(f"✅ {tipo}: Já existe e está OK")
                continue
        
        print(f"🔄 {tipo}: Criando imagem padrão...")
        
        # Criar imagem
        img = create_default_image(
            config['text'], 
            width=400, 
            height=300, 
            color=config['color']
        )
        
        # Salvar arquivo
        filename = f"{tipo}_padrao.jpg"
        temp_path = media_dir / filename
        img.save(temp_path, 'JPEG', quality=95)
        
        # Criar ou atualizar objeto no banco
        if existing:
            # Atualizar existente
            with open(temp_path, 'rb') as f:
                django_file = File(f, name=filename)
                existing.imagem.save(filename, django_file, save=True)
            print(f"   ✅ Atualizado: {existing.nome}")
        else:
            # Criar novo
            with open(temp_path, 'rb') as f:
                django_file = File(f, name=filename)
                
                new_image = ImagemSite.objects.create(
                    nome=config['nome'],
                    tipo=tipo,
                    descricao=config['descricao'],
                    ativo=True,
                    ordem=1
                )
                new_image.imagem.save(filename, django_file, save=True)
            print(f"   ✅ Criado: {config['nome']}")
        
        # Remover arquivo temporário
        if temp_path.exists():
            temp_path.unlink()
    
    print("\n🎯 RESUMO:")
    for img in ImagemSite.objects.filter(ativo=True).order_by('tipo'):
        file_path = current_dir / 'media' / str(img.imagem) if img.imagem else None
        status = "✅ OK" if file_path and file_path.exists() else "❌ ERRO"
        print(f"   {status} {img.nome} ({img.tipo}): {img.imagem.url if img.imagem else 'SEM ARQUIVO'}")

if __name__ == "__main__":
    ensure_default_images()