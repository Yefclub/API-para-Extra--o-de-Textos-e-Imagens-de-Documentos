# 🐳 Docker - Document Extractor API

Este guia mostra como executar a API de extração de documentos usando Docker.

## 🚀 Execução Rápida

### Desenvolvimento
```bash
# Construir e executar com docker-compose
docker-compose up --build

# Ou em background
docker-compose up -d --build
```

### Produção
```bash
# Usar configuração de produção
docker-compose -f docker-compose.prod.yml up -d --build

# Para redes corporativas que precisam de DNS completo do host
docker-compose -f docker-compose.host-dns.yml up -d --build
```

## 🔧 Comandos Úteis

### Gerenciamento de Containers
```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar containers
docker-compose down

# Reconstruir apenas se houver mudanças
docker-compose up --build

# Remover volumes também
docker-compose down -v
```

### Build Manual da Imagem
```bash
# Construir imagem
docker build -t document-extractor-api .

# Executar container manualmente
docker run -p 5000:5000 -v $(pwd)/database:/app/database document-extractor-api
```

## 📁 Estrutura de Volumes

### Desenvolvimento (`docker-compose.yml`)
- `./database:/app/database` - Banco de dados SQLite
- `./static:/app/static` - Arquivos estáticos
- `./src:/app/src` - Código fonte (hot reload)
- `./main.py:/app/main.py` - Arquivo principal

### Produção (`docker-compose.prod.yml`)
- `./database:/app/database` - Banco de dados SQLite
- `document_uploads:/app/uploads` - Volume nomeado para uploads

## 🌐 Portas e Acesso

### Desenvolvimento
- **API**: http://localhost:5000
- **Documentação**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/api/health

### Produção
- **API**: http://localhost:5000

## 🔧 Configurações de Ambiente

### Variáveis Disponíveis
```bash
FLASK_ENV=development|production
FLASK_DEBUG=0|1
```

### Modificar Configurações
Edite o arquivo `docker-compose.yml` ou `docker-compose.prod.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - FLASK_DEBUG=0
  - CUSTOM_VAR=value
```

## 🌐 Configuração de DNS/Rede

### Opção 1: DNS Customizado (Padrão)
Usa servidores DNS públicos + configuração personalizada:
```yaml
dns:
  - 8.8.8.8
  - 8.8.4.4
  - 1.1.1.1
dns_search:
  - localdomain
```

### Opção 2: Rede do Host (Corporativo)
Para redes corporativas que precisam de DNS interno:
```bash
# Use esta configuração para acesso completo ao DNS corporativo
docker-compose -f docker-compose.host-dns.yml up -d --build
```

**Vantagens do Host Network:**
- ✅ Acesso completo ao DNS corporativo
- ✅ Resolução de nomes internos
- ✅ Acesso a serviços da rede local
- ⚠️ Remove isolamento de rede

### Opção 3: DNS Personalizado
Para configurar DNS específicos, edite o docker-compose:
```yaml
dns:
  - 192.168.1.1        # DNS da sua rede
  - 8.8.8.8            # Fallback
extra_hosts:
  - "servidor.local:192.168.1.100"
  - "api.interna:10.0.0.50"
```

## 🗄️ Banco de Dados

### SQLite (Padrão)
O banco SQLite é persistido no volume `./database:/app/database`.

### PostgreSQL (Opcional)
Para usar PostgreSQL, descomente as seções no `docker-compose.yml`:

```yaml
# Descomentar no docker-compose.yml
postgres:
  image: postgres:13
  environment:
    POSTGRES_DB: document_extractor
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

E ajuste a string de conexão no seu código.

## 🚨 Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs document-extractor-api

# Verificar se a porta está em uso
netstat -tulpn | grep :5000
```

### Problemas de permissão
```bash
# Ajustar permissões da pasta database
sudo chown -R $USER:$USER database/

# Recriar volumes
docker-compose down -v
docker-compose up --build
```

### Rebuild completo
```bash
# Limpar tudo e reconstruir
docker-compose down -v
docker system prune -f
docker-compose up --build
```

### Problemas com dependências
```bash
# Rebuild sem cache
docker-compose build --no-cache
```

## 📊 Monitoramento

### Health Check
```bash
# Verificar status do container
docker-compose ps

# Testar health check manualmente
curl http://localhost:5000/api/health
```

### Logs
```bash
# Ver todos os logs
docker-compose logs

# Logs apenas da API
docker-compose logs document-extractor-api

# Logs em tempo real
docker-compose logs -f
```

## 🔐 Produção

### Configurações de Segurança
1. **Configurar proxy reverso externo** (seu proxy interno)
2. **Configurar HTTPS** no seu proxy
3. **Ajustar rate limiting** no seu proxy
4. **Usar secrets** para dados sensíveis
5. **Expor apenas a porta 5000** para o proxy interno

### Configuração para Proxy Externo
O container da API estará disponível na porta `5000`. Configure seu proxy interno para:

```bash
# Exemplo de configuração do seu proxy apontando para:
upstream document-extractor {
    server localhost:5000;
    # ou se estiver em outro host:
    # server ip-do-container:5000;
}
```

#### Headers Recomendados para seu Proxy:
- `X-Forwarded-For`: IP real do cliente
- `X-Forwarded-Proto`: http/https
- `X-Real-IP`: IP real do cliente
- `Host`: hostname original

#### Timeout Recomendado:
- `proxy_read_timeout`: 60s (para uploads grandes)
- `client_max_body_size`: 50M (matching Flask config)

### Backup
```bash
# Backup do banco de dados
docker-compose exec document-extractor-api cp /app/database/app.db /app/database/backup-$(date +%Y%m%d).db

# Backup via volume
cp database/app.db backup/app-$(date +%Y%m%d).db
```

## 🧪 Testes

### Testar a API
```bash
# Health check
curl http://localhost:5000/api/health

# Upload de arquivo
curl -X POST -F "file=@teste.txt" http://localhost:5000/api/extract

# Análise por dados (base64)
curl -X POST http://localhost:5000/api/extract/data \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "documento.txt",
    "file_data": "SGVsbG8gV29ybGQ=",
    "encoding": "base64"
  }'

# Tipos suportados
curl http://localhost:5000/api/supported-types
```

### Dentro do Container
```bash
# Acessar shell do container
docker-compose exec document-extractor-api bash

# Executar testes Python
docker-compose exec document-extractor-api python -m pytest
``` 