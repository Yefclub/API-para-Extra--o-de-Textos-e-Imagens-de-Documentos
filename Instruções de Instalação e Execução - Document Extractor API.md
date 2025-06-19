# Instruções de Instalação e Execução - Document Extractor API

## 📦 Instalação Rápida

### 1. Preparar o Ambiente

```bash
# Navegue até o diretório do projeto
cd document-extractor-api

# Crie um ambiente virtual Python
python -m venv venv

# Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate
```

### 2. Instalar Dependências

```bash
# Instale todas as dependências necessárias
pip install -r requirements.txt
```

### 3. Executar a Aplicação

```bash
# Execute o servidor Flask
python src/main.py
```

### 4. Acessar a Aplicação

Após executar o comando acima, você verá uma mensagem similar a:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://169.254.0.21:5000
```

Acesse os seguintes URLs:

- **Interface de Testes**: http://localhost:5000
- **Documentação da API**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/api/health

## 🔧 Verificação da Instalação

### Teste 1: Health Check
```bash
curl -X GET http://localhost:5000/api/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "service": "Document Extractor API",
  "version": "1.0.0"
}
```

### Teste 2: Tipos Suportados
```bash
curl -X GET http://localhost:5000/api/supported-types
```

### Teste 3: Upload de Arquivo
```bash
# Crie um arquivo de teste
echo "Teste da API" > teste.txt

# Teste a extração
curl -X POST http://localhost:5000/api/extract -F "file=@teste.txt"
```

## 🚨 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Port already in use"
```bash
# Verifique se há outro processo usando a porta 5000
lsof -i :5000

# Ou mude a porta no arquivo src/main.py
# app.run(host='0.0.0.0', port=5001, debug=True)
```

### Erro: "Permission denied"
```bash
# No Linux/Mac, certifique-se de ter permissões adequadas
chmod +x src/main.py
```

## 📱 Uso da Interface Web

1. **Acesse** http://localhost:5000
2. **Clique** na área de upload ou arraste um arquivo
3. **Selecione** um arquivo suportado (PDF, DOCX, XLSX, TXT)
4. **Clique** em "Extrair Dados"
5. **Visualize** os resultados na tela

## 🔌 Integração com Outras Aplicações

### Python
```python
import requests

def extrair_documento(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as file:
        files = {'file': file}
        response = requests.post('http://localhost:5000/api/extract', files=files)
        return response.json()

# Uso
resultado = extrair_documento('meu_documento.pdf')
print(resultado['data']['text'])
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function extrairDocumento(caminhoArquivo) {
    const form = new FormData();
    form.append('file', fs.createReadStream(caminhoArquivo));
    
    const response = await fetch('http://localhost:5000/api/extract', {
        method: 'POST',
        body: form
    });
    
    return await response.json();
}
```

## 🌐 Deploy em Produção

### Usando Gunicorn (Recomendado)
```bash
# Instale o Gunicorn
pip install gunicorn

# Execute com múltiplos workers
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Usando Docker (Opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

## 📊 Monitoramento

### Logs da Aplicação
Os logs aparecem no terminal onde você executou `python src/main.py`

### Métricas Básicas
- **Health Check**: GET /api/health
- **Tipos Suportados**: GET /api/supported-types

## 🔒 Configurações de Segurança

### Para Produção
1. **Desabilite o modo debug** em `src/main.py`:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

2. **Configure HTTPS** usando um proxy reverso (Nginx)

3. **Implemente autenticação** se necessário

4. **Configure rate limiting** para evitar abuso

## 📞 Suporte

Se você encontrar problemas:

1. **Verifique os logs** no terminal
2. **Teste os endpoints básicos** (health check)
3. **Consulte a documentação** em http://localhost:5000/docs
4. **Verifique as dependências** com `pip list`

## 🎯 Próximos Passos

Após a instalação bem-sucedida:

1. **Explore a interface web** em http://localhost:5000
2. **Leia a documentação** em http://localhost:5000/docs
3. **Teste com seus próprios documentos**
4. **Integre com suas aplicações** usando os exemplos fornecidos

---

**Projeto criado com ❤️ usando Flask, PyMuPDF, python-docx, openpyxl e outras tecnologias modernas.**

