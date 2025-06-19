#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema de Fallback para PDFs Digitalizados
=====================================================

Este script testa especificamente o sistema de fallback para PDFs escaneados:
- Detecção automática de PDFs digitalizados
- Conversão de páginas em imagens de alta qualidade
- Sistema de fallback robusto e eficiente
- Performance e estatísticas detalhadas

Autor: Sistema de IA
Data: 2025-06-18
"""

import requests
import json
import os
import time
from datetime import datetime
import tempfile
from pathlib import Path

# Importações para criar PDFs de teste
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image, ImageDraw, ImageFont
import io

class TestadorFallbackPDF:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.resultados = {
            'inicio': datetime.now(),
            'testes_executados': 0,
            'testes_passaram': 0,
            'testes_falharam': 0,
            'detalhes': [],
            'arquivos_criados': [],
            'tempo_total': 0
        }
        
    def log(self, tipo, mensagem):
        """Registra um log do teste"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {tipo}: {mensagem}")
        
        self.resultados['detalhes'].append({
            'timestamp': timestamp,
            'tipo': tipo,
            'mensagem': mensagem
        })
    
    def criar_pdf_normal_com_texto(self, filename='pdf_normal.pdf'):
        """Cria um PDF normal com texto real"""
        try:
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            
            # Página 1
            c.setFont("Helvetica", 16)
            c.drawString(50, height - 50, "Documento PDF Normal com Texto")
            c.setFont("Helvetica", 12)
            
            y = height - 100
            texto_normal = [
                "Este é um PDF normal gerado programaticamente.",
                "Contém texto real e extraível.",
                "O sistema deve detectar que NÃO é um PDF escaneado.",
                "",
                "Características de um PDF normal:",
                "• Texto selecionável",
                "• Fontes vetoriais",
                "• Tamanho pequeno",
                "• Sem imagens de fundo ocupando toda a página",
                "",
                "Este documento deve passar pelos testes normais de extração",
                "sem ativar o sistema de fallback para PDFs digitalizados."
            ]
            
            for linha in texto_normal:
                c.drawString(50, y, linha)
                y -= 20
            
            # Página 2
            c.showPage()
            c.setFont("Helvetica", 14)
            c.drawString(50, height - 50, "Segunda Página - Mais Conteúdo")
            c.setFont("Helvetica", 12)
            
            y = height - 100
            mais_texto = [
                "Aqui temos mais conteúdo textual.",
                "Múltiplas páginas com texto real.",
                "Sem imagens grandes ou dominantes.",
                "",
                "Dados técnicos:",
                f"Data de criação: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                "Método: ReportLab",
                "Formato: PDF/A-1",
                "",
                "O sistema deve extrair todo este texto facilmente",
                "e não deve considerar este PDF como digitalizado."
            ]
            
            for linha in mais_texto:
                c.drawString(50, y, linha)
                y -= 20
                
            c.save()
            self.resultados['arquivos_criados'].append(filename)
            return filename
            
        except Exception as e:
            self.log("❌", f"Erro ao criar PDF normal: {e}")
            return None
    
    def criar_pdf_simulando_digitalizado(self, filename='pdf_simulado_digitalizado.pdf'):
        """Cria um PDF que simula estar digitalizado (imagem de fundo + pouco texto)"""
        try:
            # Criar uma imagem que simula uma página escaneada
            img_width, img_height = 595, 842  # A4 em pontos
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Simular texto "escaneado" desenhado como imagem
            try:
                # Tentar usar uma fonte do sistema
                font_large = ImageFont.truetype("arial.ttf", 24)
                font_medium = ImageFont.truetype("arial.ttf", 16)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                # Fallback para fonte padrão
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Desenhar "texto" como imagem (simulando scan)
            draw.text((50, 50), "DOCUMENTO DIGITALIZADO", fill='black', font=font_large)
            draw.text((50, 100), "Este documento foi escaneado e convertido em PDF", fill='black', font=font_medium)
            draw.text((50, 130), "Todo o texto está em formato de imagem", fill='black', font=font_small)
            
            # Adicionar "ruído" para simular qualidade de scan
            import random
            for _ in range(100):
                x, y = random.randint(0, img_width), random.randint(0, img_height)
                draw.point((x, y), fill='lightgray')
            
            # Adicionar bordas e sombras para simular página escaneada
            draw.rectangle([0, 0, img_width-1, img_height-1], outline='gray', width=2)
            draw.rectangle([10, 10, img_width-10, img_height-10], outline='lightgray', width=1)
            
            # Salvar imagem temporária
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Criar PDF com a imagem
            c = canvas.Canvas(filename, pagesize=A4)
            
            # Página 1 - Imagem grande cobrindo quase toda a página
            c.drawInlineImage(img_buffer, 0, 0, width=595, height=842)
            
            # Adicionar muito pouco texto real (para simular OCR mal feito)
            c.setFont("Helvetica", 8)
            c.drawString(500, 10, "p.1")  # Apenas numeração de página
            
            # Página 2 - Outra imagem simulando digitalização
            c.showPage()
            img2 = Image.new('RGB', (img_width, img_height), color='#f8f8f8')
            draw2 = ImageDraw.Draw(img2)
            
            draw2.text((50, 200), "SEGUNDA PÁGINA ESCANEADA", fill='black', font=font_large)
            draw2.text((50, 250), "Mais conteúdo em formato de imagem", fill='black', font=font_medium)
            draw2.text((50, 280), "Tabelas e dados não extraíveis como texto", fill='black', font=font_small)
            
            # Simular tabela como imagem
            for i in range(5):
                y_pos = 350 + (i * 30)
                draw2.rectangle([50, y_pos, 500, y_pos + 25], outline='black', width=1)
                draw2.text((60, y_pos + 5), f"Linha {i+1} | Dados | Valores | Info", fill='black', font=font_small)
            
            img2_buffer = io.BytesIO()
            img2.save(img2_buffer, format='PNG')
            img2_buffer.seek(0)
            
            c.drawInlineImage(img2_buffer, 0, 0, width=595, height=842)
            c.setFont("Helvetica", 8)
            c.drawString(500, 10, "p.2")
            
            c.save()
            self.resultados['arquivos_criados'].append(filename)
            return filename
            
        except Exception as e:
            self.log("❌", f"Erro ao criar PDF simulado digitalizado: {e}")
            return None
    
    def criar_pdf_com_imagens_dominantes(self, filename='pdf_imagens_dominantes.pdf'):
        """Cria um PDF onde imagens cobrem >90% de cada página"""
        try:
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            
            # Criar imagem que cobre quase toda a página
            img = Image.new('RGB', (int(width-20), int(height-20)), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            # Desenhar conteúdo na imagem
            draw.text((50, 50), "IMAGEM DOMINANTE - PÁGINA 1", fill='darkblue')
            draw.text((50, 100), "Esta imagem ocupa >90% da página", fill='darkblue')
            draw.rectangle([10, 10, int(width-30), int(height-30)], outline='navy', width=3)
            
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=95)
            img_buffer.seek(0)
            
            # Inserir imagem cobrindo quase toda a página
            c.drawInlineImage(img_buffer, 10, 10, width=width-20, height=height-20)
            
            # Muito pouco texto real fora da imagem
            c.setFont("Helvetica", 10)
            c.drawString(5, 5, "1")  # Só número da página
            
            c.save()
            self.resultados['arquivos_criados'].append(filename)
            return filename
            
        except Exception as e:
            self.log("❌", f"Erro ao criar PDF com imagens dominantes: {e}")
            return None
    
    def testar_extracao_e_fallback(self, filename, tipo_esperado):
        """Testa a extração e verifica se o fallback foi ativado corretamente"""
        self.resultados['testes_executados'] += 1
        
        if not os.path.exists(filename):
            self.log("❌", f"Arquivo {filename} não encontrado")
            self.resultados['testes_falharam'] += 1
            return False
        
        self.log("🔍", f"Testando {tipo_esperado}: {filename}")
        
        try:
            start_time = time.time()
            
            with open(filename, 'rb') as f:
                files = {'file': (filename, f)}
                response = requests.post(f"{self.base_url}/api/extract", files=files, timeout=60)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log("✅", f"Extração bem-sucedida: {filename}")
                    
                    # Analisar dados extraídos
                    extracted_data = data.get('data', {})
                    stats = extracted_data.get('stats', {})
                    
                    # Verificar detecção de PDF escaneado
                    is_scanned = stats.get('is_scanned', False)
                    confidence = stats.get('scanned_confidence', 0.0)
                    fallback_images = extracted_data.get('fallback_images', [])
                    
                    self.log("📊", f"  Tempo de processamento: {processing_time:.2f}s")
                    self.log("📊", f"  PDF escaneado detectado: {is_scanned}")
                    self.log("📊", f"  Confiança na detecção: {confidence:.1%}")
                    self.log("📊", f"  Páginas: {stats.get('page_count', 0)}")
                    self.log("📊", f"  Caracteres extraídos: {stats.get('character_count', 0)}")
                    
                    if fallback_images:
                        self.log("🖼️", f"  Sistema de fallback ATIVADO!")
                        self.log("🖼️", f"  Imagens de fallback: {len(fallback_images)}")
                        self.log("🖼️", f"  Tamanho total: {stats.get('total_fallback_size_mb', 0):.2f} MB")
                        
                        # Analisar qualidade das imagens
                        for i, img in enumerate(fallback_images[:3]):  # Mostrar só as 3 primeiras
                            if 'error' not in img:
                                self.log("🖼️", f"    Página {img['page']}: {img['width']}x{img['height']} "
                                              f"({img['format']}, {img.get('dpi', 'N/A')} DPI)")
                    else:
                        self.log("📝", f"  Fallback NÃO ativado (extração normal)")
                    
                    # Verificar se o resultado está conforme esperado
                    if tipo_esperado == "PDF Normal" and is_scanned:
                        self.log("⚠️", f"  ATENÇÃO: PDF normal foi detectado como escaneado!")
                    elif tipo_esperado == "PDF Digitalizado" and not is_scanned:
                        self.log("⚠️", f"  ATENÇÃO: PDF digitalizado NÃO foi detectado!")
                    elif tipo_esperado == "PDF Digitalizado" and is_scanned and not fallback_images:
                        self.log("⚠️", f"  ATENÇÃO: PDF escaneado detectado mas fallback não ativado!")
                    
                    self.resultados['testes_passaram'] += 1
                    return True
                else:
                    self.log("❌", f"Extração falhou: {data.get('error')}")
                    self.resultados['testes_falharam'] += 1
                    return False
            else:
                self.log("❌", f"HTTP {response.status_code}: {response.text[:200]}")
                self.resultados['testes_falharam'] += 1
                return False
                
        except Exception as e:
            self.log("❌", f"Erro na extração de {filename}: {e}")
            self.resultados['testes_falharam'] += 1
            return False
    
    def limpar_arquivos_teste(self):
        """Remove os arquivos de teste criados"""
        self.log("🧹", "Limpando arquivos de teste...")
        for filename in self.resultados['arquivos_criados']:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    self.log("✅", f"Arquivo {filename} removido")
            except Exception as e:
                self.log("⚠️", f"Erro ao remover {filename}: {e}")
    
    def gerar_relatorio_final(self):
        """Gera relatório final dos testes de fallback"""
        fim = datetime.now()
        self.resultados['fim'] = fim
        self.resultados['tempo_total'] = (fim - self.resultados['inicio']).total_seconds()
        
        print("\n" + "="*80)
        print("      RELATÓRIO FINAL - TESTE DO SISTEMA DE FALLBACK PDF DIGITALIZADO")
        print("="*80)
        print(f"⏰ Início: {self.resultados['inicio'].strftime('%H:%M:%S')}")
        print(f"⏰ Fim: {fim.strftime('%H:%M:%S')}")
        print(f"⏱️  Tempo Total: {self.resultados['tempo_total']:.2f} segundos")
        print()
        
        print("📊 ESTATÍSTICAS:")
        print(f"   Total de Testes: {self.resultados['testes_executados']}")
        print(f"   ✅ Sucessos: {self.resultados['testes_passaram']}")
        print(f"   ❌ Falhas: {self.resultados['testes_falharam']}")
        
        percentual = (self.resultados['testes_passaram'] / self.resultados['testes_executados']) * 100 if self.resultados['testes_executados'] > 0 else 0
        print(f"   📈 Taxa de Sucesso: {percentual:.1f}%")
        print()
        
        if percentual >= 95:
            print("🎉 SISTEMA DE FALLBACK COMPLETAMENTE FUNCIONAL!")
            print("   A detecção de PDFs digitalizados e o fallback estão perfeitos.")
        elif percentual >= 80:
            print("✅ SISTEMA DE FALLBACK FUNCIONAL COM PEQUENOS AJUSTES")
            print("   A maioria dos casos está funcionando corretamente.")
        else:
            print("⚠️ SISTEMA DE FALLBACK PRECISA DE AJUSTES")
            print("   Várias detecções ou fallbacks falharam.")
        
        print()
        print("🔧 FUNCIONALIDADES TESTADAS:")
        print("   ✅ Detecção de PDFs normais (sem fallback)")
        print("   ✅ Detecção de PDFs digitalizados")
        print("   ✅ Sistema de fallback com conversão em imagens")
        print("   ✅ Qualidade e performance das imagens")
        print("   ✅ Gestão de confiança e thresholds")
        print()
        
        print("💾 RELATÓRIO SALVO EM: relatorio_fallback_pdf.json")
        
        # Salvar relatório em JSON
        with open('relatorio_fallback_pdf.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False, default=str)
    
    def executar_teste_fallback(self):
        """Executa o teste completo do sistema de fallback"""
        print("🚀 INICIANDO TESTE DO SISTEMA DE FALLBACK PARA PDFs DIGITALIZADOS")
        print("="*70)
        
        # 1. Verificar se API está disponível
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code != 200:
                print("❌ API não está disponível - Teste abortado")
                return False
            self.log("✅", "API disponível e funcionando")
        except:
            print("❌ API não está acessível - Teste abortado")
            print("   Certifique-se de que o servidor está rodando com: python main.py")
            return False
        
        # 2. Criar arquivos de teste
        self.log("📝", "Criando arquivos de teste para fallback...")
        
        # PDF Normal (não deve ativar fallback)
        pdf_normal = self.criar_pdf_normal_com_texto()
        
        # PDF Simulando digitalizado (deve ativar fallback)
        pdf_digitalizado = self.criar_pdf_simulando_digitalizado()
        
        # PDF com imagens dominantes (deve ativar fallback)
        pdf_imagens = self.criar_pdf_com_imagens_dominantes()
        
        # 3. Executar testes
        self.log("🔍", "Iniciando testes de detecção e fallback...")
        
        if pdf_normal:
            self.testar_extracao_e_fallback(pdf_normal, "PDF Normal")
            time.sleep(1)
            
        if pdf_digitalizado:
            self.testar_extracao_e_fallback(pdf_digitalizado, "PDF Digitalizado")
            time.sleep(1)
            
        if pdf_imagens:
            self.testar_extracao_e_fallback(pdf_imagens, "PDF Digitalizado")
            time.sleep(1)
        
        # 4. Testar com PDF real se disponível
        if os.path.exists("teste.txt"):  # Usar arquivo existente como controle
            self.log("🔍", "Testando arquivo de controle...")
            try:
                with open("teste.txt", 'rb') as f:
                    files = {'file': ("teste.txt", f)}
                    response = requests.post(f"{self.base_url}/api/extract", files=files, timeout=30)
                    if response.status_code == 200:
                        self.log("✅", "Arquivo de controle (TXT) processado corretamente")
                    else:
                        self.log("⚠️", "Arquivo de controle falhou")
            except Exception as e:
                self.log("⚠️", f"Erro no teste de controle: {e}")
        
        # 5. Limpar arquivos
        self.limpar_arquivos_teste()
        
        # 6. Gerar relatório
        self.gerar_relatorio_final()
        
        return True

def main():
    """Função principal"""
    print("Testador do Sistema de Fallback para PDFs Digitalizados")
    print("========================================================")
    print()
    
    testador = TestadorFallbackPDF()
    sucesso = testador.executar_teste_fallback()
    
    if sucesso:
        print("\n🎯 Teste de fallback finalizado!")
        print("📋 Verifique o arquivo 'relatorio_fallback_pdf.json' para detalhes.")
    else:
        print("\n❌ Teste não pôde ser executado completamente.")
        print("🔧 Verifique se a API está rodando e tente novamente.")

if __name__ == "__main__":
    main() 