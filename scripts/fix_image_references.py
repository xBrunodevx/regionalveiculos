#!/usr/bin/env python
"""
Script para corrigir as imagens do ImagemSite com arquivos corretos
"""
import os
import sys
import django
from pathlib import Path
from django.core.files import File

# Configurar Django
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')

django.setup()

from core.models import ImagemSite

def fix_image_references():
    """Corrigir referências de imagens no banco"""
    
    print("🔧 CORRIGINDO REFERÊNCIAS DE IMAGENS\n")
    
    site_images_dir = current_dir / 'media' / 'site_images'
    
    # Mapear imagens disponíveis no diretório
    available_images = {}
    for img_file in site_images_dir.iterdir():
        if img_file.is_file():
            name = img_file.stem.lower()
            if 'carro_flutuante' in name or 'imgcar' in name:
                available_images['carro_flutuante'] = img_file
            elif 'fachada' in name or 'loja' in name or 'regional' in name:
                available_images['sobre_loja'] = img_file
            elif 'banner' in name or 'hero' in name:
                available_images['banner_home'] = img_file
    
    print("📁 Imagens disponíveis no diretório:")
    for tipo, arquivo in available_images.items():
        print(f"   {tipo}: {arquivo.name}")
    
    # Corrigir cada ImagemSite
    print("\n🔄 Atualizando referências no banco:")
    
    for imagem_obj in ImagemSite.objects.all():
        tipo = imagem_obj.tipo
        print(f"\n📸 Processando: {imagem_obj.nome} ({tipo})")
        
        # Verificar se arquivo atual existe
        if imagem_obj.imagem:
            current_file = current_dir / 'media' / str(imagem_obj.imagem)
            if current_file.exists():
                print(f"   ✅ Arquivo atual existe: {imagem_obj.imagem}")
                continue
        
        # Procurar arquivo adequado
        if tipo in available_images:
            new_file = available_images[tipo]
            print(f"   🔄 Atualizando para: {new_file.name}")
            
            try:
                # Abrir e salvar o arquivo
                with open(new_file, 'rb') as f:
                    django_file = File(f, name=new_file.name)
                    imagem_obj.imagem.save(new_file.name, django_file, save=True)
                
                print(f"   ✅ Atualizado com sucesso!")
                print(f"   📎 Nova URL: {imagem_obj.imagem.url}")
                
            except Exception as e:
                print(f"   ❌ Erro ao atualizar: {e}")
        else:
            print(f"   ⚠️  Nenhum arquivo adequado encontrado para tipo '{tipo}'")
    
    print("\n✅ Processo de correção concluído!")
    
    # Verificar resultado
    print("\n🔍 Verificação final:")
    for img in ImagemSite.objects.all():
        if img.imagem:
            file_path = current_dir / 'media' / str(img.imagem)
            status = "✅ OK" if file_path.exists() else "❌ ERRO"
            print(f"   {status} {img.nome}: {img.imagem.url}")
        else:
            print(f"   ❌ SEM ARQUIVO {img.nome}")

if __name__ == "__main__":
    fix_image_references()