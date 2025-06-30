# 📊 Exemplos Práticos: Modelos DBT para o Projeto

## 🎯 Baseado no seu projeto atual, aqui estão exemplos práticos de transformações DBT

---

## 📁 Estrutura de Arquivos

```
dbt_project/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/
│   │   ├── stg_times.sql
│   │   ├── stg_jogos.sql
│   │   ├── stg_comissoes.sql
│   │   └── stg_colaboradores.sql
│   ├── intermediate/
│   │   ├── int_classificacao_times.sql
│   │   ├── int_vendedores_comissao.sql
│   │   └── int_hierarquia_empresarial.sql
│   └── marts/
│       ├── dim_times.sql
│       ├── fact_jogos.sql
│       ├── dim_vendedores.sql
│       └── dim_colaboradores.sql
├── macros/
│   └── utils.sql
├── tests/
│   └── custom_tests.sql
└── seeds/
    └── dados_iniciais.csv
```

---

## 🏗️ Modelos de Staging

### 1. stg_times.sql
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
  AND cidade IS NOT NULL
```

### 2. stg_jogos.sql
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
  AND time_casa_id IS NOT NULL
  AND time_visitante_id IS NOT NULL
```

### 3. stg_comissoes.sql
```sql
{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT 
  id,
  vendedor_id,
  valor_transferencia,
  data_transferencia,
  created_at
FROM {{ source('raw_data', 'comissoes') }}
WHERE valor_transferencia > 0
  AND data_transferencia IS NOT NULL
```

### 4. stg_colaboradores.sql
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
  salario,
  chefe_id,
  created_at
FROM {{ source('raw_data', 'colaboradores') }}
WHERE nome IS NOT NULL
  AND salario > 0
```

---

## 🔄 Modelos Intermediários

### 1. int_classificacao_times.sql
```sql
{{
  config(
    materialized='view',
    schema='intermediate'
  )
}}

WITH pontos_por_jogo AS (
  SELECT 
    time_casa_id as time_id,
    CASE 
      WHEN gols_casa > gols_visitante THEN 3
      WHEN gols_casa = gols_visitante THEN 1
      ELSE 0
    END as pontos
  FROM {{ ref('stg_jogos') }}
  
  UNION ALL
  
  SELECT 
    time_visitante_id as time_id,
    CASE 
      WHEN gols_visitante > gols_casa THEN 3
      WHEN gols_visitante = gols_casa THEN 1
      ELSE 0
    END as pontos
  FROM {{ ref('stg_jogos') }}
),

classificacao AS (
  SELECT 
    t.id,
    t.nome,
    t.cidade,
    t.estado,
    COALESCE(SUM(p.pontos), 0) as pontos_totais,
    COUNT(p.pontos) as jogos_disputados
  FROM {{ ref('stg_times') }} t
  LEFT JOIN pontos_por_jogo p ON t.id = p.time_id
  GROUP BY t.id, t.nome, t.cidade, t.estado
)

SELECT 
  id,
  nome,
  cidade,
  estado,
  pontos_totais,
  jogos_disputados,
  RANK() OVER (ORDER BY pontos_totais DESC, nome ASC) as posicao
FROM classificacao
ORDER BY pontos_totais DESC, nome ASC
```

### 2. int_vendedores_comissao.sql
```sql
{{
  config(
    materialized='view',
    schema='intermediate'
  )
}}

WITH vendedores_transferencias AS (
  SELECT 
    vendedor_id,
    COUNT(*) as total_transferencias,
    SUM(valor_transferencia) as valor_total_transferencias
  FROM {{ ref('stg_comissoes') }}
  GROUP BY vendedor_id
  HAVING COUNT(*) <= 3 
    AND SUM(valor_transferencia) >= 1024
)

SELECT 
  vt.vendedor_id,
  vt.total_transferencias,
  vt.valor_total_transferencias,
  c.valor_transferencia,
  c.data_transferencia
FROM vendedores_transferencias vt
JOIN {{ ref('stg_comissoes') }} c ON vt.vendedor_id = c.vendedor_id
ORDER BY vt.valor_total_transferencias DESC, vt.vendedor_id
```

### 3. int_hierarquia_empresarial.sql
```sql
{{
  config(
    materialized='view',
    schema='intermediate'
  )
}}

