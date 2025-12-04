#!/usr/bin/env python
"""
Script para verificar imagens no banco de dados
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')

django.setup()

from core.models import ImagemSite, Carro, Marca

def check_images():
    """Verificar todas as imagens no sistema"""
    
    print("🔍 DIAGNÓSTICO COMPLETO DO SISTEMA DE IMAGENS\n")
    
    # 1. ImagemSite
    print("1️⃣ IMAGENS DO SITE (ImagemSite):")
    imagens_site = ImagemSite.objects.all()
    if imagens_site:
        for img in imagens_site:
            status = "✅ OK" if img.imagem and img.imagem.url else "❌ SEM ARQUIVO"
            url = img.imagem.url if img.imagem else "N/A"
            print(f"   ID {img.id}: {img.nome} ({img.tipo}) - {status}")
            print(f"      URL: {url}")
            print(f"      Ativo: {'Sim' if img.ativo else 'Não'}")
            
            # Verificar se arquivo existe fisicamente
            if img.imagem:
                file_path = Path(current_dir) / 'media' / str(img.imagem)
                exists = "✅ Existe" if file_path.exists() else "❌ Não existe"
                print(f"      Arquivo: {exists} ({file_path})")
            print()
    else:
        print("   ❌ Nenhuma imagem encontrada!")
    
    # 2. Carros
    print("\n2️⃣ IMAGENS DE CARROS:")
    carros = Carro.objects.all()[:5]  # Primeiros 5 para não sobrecarregar
    if carros:
        for carro in carros:
            print(f"   🚗 {carro.fabricante} {carro.modelo} (ID: {carro.id})")
            
            # Imagem principal
            if carro.imagem_principal:
                file_path = Path(current_dir) / 'media' / str(carro.imagem_principal)
                exists = "✅" if file_path.exists() else "❌"
                print(f"      Principal: {exists} {carro.imagem_principal.url}")
            else:
                print("      Principal: ❌ SEM IMAGEM")
            
            # Outras imagens
            for i, img_field in enumerate(['imagem_2', 'imagem_3', 'imagem_4'], 2):
                img = getattr(carro, img_field)
                if img:
                    file_path = Path(current_dir) / 'media' / str(img)
                    exists = "✅" if file_path.exists() else "❌"
                    print(f"      Imagem {i}: {exists} {img.url}")
            print()
    else:
        print("   ❌ Nenhum carro encontrado!")
    
    # 3. Marcas
    print("\n3️⃣ LOGOS DE MARCAS:")
    marcas = Marca.objects.all()
    if marcas:
        for marca in marcas:
            if marca.logo:
                file_path = Path(current_dir) / 'media' / str(marca.logo)
                exists = "✅" if file_path.exists() else "❌"
                print(f"   {exists} {marca.nome}: {marca.logo.url}")
            else:
                print(f"   ❌ {marca.nome}: SEM LOGO")
    else:
        print("   ❌ Nenhuma marca encontrada!")
    
    # 4. Verificar configurações
    print("\n4️⃣ CONFIGURAÇÕES:")
    print(f"   MEDIA_URL: /media/")
    print(f"   MEDIA_ROOT: {current_dir}/media")
    
    media_dir = current_dir / 'media'
    print(f"   Diretório media existe: {'✅ Sim' if media_dir.exists() else '❌ Não'}")
    
    if media_dir.exists():
        subdirs = [d.name for d in media_dir.iterdir() if d.is_dir()]
        print(f"   Subdiretórios: {', '.join(subdirs) if subdirs else 'Nenhum'}")
    
    print("\n🎯 PROBLEMAS IDENTIFICADOS:")
    problemas = []
    
    # Verificar imagens sem arquivo
    for img in imagens_site:
        if img.imagem:
            file_path = Path(current_dir) / 'media' / str(img.imagem)
            if not file_path.exists():
                problemas.append(f"ImagemSite ID {img.id} referencia arquivo inexistente: {img.imagem}")
    
    for carro in carros:
        if carro.imagem_principal:
            file_path = Path(current_dir) / 'media' / str(carro.imagem_principal)
            if not file_path.exists():
                problemas.append(f"Carro ID {carro.id} imagem principal inexistente: {carro.imagem_principal}")
    
    if problemas:
        for problema in problemas:
            print(f"   ❌ {problema}")
    else:
        print("   ✅ Nenhum problema crítico encontrado!")

if __name__ == "__main__":
    check_images()