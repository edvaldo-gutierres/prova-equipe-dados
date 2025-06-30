# 🚀 Guia Completo: DBT com Databricks

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Configuração de Conexão](#configuração-de-conexão)
5. [Criação de Modelos](#criação-de-modelos)
6. [Execução e Testes](#execução-e-testes)
7. [Comandos Úteis](#comandos-úteis)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

### Software Necessário
- **Python 3.8+** instalado
- **Git** para controle de versão
- **Acesso ao Databricks Workspace**
- **Databricks SQL Warehouse** configurado

### Conta Databricks
- Workspace ativo
- Token de acesso pessoal
- Permissões para criar tabelas/views
- SQL Warehouse em execução

---

## 📦 Instalação e Configuração

### 1. Instalar DBT Core
```bash
# Instalar DBT Core
pip install dbt-core

# Instalar adaptador para Databricks
pip install dbt-databricks
```

### 2. Verificar Instalação
```bash
# Verificar versão do DBT
dbt --version

# Verificar adaptadores instalados
dbt --list-adapters
```

---

## 📁 Estrutura do Projeto

### 1. Criar Estrutura de Pastas
```bash
mkdir -p dbt_project/{models/{staging,intermediate,marts},macros,tests,docs,seeds}
```

### 2. Estrutura Recomendada
```
dbt_project/
├── dbt_project.yml          # Configuração principal
├── profiles.yml             # Configuração de conexões
├── models/                  # Transformações SQL
│   ├── staging/            # Modelos de staging
│   ├── intermediate/       # Modelos intermediários
│   └── marts/              # Modelos finais
├── macros/                 # Macros reutilizáveis
├── tests/                  # Testes customizados
├── docs/                   # Documentação
└── seeds/                  # Dados estáticos
```

---

## ⚙️ Configuração de Conexão

### 1. Criar dbt_project.yml
```yaml
name: 'prova_equipe_dados'
version: '1.0.0'
config-version: 2

# Configuração do projeto
profile: 'databricks_profile'

# Configuração do modelo
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

# Configuração específica para Databricks
models:
  prova_equipe_dados:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts

# Configuração de variáveis
vars:
  project_name: "prova_equipe_dados"
  environment: "development"

# Configuração de seeds
seeds:
  prova_equipe_dados:
    +schema: raw_data
    +column_types:
      id: int
      created_at: timestamp
```

### 2. Criar profiles.yml
```yaml
databricks_profile:
  target: dev
  outputs:
    dev:
      type: databricks
      method: http
      host: "{{ env_var('DATABRICKS_HOST') }}"
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      catalog: "{{ env_var('DATABRICKS_CATALOG', 'hive_metastore') }}"
      schema: "{{ env_var('DATABRICKS_SCHEMA', 'default') }}"
      threads: 4
      timeout: 300
      retry_all: true
      http_headers:
        X-Databricks-Org-Id: "{{ env_var('DATABRICKS_ORG_ID', '') }}"
    
    prod:
      type: databricks
      method: http
      host: "{{ env_var('DATABRICKS_HOST_PROD') }}"
      token: "{{ env_var('DATABRICKS_TOKEN_PROD') }}"
      catalog: "{{ env_var('DATABRICKS_CATALOG_PROD', 'hive_metastore') }}"
      schema: "{{ env_var('DATABRICKS_SCHEMA_PROD', 'default') }}"
      threads: 8
      timeout: 600
      retry_all: true
      http_headers:
        X-Databricks-Org-Id: "{{ env_var('DATABRICKS_ORG_ID_PROD', '') }}"
```

### 3. Configurar Variáveis de Ambiente
```bash
# Criar arquivo .env
# Databricks Development
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="seu-token"
export DATABRICKS_CATALOG="seu_catalogo"
export DATABRICKS_SCHEMA="seu_schema"
export DATABRICKS_ORG_ID="1234567890123456"

# Databricks Production (opcional)
export DATABRICKS_HOST_PROD="https://your-prod-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN_PROD="seu-token"
export DATABRICKS_CATALOG_PROD="seu_catalogo"
export DATABRICKS_SCHEMA_PROD="seu_schema"
export DATABRICKS_ORG_ID_PROD="1234567890123456"
EOF

# Carregar variáveis
source .env
```

### 4. Obter Credenciais do Databricks
1. Acesse seu **Databricks Workspace**
2. Vá em **User Settings** (ícone de usuário)
3. Clique em **Developer** → **Access Tokens**
4. Clique em **Generate New Token**
5. Copie o token gerado
6. Anote a URL do seu workspace

---

## 🏗️ Exemplo: Criação de Modelos

### 1. Modelo de Staging (models/staging/stg_times.sql)
```sql
{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT 
  id,
  nome,
  cidade,
  estado,
  created_at,
  updated_at
FROM {{ source('raw_data', 'times') }}
WHERE nome IS NOT NULL
```

### 2. Modelo de Staging (models/staging/stg_jogos.sql)
```sql
{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT 
  id,
  time_casa_id,
  time_visitante_id,
  gols_casa,
  gols_visitante,
  data_jogo,
  created_at
FROM {{ source('raw_data', 'jogos') }}
WHERE data_jogo IS NOT NULL
```

### 3. Modelo Intermediário (models/intermediate/int_classificacao.sql)
```sql
{{
  config(
    materialized='view',
    schema='intermediate'
  )
}}

WITH pontos_times AS (
  SELECT 
    t.id,
    t.nome,
    t.cidade,
    t.estado,
    -- Pontos como time da casa
    SUM(CASE 
      WHEN j.gols_casa > j.gols_visitante THEN 3
      WHEN j.gols_casa = j.gols_visitante THEN 1
      ELSE 0
    END) as pontos_casa,
    -- Pontos como time visitante
    SUM(CASE 
      WHEN j2.gols_visitante > j2.gols_casa THEN 3
      WHEN j2.gols_visitante = j2.gols_casa THEN 1
      ELSE 0
    END) as pontos_visitante
  FROM {{ ref('stg_times') }} t
  LEFT JOIN {{ ref('stg_jogos') }} j ON t.id = j.time_casa_id
  LEFT JOIN {{ ref('stg_jogos') }} j2 ON t.id = j2.time_visitante_id
  GROUP BY t.id, t.nome, t.cidade, t.estado
)

SELECT 
  id,
  nome,
  cidade,
  estado,
  COALESCE(pontos_casa, 0) + COALESCE(pontos_visitante, 0) as pontos_totais
FROM pontos_times
ORDER BY pontos_totais DESC
```

### 4. Modelo Final (models/marts/dim_times.sql)
```sql
{{
  config(
    materialized='table',
    schema='marts'
  )
}}

SELECT 
  t.id,
  t.nome,
  t.cidade,
  t.estado,
  c.pontos_totais,
  RANK() OVER (ORDER BY c.pontos_totais DESC) as posicao_classificacao,
  t.created_at,
  t.updated_at
FROM {{ ref('stg_times') }} t
LEFT JOIN {{ ref('int_classificacao') }} c ON t.id = c.id
```

### 5. Configurar Sources (models/sources.yml)
```yaml
version: 2

sources:
  - name: raw_data
    description: "Dados brutos do sistema"
    tables:
      - name: times
        description: "Tabela de times do campeonato"
        columns:
          - name: id
            description: "ID único do time"
            tests:
              - unique
              - not_null
          - name: nome
            description: "Nome do time"
            tests:
              - not_null
      
      - name: jogos
        description: "Tabela de jogos do campeonato"
        columns:
          - name: id
            description: "ID único do jogo"
            tests:
              - unique
              - not_null
          - name: time_casa_id
            description: "ID do time da casa"
            tests:
              - not_null
              - relationships:
                  to: ref('stg_times')
                  field: id
```

---

## 🚀 Execução e Testes

### 1. Testar Conexão
```bash
# Testar conexão com Databricks
dbt debug
```

### 2. Executar Modelos
```bash
# Executar todos os modelos
dbt run

# Executar apenas modelos de staging
dbt run --select staging

# Executar apenas um modelo específico
dbt run --select stg_times

# Executar com full refresh
dbt run --full-refresh
```

### 3. Executar Testes
```bash
# Executar todos os testes
dbt test

# Executar testes de um modelo específico
dbt test --select stg_times

# Executar testes de sources
dbt test --select source:raw_data
```

### 4. Gerar Documentação
```bash
# Gerar documentação
dbt docs generate

# Servir documentação localmente
dbt docs serve
```

### 5. Executar Seeds
```bash
# Carregar dados estáticos
dbt seed
```

---

## 📝 Comandos Úteis

### Comandos Básicos
```bash
# Listar modelos
dbt ls

# Compilar SQL sem executar
dbt compile

# Limpar cache
dbt clean

# Instalar dependências
dbt deps

# Executar análise específica
dbt run-operation nome_do_macro
```

### Comandos de Desenvolvimento
```bash
# Executar com logs detalhados
dbt run --log-level debug

# Executar com paralelismo
dbt run --threads 8

# Executar com timeout aumentado
dbt run --timeout 600

# Executar apenas modelos modificados
dbt run --select state:modified
```

### Comandos de Produção
```bash
# Executar em produção
dbt run --target prod

# Executar com full refresh em produção
dbt run --target prod --full-refresh

# Executar testes em produção
dbt test --target prod
```

---

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão
```
Error: Failed to connect to Databricks
```
**Solução:**
- Verificar se o token está correto
- Verificar se a URL do workspace está correta
- Verificar se o SQL Warehouse está ativo

#### 2. Erro de Permissão
```
Error: Permission denied
```
**Solução:**
- Verificar permissões no Databricks
- Verificar se o usuário tem acesso ao catalog/schema
- Verificar se o token tem permissões adequadas

#### 3. Erro de Timeout
```
Error: Query timeout
```
**Solução:**
- Aumentar timeout no profiles.yml
- Otimizar queries
- Verificar performance do SQL Warehouse

#### 4. Erro de Schema
```
Error: Schema not found
```
**Solução:**
- Verificar se o schema existe no Databricks
- Criar schema se necessário
- Verificar configuração no profiles.yml

### Logs e Debug
```bash
# Ver logs detalhados
dbt run --log-level debug

# Ver logs de um modelo específico
dbt run --select stg_times --log-level debug

# Ver logs de testes
dbt test --log-level debug
```

---

## 📊 Monitoramento

### 1. Verificar Execução
```bash
# Ver status dos modelos
dbt ls --select state:modified

# Ver dependências
dbt list --select +stg_times

# Ver lineage
dbt show --select dim_times
```

### 2. Performance
```bash
# Ver tempo de execução
dbt run --log-level info

# Ver queries geradas
dbt compile --select stg_times
```

---

## 🎯 Melhorias Futuras

1. **Criar Macros Customizados**
   - Macros para transformações comuns
   - Macros para testes específicos
   - Macros para documentação

2. **Implementar Testes Customizados**
   - Testes de negócio
   - Testes de qualidade de dados
   - Testes de performance

3. **Configurar CI/CD**
   - GitHub Actions
   - Jenkins
   - Azure DevOps

4. **Implementar Observabilidade**
   - dbt_utils
   - dbt_artifacts
   - dbt_expectations

---

## 📚 Recursos Adicionais

- [Documentação Oficial DBT](https://docs.getdbt.com/)
- [DBT Databricks Adapter](https://docs.getdbt.com/reference/warehouse-setups/databricks-setup)
- [DBT Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Databricks Documentation](https://docs.databricks.com/)

---

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verificar logs detalhados
2. Consultar documentação oficial
3. Verificar configurações de conexão
4. Testar com modelo simples primeiro

---