WITH RECURSIVE hierarquia AS (
  -- Base case: funcionários sem chefe (nível 1)
  SELECT 
    id,
    nome,
    salario,
    chefe_id,
    1 as nivel_hierarquico,
    CAST(id as STRING) as caminho_hierarquico
  FROM {{ ref('stg_colaboradores') }}
  WHERE chefe_id IS NULL
  
  UNION ALL
  
  -- Recursive case: funcionários com chefe
  SELECT 
    c.id,
    c.nome,
    c.salario,
    c.chefe_id,
    h.nivel_hierarquico + 1,
    CONCAT(h.caminho_hierarquico, ' -> ', CAST(c.id as STRING))
  FROM {{ ref('stg_colaboradores') }} c
  JOIN hierarquia h ON c.chefe_id = h.id
),

chefes_indiretos AS (
  SELECT 
    f.id as funcionario_id,
    f.nome as funcionario_nome,
    f.salario as funcionario_salario,
    c.id as chefe_id,
    c.nome as chefe_nome,
    c.salario as chefe_salario,
    c.nivel_hierarquico as nivel_chefe,
    f.nivel_hierarquico as nivel_funcionario
  FROM hierarquia f
  JOIN hierarquia c ON f.caminho_hierarquico LIKE CONCAT('%', CAST(c.id as STRING), '%')
  WHERE c.id != f.id
    AND c.salario >= (f.salario * 2)
)

SELECT 
  funcionario_id,
  funcionario_nome,
  funcionario_salario,
  chefe_id,
  chefe_nome,
  chefe_salario,
  nivel_chefe,
  nivel_funcionario,
  ROUND(chefe_salario / funcionario_salario, 2) as multiplicador_salario
FROM chefes_indiretos
ORDER BY funcionario_id, nivel_chefe
```

---

## 🎯 Modelos Finais (Marts)

### 1. dim_times.sql
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
  c.jogos_disputados,
  c.posicao,
  CASE 
    WHEN c.posicao <= 4 THEN 'Libertadores'
    WHEN c.posicao <= 8 THEN 'Sul-Americana'
    WHEN c.posicao <= 12 THEN 'Meio da tabela'
    ELSE 'Rebaixamento'
  END as classificacao_categoria,
  t.created_at,
  t.updated_at
FROM {{ ref('stg_times') }} t
LEFT JOIN {{ ref('int_classificacao_times') }} c ON t.id = c.id
```

### 2. fact_jogos.sql
```sql
{{
  config(
    materialized='table',
    schema='marts'
  )
}}

SELECT 
  j.id as jogo_id,
  j.time_casa_id,
  tc.nome as time_casa_nome,
  j.time_visitante_id,
  tv.nome as time_visitante_nome,
  j.gols_casa,
  j.gols_visitante,
  j.data_jogo,
  CASE 
    WHEN j.gols_casa > j.gols_visitante THEN 'Casa'
    WHEN j.gols_visitante > j.gols_casa THEN 'Visitante'
    ELSE 'Empate'
  END as resultado,
  ABS(j.gols_casa - j.gols_visitante) as diferenca_gols,
  j.created_at
FROM {{ ref('stg_jogos') }} j
JOIN {{ ref('stg_times') }} tc ON j.time_casa_id = tc.id
JOIN {{ ref('stg_times') }} tv ON j.time_visitante_id = tv.id
```

### 3. dim_vendedores.sql
```sql
{{
  config(
    materialized='table',
    schema='marts'
  )
}}

SELECT 
  vendedor_id,
  total_transferencias,
  valor_total_transferencias,
  valor_medio_transferencia,
  CASE 
    WHEN total_transferencias = 1 THEN 'Primeira venda'
    WHEN total_transferencias = 2 THEN 'Segunda venda'
    WHEN total_transferencias = 3 THEN 'Terceira venda'
    ELSE 'Múltiplas vendas'
  END as categoria_vendedor,
  CASE 
    WHEN valor_total_transferencias >= 2000 THEN 'Alto valor'
    WHEN valor_total_transferencias >= 1500 THEN 'Médio valor'
    ELSE 'Baixo valor'
  END as categoria_valor
FROM (
  SELECT 
    vendedor_id,
    COUNT(*) as total_transferencias,
    SUM(valor_transferencia) as valor_total_transferencias,
    AVG(valor_transferencia) as valor_medio_transferencia
  FROM {{ ref('stg_comissoes') }}
  GROUP BY vendedor_id
  HAVING COUNT(*) <= 3 
    AND SUM(valor_transferencia) >= 1024
)
```

