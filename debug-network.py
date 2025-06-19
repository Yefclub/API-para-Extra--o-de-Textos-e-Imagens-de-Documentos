#!/usr/bin/env python3
"""
Script para debug de conectividade de rede no container Docker
"""

import requests
import socket
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_dns_resolution(domain):
    """Testar resolução DNS"""
    try:
        logger.info(f"Testando resolução DNS para: {domain}")
        result = socket.gethostbyname(domain)
        logger.info(f"✅ DNS OK: {domain} -> {result}")
        return True, result
    except Exception as e:
        logger.error(f"❌ DNS FAIL: {domain} -> {str(e)}")
        return False, str(e)

def test_ping_domain(domain, port=80):
    """Testar conectividade TCP"""
    try:
        logger.info(f"Testando conectividade TCP para: {domain}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((domain, port))
        sock.close()
        
        if result == 0:
            logger.info(f"✅ TCP OK: {domain}:{port}")
            return True
        else:
            logger.error(f"❌ TCP FAIL: {domain}:{port} -> Erro: {result}")
            return False
    except Exception as e:
        logger.error(f"❌ TCP FAIL: {domain}:{port} -> {str(e)}")
        return False

def test_http_request(url):
    """Testar requisição HTTP"""
    try:
        logger.info(f"Testando requisição HTTP para: {url}")
        
        headers = {
            'User-Agent': 'Document-Extractor-Debug/1.0',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        # Tentar HEAD primeiro
        response = requests.head(url, headers=headers, timeout=30, allow_redirects=True)
        logger.info(f"✅ HTTP HEAD OK: {url} -> Status: {response.status_code}")
        
        # Tentar GET com range pequeno
        headers['Range'] = 'bytes=0-1023'  # Apenas 1KB para teste
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        logger.info(f"✅ HTTP GET OK: {url} -> Status: {response.status_code}, Size: {len(response.content)} bytes")
        
        return True, response.status_code
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"❌ HTTP CONNECTION FAIL: {url} -> {str(e)}")
        return False, f"Connection Error: {str(e)}"
    except requests.exceptions.Timeout as e:
        logger.error(f"❌ HTTP TIMEOUT: {url} -> {str(e)}")
        return False, f"Timeout: {str(e)}"
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP ERROR: {url} -> {str(e)}")
        return False, f"HTTP Error: {str(e)}"
    except Exception as e:
        logger.error(f"❌ HTTP FAIL: {url} -> {str(e)}")
        return False, f"General Error: {str(e)}"

def main():
    """Função principal de teste"""
    logger.info("🔍 Iniciando diagnóstico de rede...")
    
    # URLs e domínios para testar
    test_domains = [
        "google.com",
        "potential-ai.grpotencial.com.br",
        "grpotencial.com.br",
        "potencial.com.br"
    ]
    
    test_urls = [
        "https://google.com",
        "https://potential-ai.grpotencial.com.br",
        "https://potential-ai.grpotencial.com.br/uploads/documents/1750174688_68518be0c7dc07.46004534_9f2e5974-3b1f-4c16-998a-59ba5deea62b.pdf"
    ]
    
    print("\n" + "="*60)
    print("🧪 TESTE DE RESOLUÇÃO DNS")
    print("="*60)
    
    for domain in test_domains:
        test_dns_resolution(domain)
    
    print("\n" + "="*60)
    print("🔌 TESTE DE CONECTIVIDADE TCP")
    print("="*60)
    
    for domain in test_domains:
        test_ping_domain(domain, 80)
        test_ping_domain(domain, 443)
    
    print("\n" + "="*60)
    print("🌐 TESTE DE REQUISIÇÕES HTTP")
    print("="*60)
    
    for url in test_urls:
        test_http_request(url)
    
    # Informações do sistema
    print("\n" + "="*60)
    print("📋 INFORMAÇÕES DO SISTEMA")
    print("="*60)
    
    try:
        with open('/etc/resolv.conf', 'r') as f:
            logger.info(f"DNS Config: {f.read().strip()}")
    except:
        logger.error("Não foi possível ler /etc/resolv.conf")
    
    try:
        with open('/etc/hosts', 'r') as f:
            hosts_content = f.read().strip()
            logger.info(f"Hosts file: {hosts_content}")
    except:
        logger.error("Não foi possível ler /etc/hosts")

if __name__ == "__main__":
    main() 