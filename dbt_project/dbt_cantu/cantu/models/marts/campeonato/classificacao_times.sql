{{ 
    config(
        materialized='table',
        ) 
}}


WITH resultados_mandante AS (
    SELECT 
        mandante_time AS time_id,
        CASE 
            WHEN mandante_gols > visitante_gols THEN 3
            WHEN mandante_gols = visitante_gols THEN 1
            ELSE 0
        END AS pontos
    FROM {{ ref('dados_jogos') }}
),
resultados_visitante AS (
    SELECT 
        visitante_time AS time_id,
        CASE 
            WHEN visitante_gols > mandante_gols THEN 3
            WHEN visitante_gols = mandante_gols THEN 1
            ELSE 0
        END AS pontos
    FROM {{ ref('dados_jogos') }}
),
todos_resultados AS (
    SELECT * FROM resultados_mandante
    UNION ALL
    SELECT * FROM resultados_visitante
),
pontuacao_por_time AS (
    SELECT 
        time_id,
        SUM(pontos) AS num_pontos
    FROM todos_resultados
    GROUP BY time_id
)

SELECT 
    t.time_nome,
    COALESCE(p.num_pontos, 0) AS numero_pontos
FROM {{ ref('dados_times') }} t
LEFT JOIN pontuacao_por_time p ON t.time_id = p.time_id
ORDER BY num_pontos DESC, t.time_id ASC;