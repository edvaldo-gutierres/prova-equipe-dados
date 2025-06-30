# 📄 Prova de Proficiência – Engenheiro de Dados | CantuStore

Olá, Capitani! Espero que estejam todos bem.

Me chamo **Edvaldo Gutierres** — [LinkedIn](https://www.linkedin.com/in/edvaldo-gutierres-6b4a5768/)

---

## 📋 Descrição

Este repositório apresenta a solução desenvolvida para a **prova técnica da vaga de Engenheiro de Dados** da **CantuStore**. O projeto evidencia competências técnicas em **SQL**, **PySpark**, **análise de dados** e **boas práticas de engenharia de dados** na plataforma **Databricks**, com foco em problemas reais do contexto de e-commerce.

> Embora a execução prática não tenha sido solicitada, optei por validar todos os scripts SQL tanto no ambiente **Databricks SQL** quanto via **dbt**, antecipando um dos requisitos desejáveis da vaga e reforçando a aderência ao cenário de produção.

---

## 🏢 Sobre a CantuStore

A **CantuStore** é uma plataforma de tecnologia e logística especializada em soluções completas para o mercado de pneus. Com uma abordagem 360°, conecta quem compra e quem vende, promovendo a evolução conjunta de pessoas e negócios.

---

## 🎯 Objetivos do Teste

### Parte 1 – SQL (Databricks SQL)

* Demonstrar domínio em **consultas SQL** avançadas
* Resolver desafios de **classificação**, **hierarquia** e **análise de comissões**
* Explorar recursos do Databricks SQL para consultas performáticas

### Parte 2 – Análise de Dados (Databricks Notebooks)

* Investigar padrões de **abandono de carrinho** com **PySpark**
* Gerar **insights e relatórios estratégicos**
* Utilizar o Delta Lake para **armazenamento otimizado**
* Automatizar exportações de dados estruturados

---

## 🛠️ Tecnologias Utilizadas

* **Databricks** – Plataforma principal de desenvolvimento
* **Databricks SQL** – Consultas e análises analíticas
* **PySpark** – Processamento distribuído e transformações de dados
* **Delta Lake** – Armazenamento com suporte ACID e time travel
* **dbt (Data Build Tool)** – Modelagem declarativa, seeds, versionamento e modularização
* **Poetry** – Gerenciamento de dependências e ambientes virtuais
* **Git** – Controle de versão
* **Markdown** – Documentação clara e estruturada

---

## 📁 Estrutura inicial do Projeto

```
prova-equipe-dados/
├── 📄 README.md                 # Documentação principal do projeto
├── 📋 LICENSE                   # Licença MIT
├── 🚫 .gitignore               # Arquivos ignorados pelo controle de versão
├── 📦 pyproject.toml           # Configuração Poetry e dependências
├── 🔒 poetry.lock              # Lock file com versões fixas
│
├── 🏗️ databricks/              # Scripts e notebooks Databricks
│   ├── sql/                    # Consultas SQL (Parte 1)
│   │   ├── 1.1_campeonato.sql     # → Classificação de times
│   │   ├── 1.2_comissoes.sql      # → Análise de vendedores
│   │   └── 1.3_hierarquia.sql     # → Estrutura organizacional
│   │
│   └── notebooks/              # Análises PySpark (Parte 2)
│       ├── 2.1_analise_carrinho_abandonado.py  # → Padrões de abandono
│       ├── 2.2_relatorios.py                   # → Relatórios estratégicos
│       └── 2.3_exportacao_dados.py             # → Exportação estruturada
│
├── 🔧 dbt_project/             # Projeto dbt para validação e modelagem
│   ├── dbt_project.yml            # → Configuração do projeto dbt
│   ├── profiles.yml               # → Perfis de conexão Databricks
│   ├── models/                    # → Modelos SQL modulares
│   │   ├── staging/               # → Camada de staging
│   │   ├── marts/                 # → Modelos finais (classificacao, comissoes, hierarquia)
│   │   └── schema.yml             # → Documentação e testes
│   ├── seeds/                     # → Dados estáticos (CSV)
│   │   └── sample_data.csv        # → Dados de teste para validação
│   ├── tests/                     # → Testes automatizados
│   └── macros/                    # → Funções reutilizáveis
│
├── 📊 data/                    # Datasets de entrada
│   └── carrinho_abandonado.csv    # → Base principal para análises
│
└── 📈 reports/                 # Relatórios e exportações geradas
    ├── relatorio_produtos_mensal.csv  # → Resumo mensal
    ├── relatorio_diario.csv           # → Métricas diárias
    └── top_50_carrinhos.txt           # → Maiores carrinhos (formato .txt)
```
---

## 🚀 Como Executar

### Pré-requisitos

* **Databricks Workspace** com permissões
* **SQL Warehouse** e **cluster PySpark**
* **Poetry** instalado (`pip install poetry`)
* **Git** instalado

### Etapas

```bash
# Clone o repositório
git clone https://github.com/edvaldo-gutierres/prova-equipe-dados.git
cd prova-equipe-dados

# Instale dependências com Poetry
poetry install
poetry add databricks-cli dbt-databricks --group dev

# Ative o ambiente virtual
poetry shell

# Configure o Databricks CLI
databricks configure --token

# Importe os notebooks para o workspace
databricks workspace import_dir databricks/notebooks /Shared/Prova-Equipe-Dados

# Execute validações dbt (opcional)
cd dbt_project
dbt seed    # Carrega dados de teste
dbt run     # Executa modelos
dbt test    # Valida testes automatizados
```

**Configurações sugeridas:**

* **Cluster:** Databricks Runtime 13.3 LTS (Spark 3.4.1)
* **SQL Warehouse:** Size Small, auto-stop em 10 min

### Gerenciamento de Dependências

O projeto utiliza **Poetry** para:
* 📦 **Gerenciamento de dependências** – Controle preciso de versões
* 🔒 **Ambientes isolados** – Evita conflitos entre projetos
* 🚀 **Build e deploy** – Empacotamento simplificado
* 📋 **Metadata do projeto** – Configuração centralizada no `pyproject.toml`

---

## 📊 Desafios Implementados

### Parte 1 – SQL

#### 1.1 Campeonato

* Cálculo de pontuação por time (vitória, empate, derrota)
* Classificação final com ordenação por pontos

#### 1.2 Comissões

* Filtragem de vendedores com até 3 transferências ≥ R\$1.024
* Análise agrupada por vendedor

#### 1.3 Hierarquia Organizacional

* Mapeamento de chefes diretos e indiretos
* Verificação de salário ≥ 2x o subordinado

### Parte 2 – PySpark

#### 2.1 Análise de Carrinhos Abandonados

* Produtos com maior índice de abandono
* Padrões de abandono em duplas de produtos
* Comparativo temporal e por estado

#### 2.2 Relatórios Estratégicos

* Relatórios mensais e diários exportados em CSV
* Métricas: quantidade de itens, valor total, produtos

#### 2.3 Exportação Estruturada

* Geração de `.txt` com os 50 maiores carrinhos abandonados
* Layout com formatação específica via PySpark

---

## 🔧 Desenvolvimento

### Padrões de Código e Boas Práticas

* **Databricks SQL** – Escrita otimizada com foco em performance e clareza
* **PySpark** – Processamento distribuído com DataFrames e expressões eficientes
* **dbt** – Modelos modulares com uso de `seeds`, `ref`, testes e versionamento
* **Poetry** – Dependency management, versionamento semântico e builds reproduzíveis
* **Notebooks** – Documentação com markdowns, visualizações e organização por etapas
* **Delta Lake** – Uso de ACID, controle de SCDs e time travel
* **Git** – Commits atômicos e semânticos

### Exemplo de Commits

```
feat: adiciona cálculo de classificação no campeonato
fix: ajusta condição de empate em análise de comissões
refactor: organiza lógica de hierarquia com auto join
build: atualiza dependências Poetry para dbt 1.6.0
docs: atualiza README com orientações de execução
test: valida queries dbt com dados de seed
```

---

## 📈 Indicadores de Sucesso

* ✅ Execução validada no Databricks SQL e dbt
* ✅ Relatórios exportados corretamente
* ✅ Processamento escalável com PySpark
* ✅ Scripts claros e bem documentados
* ✅ Dados versionados e modularizados com dbt
* ✅ Testes e evidências alinhadas ao cenário real

---

## 👨‍💻 Sobre o Autor

**Edvaldo Gutierres**

* 💼 [LinkedIn](https://www.linkedin.com/in/edvaldo-gutierres-6b4a5768/)
* 📧 [edvaldo\_gutierres@yahoo.com.br](mailto:edvaldo_gutierres@yahoo.com.br)
* 💻 [GitHub](https://github.com/edvaldo-gutierres)

---

## 🙏 Agradecimentos

Agradeço a oportunidade e estou à disposição para qualquer esclarecimento ou conversa técnica.

---
