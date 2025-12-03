#!/usr/bin/env python
"""
Script para criar imagens placeholder que estão faltando
"""
import os
import shutil

# Diretório de imagens
img_dir = "static/images"

# Lista de imagens que podem estar faltando baseado nos templates
missing_images = [
    "hero-car.jpg",
    "about-us.jpg", 
    "carro-padrao.jpg",
    "placeholder-car.jpg"
]

# Usar imgcar.jpg como base
base_image = os.path.join(img_dir, "imgcar.jpg")

if os.path.exists(base_image):
    print(f"📁 Usando como base: {base_image}")
    
    for img_name in missing_images:
        target_path = os.path.join(img_dir, img_name)
        
        if not os.path.exists(target_path):
            try:
                shutil.copy2(base_image, target_path)
                print(f"✅ Criada: {target_path}")
            except Exception as e:
                print(f"❌ Erro ao criar {target_path}: {e}")
        else:
            print(f"📋 Já existe: {target_path}")
            
else:
    print(f"❌ Imagem base não encontrada: {base_image}")

print("\n📊 Imagens no diretório:")
if os.path.exists(img_dir):
    for img in sorted(os.listdir(img_dir)):
        if img.lower().endswith(('.jpg', '.jpeg', '.png', '.svg')):
            print(f"  📸 {img}")