### 4. dim_colaboradores.sql
```sql
{{
  config(
    materialized='table',
    schema='marts'
  )
}}

SELECT 
  c.funcionario_id,
  c.funcionario_nome,
  c.funcionario_salario,
  c.chefe_id,
  c.chefe_nome,
  c.chefe_salario,
  c.nivel_chefe,
  c.nivel_funcionario,
  c.multiplicador_salario,
  CASE 
    WHEN c.multiplicador_salario >= 3 THEN 'Alto multiplicador'
    WHEN c.multiplicador_salario >= 2 THEN 'Multiplicador padrão'
    ELSE 'Baixo multiplicador'
  END as categoria_multiplicador
FROM {{ ref('int_hierarquia_empresarial') }} c
```

---

## 🧪 Testes Customizados

### 1. tests/custom_tests.sql
```sql
-- Teste: Verificar se não há empates com gols diferentes
SELECT 
  id,
  gols_casa,
  gols_visitante
FROM {{ ref('stg_jogos') }}
WHERE gols_casa = gols_visitante 
  AND (gols_casa IS NULL OR gols_visitante IS NULL)

-- Teste: Verificar se salários são positivos
SELECT 
  id,
  nome,
  salario
FROM {{ ref('stg_colaboradores') }}
WHERE salario <= 0

-- Teste: Verificar se valores de transferência são positivos
SELECT 
  id,
  vendedor_id,
  valor_transferencia
FROM {{ ref('stg_comissoes') }}
WHERE valor_transferencia <= 0
```

---

## 🔧 Macros Úteis

### 1. macros/utils.sql
```sql
-- Macro para gerar surrogate key
{% macro generate_surrogate_key(field_list) %}
  {%- set fields = field_list.split(',') -%}
  {%- set field_strings = [] -%}
  {%- for field in fields -%}
    {%- set field_strings = field_strings + [field.strip()] -%}
  {%- endfor -%}
  {{ dbt_utils.generate_surrogate_key(field_strings) }}
{% endmacro %}

-- Macro para validar data
{% macro is_valid_date(date_column) %}
  CASE 
    WHEN {{ date_column }} IS NULL THEN FALSE
    WHEN TRY_CAST({{ date_column }} AS DATE) IS NULL THEN FALSE
    ELSE TRUE
  END
{% endmacro %}

-- Macro para calcular idade
{% macro calculate_age(birth_date_column) %}
  DATE_DIFF(CURRENT_DATE(), {{ birth_date_column }}, YEAR)
{% endmacro %}
```

---

## 📊 Seeds (Dados Estáticos)

### 1. seeds/dados_iniciais.csv
```csv
id,nome,cidade,estado,created_at
1,Time A,São Paulo,SP,2024-01-01
2,Time B,Rio de Janeiro,RJ,2024-01-01
3,Time C,Belo Horizonte,MG,2024-01-01
```

---

## 🚀 Comandos de Execução

```bash
# 1. Testar conexão
dbt debug

# 2. Executar modelos de staging
dbt run --select staging

# 3. Executar modelos intermediários
dbt run --select intermediate

# 4. Executar modelos finais
dbt run --select marts

# 5. Executar todos os modelos
dbt run

# 6. Executar testes
dbt test

# 7. Gerar documentação
dbt docs generate
dbt docs serve

# 8. Executar seeds
dbt seed
```

---

## 📈 Monitoramento

### 1. Verificar Dependências
```bash
# Ver lineage de um modelo
dbt show --select dim_times

# Ver dependências
dbt list --select +stg_times
```

### 2. Verificar Performance
```bash
# Ver queries compiladas
dbt compile --select int_classificacao_times

# Ver logs detalhados
dbt run --select marts --log-level debug
```

---

**🎯 Estes exemplos são baseados no seu projeto atual e demonstram como transformar suas queries SQL existentes em modelos DBT organizados e reutilizáveis!** 