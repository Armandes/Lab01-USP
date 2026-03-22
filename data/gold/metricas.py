"""
Objetivo: Responder 5 perguntas (descritas em cada operação)
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configuração e leitura
load_dotenv()
DB_URL = os.getenv("DATABASE_URL",
         "postgresql://postgres:senha@localhost:5432/lab01")

engine = create_engine(DB_URL)

# Embelezar o resultado
def executar(titulo, sql):
    print(f"\n{'==================================================================='}")
    print(f" {titulo}")
    print('===================================================================')
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)
    print(df.to_string(index=False))
    return df


# Qual faixa de horas de jogo diárias está associada ao maior score médio de ansiedade?
executar(
    "M1 — Ansiedade média por faixa de horas de jogo",
    """
    SELECT
        CASE
            WHEN h.daily_gaming_hours < 2  THEN '< 2h'
            WHEN h.daily_gaming_hours < 4  THEN '2–4h'
            WHEN h.daily_gaming_hours < 6  THEN '4–6h'
            WHEN h.daily_gaming_hours < 8  THEN '6–8h'
            ELSE '> 8h'
        END AS faixa_horas,
        COUNT(*) AS total_jogadores,
        ROUND(AVG(f.anxiety_score)::numeric, 2)   AS ansiedade_media,
        ROUND(AVG(f.depression_score)::numeric, 2) AS depressao_media
    FROM fato_saude_mental f
    JOIN dim_habitos h ON f.player_id = h.player_id
    GROUP BY faixa_horas
    ORDER BY ansiedade_media DESC
    """
)


# Qual gênero apresenta maior nível médio de vício em jogos?
executar(
    "M2 — Nível de vício médio por gênero",
    """
    SELECT
        j.gender,
        COUNT(*)                                   AS total,
        ROUND(AVG(f.addiction_level)::numeric, 2)  AS vicio_medio,
        ROUND(AVG(f.happiness_score)::numeric, 2)  AS felicidade_media,
        ROUND(AVG(f.anxiety_score)::numeric, 2)    AS ansiedade_media
    FROM fato_saude_mental f
    JOIN dim_jogador j ON f.player_id = j.player_id
    GROUP BY j.gender
    ORDER BY vicio_medio DESC
    """
)


# Jogadores com alta exposição a conteúdo tóxico têm maior score de agressividade?
executar(
    "M3 — Agressividade vs exposição a conteúdo tóxico",
    """
    SELECT
        CASE
            WHEN c.toxic_exposure < 0.33 THEN 'Baixa'
            WHEN c.toxic_exposure < 0.66 THEN 'Média'
            ELSE 'Alta'
        END                                          AS nivel_toxicidade,
        COUNT(*)                                     AS total,
        ROUND(AVG(f.aggression_score)::numeric, 2)   AS agressividade_media,
        ROUND(AVG(f.depression_score)::numeric, 2)   AS depressao_media
    FROM fato_saude_mental f
    JOIN dim_comportamento c ON f.player_id = c.player_id
    GROUP BY nivel_toxicidade
    ORDER BY agressividade_media DESC
    """
)


# Jogadores que dormem bem (ou seja, sleep_hours >= 7h) têm melhor saúde mental?
executar(
    "M4 — Saúde mental por qualidade de sono",
    """
    SELECT
        CASE
            WHEN h.sleep_hours >= 7 THEN 'Sono adequado (>= 7h)'
            ELSE 'Sono insuficiente (< 7h)'
        END AS qualidade_sono,
        COUNT(*) AS total,
        ROUND(AVG(f.anxiety_score)::numeric, 2) AS ansiedade_media,
        ROUND(AVG(f.depression_score)::numeric, 2) AS depressao_media,
        ROUND(AVG(f.happiness_score)::numeric, 2) AS felicidade_media
    FROM fato_saude_mental f
    INNER JOIN dim_habitos h ON f.player_id = h.player_id
    GROUP BY qualidade_sono
    ORDER BY felicidade_media DESC
    """
)


# Jogadores com mais amigos online se sentem menos solitários?
executar(
    "M5 — Solidão vs quantidade de amigos online",
    """
    SELECT
        CASE
            WHEN s.online_friends < 50  THEN '< 50 amigos'
            WHEN s.online_friends < 150 THEN '50–150 amigos'
            WHEN s.online_friends < 300 THEN '150–300 amigos'
            ELSE '> 300 amigos'
        END AS faixa_amigos,
        COUNT(*) AS total,
        ROUND(AVG(s.loneliness_score)::numeric, 2) AS solidao_media,
        ROUND(AVG(f.happiness_score)::numeric, 2) AS felicidade_media
    FROM fato_saude_mental f
    INNER JOIN dim_social s ON f.player_id = s.player_id
    GROUP BY faixa_amigos
    ORDER BY solidao_media ASC
    """
)

print("\nMétricas finalizadas!")