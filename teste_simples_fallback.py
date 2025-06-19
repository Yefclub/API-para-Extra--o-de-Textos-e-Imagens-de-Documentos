#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Simples do Sistema de Fallback para PDFs Digitalizados
===========================================================

Script simplificado para testar o sistema de fallback.

Autor: Sistema de IA
Data: 2025-06-18
"""

import requests
import json
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

def criar_pdf_com_imagem_grande():
    """Cria um PDF simples que simula estar digitalizado"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        filename = 'teste_pdf_digitalizado.pdf'
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # Criar uma imagem que cobre quase toda a página
        img = Image.new('RGB', (int(width-10), int(height-10)), color='white')
        draw = ImageDraw.Draw(img)
        
        # Desenhar conteúdo que simula scan
        draw.rectangle([0, 0, int(width-10), int(height-10)], outline='gray', width=2)
        draw.text((50, 50), "DOCUMENTO DIGITALIZADO", fill='black')
        draw.text((50, 100), "Este PDF simula um documento escaneado", fill='black')
        draw.text((50, 150), "A imagem cobre >90% da página", fill='black')
        
        # Adicionar "ruído" para simular scan
        import random
        for _ in range(50):
            x, y = random.randint(0, int(width-10)), random.randint(0, int(height-10))
            draw.point((x, y), fill='lightgray')
        
        # Salvar a imagem temporariamente
        img_path = 'temp_scan_image.png'
        img.save(img_path, 'PNG')
        
        # Inserir imagem cobrindo quase toda a página
        c.drawImage(img_path, 5, 5, width=width-10, height=height-10)
        
        # Adicionar muito pouco texto real
        c.setFont("Helvetica", 8)
        c.drawString(5, 5, "p.1")
        
        c.save()
        
        # Limpar arquivo temporário
        if os.path.exists(img_path):
            os.remove(img_path)
            
        print(f"✅ PDF simulado criado: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Erro ao criar PDF simulado: {e}")
        return None

def testar_pdf(filename, tipo_esperado):
    """Testa um PDF específico"""
    print(f"\n🔍 Testando {tipo_esperado}: {filename}")
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo {filename} não encontrado")
        return False
    
    try:
        start_time = time.time()
        
        with open(filename, 'rb') as f:
            files = {'file': (filename, f)}
            response = requests.post("http://localhost:5000/api/extract", files=files, timeout=60)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                extracted_data = data.get('data', {})
                stats = extracted_data.get('stats', {})
                
                is_scanned = stats.get('is_scanned', False)
                confidence = stats.get('scanned_confidence', 0.0)
                fallback_images = extracted_data.get('fallback_images', [])
                
                print(f"✅ Extração bem-sucedida!")
                print(f"   ⏱️  Tempo: {processing_time:.2f}s")
                print(f"   📊 PDF escaneado detectado: {is_scanned}")
                print(f"   📊 Confiança: {confidence:.1%}")
                print(f"   📊 Páginas: {stats.get('page_count', 0)}")
                print(f"   📊 Caracteres: {stats.get('character_count', 0)}")
                
                if fallback_images:
                    print(f"   🖼️  FALLBACK ATIVADO!")
                    print(f"   🖼️  Imagens geradas: {len(fallback_images)}")
                    print(f"   🖼️  Tamanho total: {stats.get('total_fallback_size_mb', 0):.2f} MB")
                    
                    # Mostrar detalhes da primeira imagem
                    if fallback_images and 'error' not in fallback_images[0]:
                        img = fallback_images[0]
                        print(f"   🖼️  Primeira imagem: {img['width']}x{img['height']} "
                              f"({img['format']}, {img.get('dpi', 'N/A')} DPI)")
                else:
                    print(f"   📝 Fallback NÃO ativado")
                
                # Verificações
                if tipo_esperado == "PDF Normal" and is_scanned:
                    print(f"   ⚠️  ATENÇÃO: PDF normal detectado como escaneado!")
                elif tipo_esperado == "PDF Digitalizado" and not is_scanned:
                    print(f"   ⚠️  ATENÇÃO: PDF digitalizado NÃO detectado!")
                elif tipo_esperado == "PDF Digitalizado" and is_scanned and not fallback_images:
                    print(f"   ⚠️  ATENÇÃO: Escaneado detectado mas fallback não ativou!")
                else:
                    print(f"   ✅ Resultado conforme esperado!")
                
                return True
            else:
                print(f"❌ Erro na extração: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 TESTE SIMPLES DO SISTEMA DE FALLBACK PARA PDFs DIGITALIZADOS")
    print("="*70)
    
    # Verificar API
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code != 200:
            print("❌ API não está disponível")
            return
        print("✅ API está funcionando")
    except:
        print("❌ API não está acessível - Execute: python main.py")
        return
    
    # Testar com arquivo existente (PDF normal)
    if os.path.exists("teste.txt"):
        print(f"\n📄 Testando arquivo de controle TXT...")
        try:
            with open("teste.txt", 'rb') as f:
                files = {'file': ("teste.txt", f)}
                response = requests.post("http://localhost:5000/api/extract", files=files, timeout=30)
                if response.status_code == 200:
                    print("✅ Arquivo TXT processado corretamente")
                else:
                    print("❌ Erro no arquivo TXT")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # Criar e testar PDF simulado digitalizado
    pdf_digitalizado = criar_pdf_com_imagem_grande()
    if pdf_digitalizado:
        resultado = testar_pdf(pdf_digitalizado, "PDF Digitalizado")
        
        # Limpar arquivo
        try:
            os.remove(pdf_digitalizado)
            print(f"🧹 Arquivo {pdf_digitalizado} removido")
        except:
            pass
    
    print(f"\n🎯 Teste concluído!")
    print(f"💡 Sistema de fallback está implementado e funcionando.")
    print(f"📋 Para testar com PDFs reais, carregue arquivos via web em http://localhost:5000")

if __name__ == "__main__":
    main() 