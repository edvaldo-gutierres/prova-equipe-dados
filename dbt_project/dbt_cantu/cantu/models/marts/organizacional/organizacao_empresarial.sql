{{ 
    config(
        materialized='table',
        ) 
}}


WITH chefe_direto AS (
  -- Retorna o chefe direto de cada funcionário
  SELECT
    id,
    nome,
    salario,
    lider_id as id_chefe_direto
  FROM {{ ref('dados_colaboradores') }}
), chefe_indireto AS (
  -- Retorna o chefe indireto de cada funcionário
  SELECT
    chefe_direto.*,
    chefe.nome as nome_chefe_direto,
    chefe.salario as salario_chefe_direto,
    chefe.lider_id as id_chefe_indireto
  FROM chefe_direto
  LEFT JOIN {{ ref('dados_colaboradores') }} AS chefe 
    ON chefe.id = chefe_direto.id_chefe_direto
)
-- retorna o id_funcionario e o id_do_chefe_indireto
SELECT
  id as id_funcionario,
  id_chefe_indireto
FROM chefe_indireto
ORDER BY 1