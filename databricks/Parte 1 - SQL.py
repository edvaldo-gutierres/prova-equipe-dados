# Databricks notebook source
# MAGIC %md
# MAGIC # Prova Equipe de Dados
# MAGIC
# MAGIC Somos a CantuStore: Plataforma de tecnologia e logística que viabiliza soluções completas em pneus, 
# MAGIC guiando quem compra e apoiando quem vende. Se o assunto é pneu, você resolve aqui. Produtos e 
# MAGIC serviços em uma experiência 360° para abrir caminhos e ver pessoas e negócios evoluindo junto com 
# MAGIC a gente. Afinal, ficar parado não é opção, pelos menos pra nós. 

# COMMAND ----------

# DBTITLE 1,Importa Lib's
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DateType, FloatType, IntegerType, DoubleType
from datetime import datetime

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 1 - SQL

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1 Campeonato
# MAGIC
# MAGIC A organização e os resultados de um campeonato estão representados pelas seguintes tabelas:
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC Tabela `times`
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE times (
# MAGIC     time_id INTEGER NOT NULL,
# MAGIC     time_nome VARCHAR NOT NULL,
# MAGIC     UNIQUE(time_id)
# MAGIC );
# MAGIC ````
# MAGIC
# MAGIC <br>
# MAGIC
# MAGIC Dados da Tabela `times`
# MAGIC
# MAGIC | Time\_id | Time\_nome |
# MAGIC | -------- | ---------- |
# MAGIC | 10       | Financeiro |
# MAGIC | 20       | Marketing  |
# MAGIC | 30       | Logística  |
# MAGIC | 40       | TI         |
# MAGIC | 50       | Dados      |
# MAGIC
# MAGIC ---
# MAGIC <br>
# MAGIC
# MAGIC ## Tabela `jogos`
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE jogos (
# MAGIC     jogo_id INTEGER NOT NULL,
# MAGIC     mandante_time INTEGER NOT NULL,
# MAGIC     visitante_time INTEGER NOT NULL,
# MAGIC     mandante_gols INTEGER NOT NULL,
# MAGIC     visitante_gols INTEGER NOT NULL,
# MAGIC     UNIQUE(jogo_id)
# MAGIC );
# MAGIC ```
# MAGIC ---
# MAGIC <br>
# MAGIC
# MAGIC Essas tabelas podem ser utilizadas para armazenar os dados das equipes e os resultados dos jogos em um campeonato entre departamentos.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # 🏆 Estrutura do Campeonato
# MAGIC
# MAGIC A seguir, temos a modelagem e os dados de um campeonato entre equipes:
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📄 Tabela `times`
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE times (
# MAGIC     time_id INTEGER NOT NULL,
# MAGIC     time_nome VARCHAR NOT NULL,
# MAGIC     UNIQUE(time_id)
# MAGIC );
# MAGIC ````
# MAGIC
# MAGIC ### 📌 Dados da Tabela `times`
# MAGIC
# MAGIC | Time\_id | Time\_nome |
# MAGIC | -------- | ---------- |
# MAGIC | 10       | Financeiro |
# MAGIC | 20       | Marketing  |
# MAGIC | 30       | Logística  |
# MAGIC | 40       | TI         |
# MAGIC | 50       | Dados      |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📄 Tabela `jogos`
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE jogos (
# MAGIC     jogo_id INTEGER NOT NULL,
# MAGIC     mandante_time INTEGER NOT NULL,
# MAGIC     visitante_time INTEGER NOT NULL,
# MAGIC     mandante_gols INTEGER NOT NULL,
# MAGIC     visitante_gols INTEGER NOT NULL,
# MAGIC     UNIQUE(jogo_id)
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ### 📌 Dados da Tabela `jogos`
# MAGIC
# MAGIC | Jogo\_id | Time\_mandante | Time\_visitante | Gols\_mandante | Gols\_visitante |
# MAGIC | -------- | -------------- | --------------- | -------------- | --------------- |
# MAGIC | 1        | 30             | 20              | 1              | 0               |
# MAGIC | 2        | 10             | 20              | 1              | 2               |
# MAGIC | 3        | 20             | 50              | 2              | 2               |
# MAGIC | 4        | 10             | 30              | 1              | 1               |
# MAGIC | 5        | 30             | 50              | 0              | 1               |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⚙️ Regras para Pontuação
# MAGIC
# MAGIC * ✅ Vitória: 3 pontos (mais gols que o adversário)
# MAGIC * ⚖️ Empate: 1 ponto (mesmo número de gols)
# MAGIC * ❌ Derrota: 0 pontos (menos gols que o adversário)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivo
# MAGIC
# MAGIC Escrever uma consulta que calcule o total de pontos de cada equipe (`time_id`) com base nas regras acima.
# MAGIC
# MAGIC ### Requisitos da consulta:
# MAGIC
# MAGIC * Retornar o nome do time e o total de pontos (`num_pontos`);
# MAGIC * Agrupar por time;
# MAGIC * Ordenar por `num_pontos` em ordem decrescente;
# MAGIC * Em caso de empate, ordenar por `time_id` em ordem crescente.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.1.1 Cria tabelas no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Create Table - Times
# MAGIC %sql
# MAGIC USE datacraft_catalog.cantu;
# MAGIC CREATE TABLE IF NOT EXISTS cantu.times (
# MAGIC   time_id LONG NOT NULL, 
# MAGIC   time_nome STRING NOT NULL,
# MAGIC   PRIMARY KEY(time_id)
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Create Table - Jogos
# MAGIC %sql
# MAGIC USE datacraft_catalog.cantu;
# MAGIC CREATE TABLE IF NOT EXISTS cantu.jogos (
# MAGIC   jogo_id LONG NOT NULL, 
# MAGIC   mandante_time LONG NOT NULL,
# MAGIC   visitante_time LONG NOT NULL,
# MAGIC   mandante_gols LONG NOT NULL,
# MAGIC   visitante_gols LONG NOT NULL,
# MAGIC   PRIMARY KEY(jogo_id),
# MAGIC   CONSTRAINT fk_mandante_time FOREIGN KEY (mandante_time) REFERENCES times(time_id),
# MAGIC   CONSTRAINT fk_visitante_time FOREIGN KEY (visitante_time) REFERENCES times(time_id)
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.1.2 Insere os dados nas tabelas no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Gerar dados
# 📄 DataFrame de times
df_times = spark.createDataFrame([
    (10, "Financeiro"),
    (20, "Marketing"),
    (30, "Logística"),
    (40, "TI"),
    (50, "Dados"),
], ["time_id", "time_nome"])

# 📄 DataFrame de jogos
df_jogos = spark.createDataFrame([
    (1, 30, 20, 1, 0),
    (2, 10, 20, 1, 2),
    (3, 20, 50, 2, 2),
    (4, 10, 30, 1, 0),
    (5, 30, 50, 0, 1),
], ["jogo_id", "mandante_time", "visitante_time", "mandante_gols", "visitante_gols"])

# Cria view temporária
df_times.createOrReplaceTempView('temp_times')
df_jogos.createOrReplaceTempView('temp_jogos')


# COMMAND ----------

# DBTITLE 1,Inserir dados - Times
# MAGIC %sql
# MAGIC INSERT INTO datacraft_catalog.cantu.times (
# MAGIC     time_id, time_nome
# MAGIC   )
# MAGIC SELECT
# MAGIC   time_id,
# MAGIC   time_nome
# MAGIC FROM temp_times

# COMMAND ----------

# %sql
# TRUNCATE TABLE datacraft_catalog.cantu.times

# COMMAND ----------

# DBTITLE 1,Inserir dados - Jogos
# MAGIC %sql
# MAGIC INSERT INTO datacraft_catalog.cantu.jogos (
# MAGIC     jogo_id, mandante_time, visitante_time, mandante_gols, visitante_gols
# MAGIC   )
# MAGIC   SELECT
# MAGIC     jogo_id,
# MAGIC     mandante_time,
# MAGIC     visitante_time,
# MAGIC     mandante_gols,
# MAGIC     visitante_gols
# MAGIC   FROM
# MAGIC     temp_jogos

# COMMAND ----------

# %sql
# TRUNCATE TABLE datacraft_catalog.cantu.jogos

# COMMAND ----------

# DBTITLE 1,Query - Classificação Times
# MAGIC %sql
# MAGIC WITH resultados_mandante AS (
# MAGIC     SELECT 
# MAGIC         mandante_time AS time_id,
# MAGIC         CASE 
# MAGIC             WHEN mandante_gols > visitante_gols THEN 3
# MAGIC             WHEN mandante_gols = visitante_gols THEN 1
# MAGIC             ELSE 0
# MAGIC         END AS pontos
# MAGIC     FROM datacraft_catalog.cantu.jogos
# MAGIC ),
# MAGIC resultados_visitante AS (
# MAGIC     SELECT 
# MAGIC         visitante_time AS time_id,
# MAGIC         CASE 
# MAGIC             WHEN visitante_gols > mandante_gols THEN 3
# MAGIC             WHEN visitante_gols = mandante_gols THEN 1
# MAGIC             ELSE 0
# MAGIC         END AS pontos
# MAGIC     FROM datacraft_catalog.cantu.jogos
# MAGIC ),
# MAGIC todos_resultados AS (
# MAGIC     SELECT * FROM resultados_mandante
# MAGIC     UNION ALL
# MAGIC     SELECT * FROM resultados_visitante
# MAGIC ),
# MAGIC pontuacao_por_time AS (
# MAGIC     SELECT 
# MAGIC         time_id,
# MAGIC         SUM(pontos) AS num_pontos
# MAGIC     FROM todos_resultados
# MAGIC     GROUP BY time_id
# MAGIC )
# MAGIC
# MAGIC SELECT 
# MAGIC     t.time_nome,
# MAGIC     COALESCE(p.num_pontos, 0) AS num_pontos
# MAGIC FROM datacraft_catalog.cantu.times t
# MAGIC LEFT JOIN pontuacao_por_time p ON t.time_id = p.time_id
# MAGIC ORDER BY num_pontos DESC, t.time_id ASC;

# COMMAND ----------

# MAGIC %md 
# MAGIC ### 1.2 Comissões
# MAGIC
# MAGIC A tabela `comissoes` tem a seguinte estrutura:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE comissoes (
# MAGIC     comprador VARCHAR NOT NULL,
# MAGIC     vendedor VARCHAR NOT NULL,
# MAGIC     dataPgto DATE NOT NULL,
# MAGIC     valor FLOAT NOT NULL
# MAGIC );
# MAGIC ````
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📌 Regras da Consulta
# MAGIC
# MAGIC Escreva uma query SQL que retorne a **lista de vendedores** que:
# MAGIC
# MAGIC * Receberam **pelo menos R\$ 1.024,00** em comissões;
# MAGIC * Considerando **no máximo 3 transferências** por vendedor;
# MAGIC * Ou seja, só deve aparecer na lista quem tiver até 3 registros e a soma total dos valores seja maior ou igual a R\$ 1.024,00;
# MAGIC * Vendedores com mais de 3 comissões **não devem aparecer**, mesmo que tenham recebido mais de R\$ 1.024,00;
# MAGIC * O resultado deve ser ordenado **em ordem alfabética** pelo nome do vendedor.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧪 Exemplo de Dados
# MAGIC
# MAGIC | Comprador | Vendedor | Data       | Valor    |
# MAGIC | --------- | -------- | ---------- | -------- |
# MAGIC | Leonardo  | Bruno    | 01/01/2000 | 200,00   |
# MAGIC | Leonardo  | Matheus  | 27/09/2003 | 1.024,00 |
# MAGIC | Leonardo  | Lucas    | 26/06/2006 | 512,00   |
# MAGIC | Marcos    | Lucas    | 17/12/2020 | 100,00   |
# MAGIC | Marcos    | Lucas    | 22/03/2002 | 10,00    |
# MAGIC | Cinthia   | Lucas    | 20/03/2021 | 500,00   |
# MAGIC | Mateus    | Bruno    | 02/06/2007 | 400,00   |
# MAGIC | Mateus    | Bruno    | 26/06/2006 | 400,00   |
# MAGIC | Mateus    | Bruno    | 26/06/2015 | 200,00   |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Resultado Esperado
# MAGIC
# MAGIC | Vendedor |
# MAGIC | -------- |
# MAGIC | Lucas    |
# MAGIC | Matheus  |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ℹ️ Explicação
# MAGIC
# MAGIC * **Lucas** tem 3 comissões: 512 + 100 + 500 = 1.112 ≥ 1.024 → OK ✅
# MAGIC * **Matheus** tem 1 comissão de 1.024 → OK ✅
# MAGIC * **Bruno** tem 4 comissões (mesmo somando 1.200, excede 3 transferências) → ❌
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.2.1 Cria tabelas no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Create Table - Comissões
# MAGIC %sql
# MAGIC USE datacraft_catalog.cantu;
# MAGIC CREATE TABLE IF NOT EXISTS cantu.comissoes (
# MAGIC   comissao_id LONG NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
# MAGIC   comprador STRING NOT NULL,
# MAGIC   vendedor STRING NOT NULL,
# MAGIC   dataPgto DATE NOT NULL,
# MAGIC   valor DOUBLE NOT NULL,
# MAGIC   PRIMARY KEY(comissao_id)
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.2.2 Insere os dados na tabela no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Gerar dados
# Define o schema
schema = StructType([
    StructField("comprador", StringType(), False),
    StructField("vendedor", StringType(), False),
    StructField("dataPgto", DateType(), False),
    StructField("valor", FloatType(), False)
])

# Dados da tabela comissoes
dados_comissoes = [
    ("Leonardo", "Bruno",   datetime(2000, 1, 1),   200.00),
    ("Leonardo", "Matheus",datetime(2003, 9, 27), 1024.00),
    ("Leonardo", "Lucas",  datetime(2006, 6, 26),  512.00),
    ("Marcos",   "Lucas",  datetime(2020, 12, 17), 100.00),
    ("Marcos",   "Lucas",  datetime(2002, 3, 22),   10.00),
    ("Cinthia",  "Lucas",  datetime(2021, 3, 20),  500.00),
    ("Mateus",   "Bruno",  datetime(2007, 6, 2),   400.00),
    ("Mateus",   "Bruno",  datetime(2006, 6, 26),  400.00),
    ("Mateus",   "Bruno",  datetime(2015, 6, 26),  200.00),
]

# Cria o DataFrame
df_comissoes = spark.createDataFrame(dados_comissoes, schema)

# Cria view temporária
df_comissoes.createOrReplaceTempView('temp_comissoes')


# COMMAND ----------

# DBTITLE 1,Inserir dados - Comissões
# MAGIC %sql
# MAGIC INSERT INTO datacraft_catalog.cantu.comissoes (
# MAGIC     comprador, vendedor, dataPgto, valor
# MAGIC   )
# MAGIC SELECT
# MAGIC   comprador,
# MAGIC   vendedor,
# MAGIC   dataPgto,
# MAGIC   valor
# MAGIC FROM temp_comissoes

# COMMAND ----------

# DBTITLE 1,Query - Lista de Vendedores
# MAGIC %sql
# MAGIC WITH ranked_comissoes AS (
# MAGIC     SELECT
# MAGIC         vendedor,
# MAGIC         valor,
# MAGIC         ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS rn
# MAGIC     FROM datacraft_catalog.cantu.comissoes
# MAGIC ),
# MAGIC top3_comissoes AS (
# MAGIC     SELECT
# MAGIC         vendedor,
# MAGIC         valor
# MAGIC     FROM ranked_comissoes
# MAGIC     WHERE rn <= 3
# MAGIC ),
# MAGIC vendedores_qualificados AS (
# MAGIC     SELECT
# MAGIC         vendedor,
# MAGIC         COUNT(*) AS qtd_transferencias,
# MAGIC         SUM(valor) AS total_recebido
# MAGIC     FROM top3_comissoes
# MAGIC     GROUP BY vendedor
# MAGIC     HAVING qtd_transferencias <= 3 AND total_recebido >= 1024
# MAGIC )
# MAGIC SELECT vendedor
# MAGIC FROM vendedores_qualificados
# MAGIC ORDER BY vendedor ASC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.3 Organização Empresarial
# MAGIC ---
# MAGIC ## 📋 Estrutura da Tabela
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE colaboradores (
# MAGIC     id INTEGER NOT NULL,
# MAGIC     nome VARCHAR NOT NULL,
# MAGIC     salario INTEGER NOT NULL,
# MAGIC     lider_id INTEGER,
# MAGIC     UNIQUE(id)
# MAGIC );
# MAGIC ````
# MAGIC
# MAGIC > *A coluna `lider` foi ajustada para receber dados nulos, por conta dos requisitos da questão.*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧠 Desafio
# MAGIC
# MAGIC Para cada funcionário, retornar:
# MAGIC
# MAGIC * `id` do funcionário;
# MAGIC * `id` do **chefe indireto** que:
# MAGIC
# MAGIC   * Ganha pelo menos o **dobro do salário** do funcionário;
# MAGIC   * É um **chefe indireto** (ou seja, chefe do chefe, ou superior a isso);
# MAGIC * Se **nenhum chefe indireto** atender a condição, o valor deve ser `NULL`.
# MAGIC
# MAGIC ### 🧩 Definições
# MAGIC
# MAGIC * Um funcionário A é **chefe indireto** de B se:
# MAGIC
# MAGIC   * A é o chefe do chefe de B, ou do chefe do chefe do chefe... e assim por diante;
# MAGIC * Não existem ciclos na hierarquia (garantido pelo enunciado);
# MAGIC * O resultado deve ser ordenado por `id` do funcionário de forma crescente.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 💡 Exemplo de Funcionários
# MAGIC
# MAGIC - Diagrama Hierárquico:
# MAGIC
# MAGIC ```planText
# MAGIC Marcos (20) - $ 10.000
# MAGIC └── Leonardo (10) - $ 4.500
# MAGIC     ├── Bruno (50) - $ 3.000 
# MAGIC     │   ├── Helen  (40) - $ 1.500
# MAGIC     │   └── Wilian (30) - $ 1.501
# MAGIC     └── Mateus (70) - $ 1.500
# MAGIC         └── Cinthia (60) $ 2.000
# MAGIC ```
# MAGIC
# MAGIC | Id | Nome     | Salário | Lider\_Id |
# MAGIC | -- | -------- | ------- | --------- |
# MAGIC | 40 | Helen    | 1500    | 50        |
# MAGIC | 50 | Bruno    | 3000    | 10        |
# MAGIC | 10 | Leonardo | 4500    | 20        |
# MAGIC | 20 | Marcos   | 10000   | NULL      |
# MAGIC | 70 | Mateus   | 1500    | 10        |
# MAGIC | 60 | Cinthia  | 2000    | 70        |
# MAGIC | 30 | Wilian   | 1501    | 50        |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Resultado Esperado
# MAGIC
# MAGIC | funcionario\_id | chefe\_indireto\_id |
# MAGIC | --------------- | ------------------- |
# MAGIC | 10              | NULL                |
# MAGIC | 20              | NULL                |
# MAGIC | 30              | 10                  |
# MAGIC | 40              | 10                  |
# MAGIC | 50              | 10                  |
# MAGIC | 60              | 10                  |
# MAGIC | 70              | 10                  |
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.3.1 Cria tabelas no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Create Table - Colaboradores
# MAGIC %sql
# MAGIC USE datacraft_catalog.cantu;
# MAGIC CREATE TABLE IF NOT EXISTS cantu.colaboradores (
# MAGIC   id LONG NOT NULL, 
# MAGIC   nome STRING NOT NULL,
# MAGIC   salario DOUBLE NOT NULL,
# MAGIC   lider_id LONG,
# MAGIC   PRIMARY KEY(id)
# MAGIC );

# COMMAND ----------

# %sql
# DROP TABLE cantu.colaboradores

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.1.2 Insere os dados nas tabelas no Databricks - com Unity Catalog

# COMMAND ----------

# DBTITLE 1,Gerar dados
# Define o schema
schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("nome", StringType(), False),
    StructField("salario", DoubleType(), False),
    StructField("lider_id", IntegerType(), True)
])

# Dados conforme a tabela da imagem
dados_colaboradores = [
    (40, "Helen",    1500, 50),
    (50, "Bruno",    3000, 10),
    (10, "Leonardo", 4500, 20),
    (20, "Marcos",  10000, None),
    (70, "Mateus",   1500, 10),
    (60, "Cinthia",  2000, 70),
    (30, "Wilian",   1501, 50),
]

# Cria o DataFrame
df_colaboradores = spark.createDataFrame(dados_colaboradores, schema)

# Exibe o conteúdo
df_colaboradores.createOrReplaceTempView('temp_colaboradores')


# COMMAND ----------

# DBTITLE 1,Inserir dados - Colaboradores
# MAGIC %sql
# MAGIC INSERT INTO datacraft_catalog.cantu.colaboradores (
# MAGIC     id, nome, salario, lider_id
# MAGIC   )
# MAGIC SELECT
# MAGIC   id,
# MAGIC   nome,
# MAGIC   salario,
# MAGIC   lider_id
# MAGIC FROM temp_colaboradores

# COMMAND ----------

# DBTITLE 1,Query - Organização Empresarial
# MAGIC %sql
# MAGIC WITH chefe_direto AS (
# MAGIC   -- Retorna o chefe direto de cada funcionário
# MAGIC   SELECT
# MAGIC     id,
# MAGIC     nome,
# MAGIC     salario,
# MAGIC     lider_id as id_chefe_direto
# MAGIC   FROM datacraft_catalog.cantu.colaboradores
# MAGIC ), chefe_indireto AS (
# MAGIC   -- Retorna o chefe indireto de cada funcionário
# MAGIC   SELECT
# MAGIC     chefe_direto.*,
# MAGIC     chefe.nome as nome_chefe_direto,
# MAGIC     chefe.salario as salario_chefe_direto,
# MAGIC     chefe.lider_id as id_chefe_indireto
# MAGIC   FROM chefe_direto
# MAGIC   LEFT JOIN datacraft_catalog.cantu.colaboradores AS chefe ON chefe.id = chefe_direto.id_chefe_direto
# MAGIC )
# MAGIC -- retorna o id_funcionario e o id_do_chefe_indireto
# MAGIC SELECT
# MAGIC   id as id_funcionario,
# MAGIC   id_chefe_indireto
# MAGIC FROM chefe_indireto
# MAGIC ORDER BY 1
