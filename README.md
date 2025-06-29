# Prova de Proficiência - Engenheiro de Dados | CantuStore

## 📋 Descrição

Este repositório contém a solução desenvolvida para o teste de proficiência da vaga de **Engenheiro de Dados** da **CantuStore**. O projeto demonstra habilidades técnicas em SQL, análise de dados e processamento de dados utilizando a plataforma **Databricks** para resolver problemas reais de e-commerce.

## 🏢 Sobre a CantuStore

A **CantuStore** é uma plataforma de tecnologia e logística que viabiliza soluções completas em pneus, guiando quem compra e apoiando quem vende. Produtos e serviços em uma experiência 360° para abrir caminhos e ver pessoas e negócios evoluindo junto com a gente.

## 🎯 Objetivos do Teste

### Parte 1 - SQL (Databricks SQL)
- Demonstrar proficiência em consultas SQL complexas no ambiente Databricks
- Resolver problemas de classificação e hierarquia organizacional
- Implementar análises de comissões e vendas usando Databricks SQL

### Parte 2 - Análise de Dados (Databricks Notebooks)
- Analisar dados de carrinho abandonado em e-commerce usando PySpark
- Identificar padrões e insights para redução de abandono
- Gerar relatórios estratégicos para tomada de decisão
- Utilizar Databricks e PySpark para processamento distribuído

## 🛠️ Tecnologias Utilizadas

- **Databricks** - Plataforma principal de desenvolvimento
- **Databricks SQL** - Consultas SQL e análise de dados
- **PySpark** - Framework para big data e processamento distribuído
- **Databricks Notebooks** - Desenvolvimento e documentação
- **Delta Lake** - Armazenamento de dados otimizado
- **Git** - Controle de versão
- **Markdown** - Documentação

## 📁 Estrutura do Projeto

```
prova-equipe-dados/
├── README.md                    # Documentação principal
├── LICENSE                      # Licença MIT
├── .gitignore                   # Arquivos ignorados pelo Git
├── databricks/                  # Código Databricks
│   ├── sql/                     # Queries SQL
│   │   ├── 1.1_campeonato.sql  # Consulta de classificação
│   │   ├── 1.2_comissoes.sql   # Análise de comissões
│   │   └── 1.3_hierarquia.sql  # Organização empresarial
│   └── notebooks/               # Databricks Notebooks
│       ├── 2.1_analise_carrinho_abandonado.py
│       ├── 2.2_relatorios.py
│       └── 2.3_exportacao_dados.py
├── data/                        # Dados de entrada
│   └── carrinho_abandonado.csv
├── reports/                     # Relatórios gerados
│   ├── relatorio_produtos_mensal.csv
│   ├── relatorio_diario.csv
│   └── top_50_carrinhos.txt
└── requirements.txt             # Dependências Python
```

## 🚀 Como Executar

### Pré-requisitos

- **Databricks Workspace** - Acesso à plataforma Databricks
- **Databricks Runtime** - Cluster configurado com PySpark
- **Databricks SQL** - Acesso ao SQL Warehouse
- **Git** - Controle de versão

### Configuração no Databricks

1. **Clone o repositório**:
```bash
git clone https://github.com/edvaldo-gutierres/prova-equipe-dados.git
```

2. **Configure o Databricks CLI**:
```bash
pip install databricks-cli
databricks configure --token
```

3. **Importe os notebooks**:
```bash
databricks workspace import_dir databricks/notebooks /Shared/Prova-Equipe-Dados
```

4. **Configure o cluster**:
   - Runtime: Databricks Runtime 13.3 LTS (Scala 2.12, Spark 3.4.1)
   - Node Type: Standard_DS3_v2 ou superior
   - Min Workers: 1, Max Workers: 3

5. **Configure o SQL Warehouse**:
   - Size: Small (2X-Small)
   - Auto-stop: 10 minutos
   - Auto-scaling: Enabled

## 📊 Desafios Implementados

### Parte 1 - SQL (Databricks SQL)

#### 1.1 Campeonato
- **Objetivo**: Calcular pontos de equipes em campeonato
- **Regras**: Vitória = 3 pontos, Empate = 1 ponto, Derrota = 0 pontos
- **Entrada**: Tabelas `times` e `jogos`
- **Saída**: Classificação ordenada por pontos
- **Tecnologia**: Databricks SQL

#### 1.2 Comissões
- **Objetivo**: Identificar vendedores com até 3 transferências totalizando ≥ R$ 1.024
- **Entrada**: Tabela `comissoes`
- **Saída**: Lista de vendedores que atendem aos critérios
- **Tecnologia**: Databricks SQL

#### 1.3 Organização Empresarial
- **Objetivo**: Encontrar chefes indiretos com salário ≥ 2x do funcionário
- **Entrada**: Tabela `colaboradores`
- **Saída**: Relacionamento funcionário-chefe hierárquico
- **Tecnologia**: Databricks SQL

### Parte 2 - Análise de Dados (Databricks Notebooks)

#### 2.1 Análise de Carrinho Abandonado
- **Produtos com mais abandono** - Análise PySpark
- **Duplas de produtos abandonados** - Processamento distribuído
- **Produtos com aumento de abandono** - Análise temporal
- **Produtos novos no primeiro mês** - Agregações complexas
- **Estados com mais abandonos** - Análise geográfica

#### 2.2 Relatórios Estratégicos
- **Relatório mensal**: Produtos, carrinhos abandonados, itens, valor não faturado
- **Relatório diário**: Quantidade de carrinhos, itens, valor não faturado
- **Exportação**: Delta Lake e CSV

#### 2.3 Exportação de Dados
- **Arquivo .txt**: Top 50 carrinhos com maior valor total
- **Layout específico**: Dados estruturados conforme especificação
- **Processamento**: PySpark para performance

## 🔧 Desenvolvimento

### Padrões de Código

- **Databricks SQL**: Otimização de queries para performance
- **PySpark**: Uso eficiente de DataFrames e Spark SQL
- **Notebooks**: Documentação clara com markdown
- **Delta Lake**: Utilização de recursos ACID
- **Commits**: Atômicos e descritivos

### Estrutura de Commits

```
feat: adiciona consulta SQL para campeonato no Databricks
fix: corrige cálculo de pontos com PySpark
docs: atualiza documentação dos notebooks
refactor: otimiza query de hierarquia com Delta Lake
test: adiciona testes para análise de dados
```

## 📈 Métricas de Sucesso

- [ ] Consultas SQL executando no Databricks SQL
- [ ] Análises PySpark gerando insights relevantes
- [ ] Relatórios exportados no formato correto
- [ ] Performance otimizada com processamento distribuído
- [ ] Documentação clara nos notebooks
- [ ] Uso eficiente dos recursos Databricks

## 📝 Documentação

- **README.md** - Documentação principal do projeto
- **Databricks SQL/*** - Comentários nas consultas SQL
- **Databricks Notebooks/*** - Análises documentadas com markdown
- **LICENSE** - Licença MIT para uso livre

## 🤝 Contribuição

Este é um projeto de teste de proficiência. Para contribuições em projetos futuros:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaAnalise`)
3. Commit suas mudanças (`git commit -m 'Adiciona análise de tendências'`)
4. Push para a branch (`git push origin feature/NovaAnalise`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Edvaldo Gutierres**

- LinkedIn: [https://www.linkedin.com/in/edvaldo-gutierres-6b4a5768/]
- Email: [edvaldo_gutierres@yahoo.com.br]
- GitHub: [https://github.com/edvaldo-gutierres]

---