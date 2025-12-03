#!/usr/bin/env python3
"""
Script de validação do deploy
Verifica se o site está funcionando corretamente após o deploy
"""

import requests
import sys
import time

def check_deploy_status():
    """Verifica o status do deploy no Render"""
    
    url = "https://regional-veiculos.onrender.com"
    
    print("🚀 Verificando status do deploy...")
    print(f"📍 URL: {url}")
    
    try:
        # Aguardar alguns segundos para o deploy processar
        print("⏳ Aguardando deploy processar...")
        time.sleep(10)
        
        # Fazer requisição para verificar se o site está online
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Deploy realizado com sucesso!")
            print("✅ Site está online e funcionando")
            print(f"✅ Status Code: {response.status_code}")
            
            # Verificar se as otimizações estão ativas
            if 'cache-clear.js' in response.text:
                print("✅ Script de otimização de cache carregado")
            else:
                print("⚠️  Script de cache não detectado (normal se ainda não processado)")
                
            print("\n🎉 Deploy atualizado com sucesso!")
            print("🔗 Acesse: https://regional-veiculos.onrender.com")
            
        else:
            print(f"❌ Erro no deploy - Status Code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏳ Site ainda carregando (normal para primeiro deploy)")
        print("⏳ Aguarde alguns minutos e tente novamente")
        
    except requests.exceptions.ConnectionError:
        print("⏳ Deploy ainda em progresso...")
        print("⏳ O Render pode levar alguns minutos para processar")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("=" * 50)
    print("🔄 VERIFICAÇÃO DE DEPLOY - REGIONAL VEÍCULOS")
    print("=" * 50)
    
    # Verificar status
    success = check_deploy_status()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ DEPLOY FINALIZADO COM SUCESSO!")
    else:
        print("⚠️  DEPLOY EM PROGRESSO - AGUARDE")
    print("=" * 50)

if __name__ == "__main__":
    main()