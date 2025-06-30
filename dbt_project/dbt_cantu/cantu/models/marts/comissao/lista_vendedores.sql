{{ 
    config(
        materialized='table',
        ) 
}}


WITH ranked_comissoes AS (
    SELECT
        vendedor,
        valor,
        ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS rn
    FROM {{ ref('dados_comissoes') }}
),
top3_comissoes AS (
    SELECT
        vendedor,
        valor
    FROM ranked_comissoes
    WHERE rn <= 3
),
vendedores_qualificados AS (
    SELECT
        vendedor,
        COUNT(*) AS qtd_transferencias,
        SUM(valor) AS total_recebido
    FROM top3_comissoes
    GROUP BY vendedor
    HAVING qtd_transferencias <= 3 AND total_recebido >= 1024
)
SELECT vendedor
FROM vendedores_qualificados
ORDER BY vendedor ASC