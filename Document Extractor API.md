# Document Extractor API

Uma API robusta para extração de texto e imagens de diversos tipos de documentos, incluindo PDF, Word, Excel e arquivos de texto simples.

## 🚀 Características

- **Múltiplos formatos suportados**: PDF, DOCX, DOC, XLSX, XLS, TXT
- **Extração de texto**: Texto completo de todos os formatos suportados
- **Extração de imagens**: Imagens de documentos PDF em alta qualidade
- **Dados estruturados**: Processamento de tabelas e planilhas
- **Interface web**: Interface moderna para testes e demonstrações
- **Documentação completa**: API totalmente documentada com exemplos
- **CORS habilitado**: Pronto para integração com aplicações frontend

## 📋 Tipos de Arquivo Suportados

| Formato | Extensão | Recursos |
|---------|----------|----------|
| PDF | `.pdf` | Texto, Imagens |
| Word Document | `.docx` | Texto, Tabelas |
| Word Document (Legacy) | `.doc` | Texto |
| Excel Spreadsheet | `.xlsx` | Dados estruturados |
| Excel Spreadsheet (Legacy) | `.xls` | Dados estruturados |
| Texto Simples | `.txt` | Texto |

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone <url-do-repositorio>
   cd document-extractor-api
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv venv
   
   # No Linux/Mac
   source venv/bin/activate
   
   # No Windows
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse a aplicação**
   - Interface de testes: http://localhost:5000
   - Documentação da API: http://localhost:5000/docs
   - Health check: http://localhost:5000/api/health

## 🔧 Uso da API

### Endpoints Principais

#### 1. Verificação de Saúde
```http
GET /api/health
```

#### 2. Tipos Suportados
```http
GET /api/supported-types
```

#### 3. Extração de Documentos
```http
POST /api/extract
Content-Type: multipart/form-data

file: [arquivo a ser processado]
```

### Exemplos de Uso

#### cURL
```bash
# Extrair dados de um documento
curl -X POST http://localhost:5000/api/extract \
  -F "file=@documento.pdf"
```

#### Python
```python
import requests

# Extrair dados de um documento
with open('documento.pdf', 'rb') as file:
    files = {'file': file}
    response = requests.post('http://localhost:5000/api/extract', files=files)
    result = response.json()
    
    if result['success']:
        print("Texto extraído:", result['data']['text'])
    else:
        print("Erro:", result['error'])
```

#### JavaScript
```javascript
// Extrair dados de um arquivo
async function extractDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/extract', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  return result;
}
```

## 📊 Estrutura de Resposta

### Resposta de Sucesso
```json
{
  "success": true,
  "data": {
    "text": "Texto extraído do documento...",
    "file_info": {
      "filename": "documento.pdf",
      "type": "pdf",
      "mime_type": "application/pdf"
    },
    "pages": 5,
    "total_images": 3,
    "images": [
      {
        "page": 1,
        "index": 1,
        "format": "png",
        "data": "base64_encoded_image_data",
        "width": 800,
        "height": 600
      }
    ]
  }
}
```

### Resposta de Erro
```json
{
  "success": false,
  "error": "Descrição do erro"
}
```

## 🏗️ Estrutura do Projeto

```
document-extractor-api/
├── src/
│   ├── routes/
│   │   ├── extractor.py      # Endpoints da API de extração
│   │   └── user.py           # Endpoints de usuário (exemplo)
│   ├── models/
│   │   └── user.py           # Modelos de dados
│   ├── static/
│   │   ├── index.html        # Interface de testes
│   │   └── docs.html         # Documentação da API
│   ├── database/
│   │   └── app.db           # Banco de dados SQLite
│   └── main.py              # Arquivo principal da aplicação
├── venv/                    # Ambiente virtual Python
├── requirements.txt         # Dependências do projeto
├── README.md               # Este arquivo
└── todo.md                 # Lista de tarefas do projeto
```

## 🔒 Configurações de Segurança

### Limites de Upload
- Tamanho máximo de arquivo: 50MB
- Tipos de arquivo permitidos: PDF, DOCX, DOC, XLSX, XLS, TXT

### Recomendações para Produção
- Implementar autenticação (API Key ou OAuth2)
- Configurar rate limiting
- Usar HTTPS
- Implementar logging detalhado
- Configurar monitoramento

## 🚀 Deploy

### Deploy Local
A aplicação já está configurada para rodar localmente na porta 5000.

### Deploy em Produção
Para deploy em produção, considere:

1. **Usar um servidor WSGI** (como Gunicorn)
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. **Configurar um proxy reverso** (Nginx)
3. **Usar variáveis de ambiente** para configurações sensíveis
4. **Implementar SSL/TLS**

## 🧪 Testes

### Teste Manual
1. Acesse http://localhost:5000
2. Faça upload de um arquivo de teste
3. Verifique os resultados na interface

### Teste via API
```bash
# Teste básico
curl -X GET http://localhost:5000/api/health

# Teste com arquivo
curl -X POST http://localhost:5000/api/extract \
  -F "file=@teste.txt"
```

## 📚 Documentação

- **Interface de testes**: http://localhost:5000
- **Documentação completa**: http://localhost:5000/docs
- **Endpoints da API**: Veja a documentação completa para detalhes

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a documentação em http://localhost:5000/docs
2. Teste os endpoints básicos (health check)
3. Verifique os logs da aplicação
4. Abra uma issue no repositório

## 🔄 Changelog

### v1.0.0
- Implementação inicial da API
- Suporte para PDF, Word, Excel e TXT
- Interface web para testes
- Documentação completa
- Extração de imagens de PDFs
- Processamento de tabelas em documentos Word

