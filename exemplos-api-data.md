# 📄 API de Análise por Dados - Exemplos de Uso

Esta documentação mostra como usar as novas rotas para análise de documentos através de dados (base64 ou binários) em vez de upload de arquivos.

## 🔗 Novas Rotas Disponíveis

### 1. `/api/extract/data` - Análise Individual
Processa um único documento a partir de dados.

### 2. `/api/extract/data/bulk` - Análise em Lote  
Processa múltiplos documentos de uma vez.

## 📋 Formato dos Dados

### Campos Obrigatórios:
- `filename`: Nome do arquivo com extensão
- `file_data`: Dados do arquivo (base64 ou binários)

### Campos Opcionais:
- `encoding`: "base64" (padrão) ou "binary"

## 💡 Exemplos Práticos

### 1. Análise de Arquivo de Texto (Base64)

```bash
curl -X POST http://localhost:5000/api/extract/data \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "documento.txt",
    "file_data": "RXN0ZSBkb2N1bWVudG8gY29udMOpbSB0ZXh0byBwYXJhIGFuw6FsaXNl",
    "encoding": "base64"
  }'
```

### 2. Análise de PDF (Base64)

```bash
curl -X POST http://localhost:5000/api/extract/data \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "relatorio.pdf",
    "file_data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCg==",
    "encoding": "base64"
  }'
```

### 3. Análise em Lote (Múltiplos Documentos)

```bash
curl -X POST http://localhost:5000/api/extract/data/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "filename": "doc1.txt",
        "file_data": "VGV4dG8gZG8gcHJpbWVpcm8gZG9jdW1lbnRv",
        "encoding": "base64"
      },
      {
        "filename": "doc2.txt", 
        "file_data": "VGV4dG8gZG8gc2VndW5kbyBkb2N1bWVudG8=",
        "encoding": "base64"
      }
    ]
  }'
```

## 🐍 Exemplos em Python

### Análise Individual

```python
import requests
import base64

# Ler arquivo e converter para base64
with open("documento.pdf", "rb") as file:
    file_content = file.read()
    file_base64 = base64.b64encode(file_content).decode('utf-8')

# Fazer requisição
response = requests.post('http://localhost:5000/api/extract/data', json={
    "filename": "documento.pdf",
    "file_data": file_base64,
    "encoding": "base64"
})

result = response.json()
if result['success']:
    print("Texto extraído:", result['data']['text'])
else:
    print("Erro:", result['error'])
```

### Análise em Lote

```python
import requests
import base64
import os

def process_files_in_directory(directory_path):
    documents = []
    
    # Processar todos os arquivos do diretório
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                file_content = file.read()
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                
                documents.append({
                    "filename": filename,
                    "file_data": file_base64,
                    "encoding": "base64"
                })
    
    # Enviar para análise em lote
    response = requests.post('http://localhost:5000/api/extract/data/bulk', json={
        "documents": documents
    })
    
    return response.json()

# Usar a função
result = process_files_in_directory("./documentos")
print(f"Processados: {result['data']['statistics']['successful']}/{result['data']['statistics']['total_documents']}")
```

## 🌐 Exemplos em JavaScript

### Análise Individual (Node.js)

```javascript
const fs = require('fs');
const fetch = require('node-fetch');

async function analyzeDocument(filePath) {
    // Ler arquivo e converter para base64
    const fileBuffer = fs.readFileSync(filePath);
    const fileBase64 = fileBuffer.toString('base64');
    const filename = path.basename(filePath);
    
    const response = await fetch('http://localhost:5000/api/extract/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filename: filename,
            file_data: fileBase64,
            encoding: 'base64'
        })
    });
    
    const result = await response.json();
    return result;
}

// Usar
analyzeDocument('./documento.pdf')
    .then(result => {
        if (result.success) {
            console.log('Texto:', result.data.text);
        } else {
            console.error('Erro:', result.error);
        }
    });
```

### Análise no Frontend (JavaScript)

```javascript
// Análise de arquivo selecionado pelo usuário
async function analyzeSelectedFile(fileInput) {
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Selecione um arquivo');
        return;
    }
    
    // Converter arquivo para base64
    const reader = new FileReader();
    reader.onload = async function(e) {
        const fileBase64 = e.target.result.split(',')[1]; // Remove prefixo data:
        
        try {
            const response = await fetch('/api/extract/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: file.name,
                    file_data: fileBase64,
                    encoding: 'base64'
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                document.getElementById('result').textContent = result.data.text;
            } else {
                alert('Erro: ' + result.error);
            }
        } catch (error) {
            alert('Erro na requisição: ' + error.message);
        }
    };
    
    reader.readAsDataURL(file);
}
```

## 📊 Formato de Resposta

### Sucesso (Individual)
```json
{
  "success": true,
  "data": {
    "text": "Texto extraído do documento...",
    "file_info": {
      "filename": "documento.pdf",
      "type": "pdf",
      "mime_type": "application/pdf",
      "size_bytes": 1024,
      "size_mb": 0.001,
      "encoding_used": "base64"
    }
  },
  "message": "Documento processado com sucesso a partir de dados"
}
```

### Sucesso (Lote)
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "index": 0,
        "success": true,
        "data": {
          "text": "Texto do primeiro documento...",
          "file_info": { ... }
        }
      }
    ],
    "errors": [],
    "statistics": {
      "total_documents": 2,
      "successful": 2,
      "failed": 0,
      "success_rate": 100.0,
      "total_processing_time_seconds": 1.234
    }
  },
  "message": "Processamento concluído: 2/2 documentos processados com sucesso"
}
```

## 🔧 Vantagens da Análise por Dados

### ✅ **Benefícios:**
1. **Integração Direta**: Não precisa salvar arquivos temporários
2. **APIs Externas**: Fácil integração com outros sistemas
3. **Processamento em Lote**: Múltiplos documentos de uma vez
4. **Flexibilidade**: Suporte a base64 e dados binários
5. **Estatísticas**: Relatórios detalhados de processamento

### 🎯 **Casos de Uso:**
- Integração com sistemas legados
- Processamento automático de documentos
- APIs de terceiros que fornecem dados em base64
- Aplicações web que precisam analisar arquivos sem upload
- Processamento em lote de documentos armazenados em banco de dados

## 🚨 Limitações

- **Tamanho máximo**: Mesmo limite dos uploads (50MB)
- **Tipos suportados**: Mesmos formatos da API de upload
- **Lote**: Máximo 10 documentos por requisição
- **Encoding**: Apenas base64 e binary suportados 