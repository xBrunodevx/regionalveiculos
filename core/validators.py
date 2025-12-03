"""
Validadores personalizados para upload de imagens
"""
import os
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_file(file):
    """
    Valida se o arquivo é uma imagem válida
    """
    # Extensões permitidas
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff']
    
    # Obter extensão do arquivo
    ext = os.path.splitext(file.name)[1].lower()
    
    if not ext in valid_extensions:
        raise ValidationError(
            f'Formato de arquivo não suportado. Formatos permitidos: {", ".join(valid_extensions)}'
        )
    
    # Verificar se é uma imagem válida (exceto SVG)
    if ext != '.svg':
        try:
            # Tentar abrir como imagem
            img = Image.open(file)
            img.verify()
        except Exception:
            raise ValidationError('Arquivo de imagem corrompido ou inválido')
    
    # Verificar tamanho do arquivo (máximo 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValidationError('Arquivo muito grande. Tamanho máximo: 10MB')
    
    return file

def validate_image_dimensions(file):
    """
    Valida as dimensões da imagem
    """
    try:
        img = Image.open(file)
        width, height = img.size
        
        # Dimensões mínimas
        if width < 100 or height < 100:
            raise ValidationError('Imagem muito pequena. Dimensões mínimas: 100x100 pixels')
            
        # Dimensões máximas  
        if width > 4000 or height > 4000:
            raise ValidationError('Imagem muito grande. Dimensões máximas: 4000x4000 pixels')
            
    except Exception as e:
        if 'Imagem muito' in str(e):
            raise e
        # Se não conseguir ler, deixa passar (pode ser SVG)
        pass
    
    return file