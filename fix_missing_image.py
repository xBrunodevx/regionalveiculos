# Criando placeholder para imagemcarr.jpg (cópia do imgcar.jpg)
import shutil
import os

source = "static/images/imgcar.jpg"
target = "static/images/imagemcarr.jpg"

if os.path.exists(source):
    shutil.copy2(source, target)
    print(f"✅ Criada: {target}")
else:
    print(f"❌ Arquivo fonte não encontrado: {source}")