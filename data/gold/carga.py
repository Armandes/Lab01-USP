"""
Entrada:
    - data/silver/dataset_clean.parquet

Saídas (tabelas no PostgreSQL):
    - dim_jogador        (perfil demográfico)
    - dim_habitos        (hábitos de jogo e saúde)
    - dim_comportamento  (comportamento online)
    - dim_social         (vida social)
    - fato_saude_mental  (métricas de saúde mental) -> Única tabela fato no esquema


Resumo do Star Schema:
Esse esquema divide as tabelas através de conceitos fato e dimensão.
*As tabelas criadas "dim_..." são dimensão e a "fato_..." a tabela fato.
Tabela fato -> métricas
Tabelas dimensão -> Dão contexto às métricas
Essas tabelas vão se relacionar através do player_id nessa parte.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Configuração e leitura
load_dotenv()
PARQUET = "data/silver/dataset_clean.parquet"
DB_URL  = os.getenv("DATABASE_URL",
          "postgresql://postgres:senha@localhost:5432/lab01")


def criar_engine():
    engine = create_engine(DB_URL)
    print("Conexão com PostgreSQL estabelecida!")
    return engine

# Carrega um DataFrame como tabela no PostgreSQL.
def carregar_tabela(df, nome, engine):
    df.to_sql(nome, engine, if_exists="replace",
              index=False, method="multi", chunksize=10000)
    print(f"  {nome:<25} {len(df):>10,} linhas carregadas")

# Divide o parquet em tabelas dimensões e fato de acordo com o modelo star schema
def modelar_e_carregar(df, engine):

    # Cria um ID único por linha (representa cada jogador/registro)
    df = df.reset_index(drop=True)
    df["player_id"] = df.index + 1

    # Dimensões

    dim_jogador = df[[
        "player_id", "age", "gender", "income", "bmi"
    ]]

    dim_habitos = df[[
        "player_id", "daily_gaming_hours", "weekly_sessions",
        "years_gaming", "sleep_hours", "caffeine_intake",
        "exercise_hours", "weekend_gaming_hours",
        "screen_time_total", "streaming_hours"
    ]]

    dim_comportamento = df[[
        "player_id", "multiplayer_ratio", "toxic_exposure",
        "violent_games_ratio", "mobile_gaming_ratio",
        "night_gaming_ratio", "esports_interest",
        "headset_usage", "microtransactions_spending",
        "competitive_rank", "internet_quality"
    ]]

    dim_social = df[[
        "player_id", "friends_gaming_count", "online_friends",
        "social_interaction_score", "relationship_satisfaction",
        "loneliness_score", "parental_supervision"
    ]]

    # Tabela fato
    fato_saude_mental = df[[
        "player_id",
        "stress_level", "anxiety_score", "depression_score",
        "addiction_level", "happiness_score", "aggression_score",
        "academic_performance", "work_productivity",
        "eye_strain_score", "back_pain_score"
    ]]

    # Carga
    print("\nCarregando tabelas no PostgreSQL...")
    carregar_tabela(dim_jogador,       "dim_jogador",       engine)
    carregar_tabela(dim_habitos,       "dim_habitos",       engine)
    carregar_tabela(dim_comportamento, "dim_comportamento", engine)
    carregar_tabela(dim_social,        "dim_social",        engine)
    carregar_tabela(fato_saude_mental, "fato_saude_mental", engine)


if __name__ == "__main__":
    print("Lendo Parquet...")
    df = pd.read_parquet(PARQUET)
    print(f"Shape: {df.shape[0]:,} linhas × {df.shape[1]} colunas")

    engine = criar_engine()
    modelar_e_carregar(df, engine)

    print("\nCamada Gold carregada com sucesso!")