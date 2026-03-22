import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use("Agg")  # salva sem abrir janela
sns.set_theme(style="whitegrid", palette="muted")

# Caminhos
PARQUET      = "data/silver/dataset_clean.parquet"
GRAFICOS_DIR = "data/silver/graficos"
RELATORIO    = "data/silver/relatorio_graficos.md"

os.makedirs(GRAFICOS_DIR, exist_ok=True)


# Utilitários gerais e salvando em png
def salvar(nome, titulo):
    caminho = os.path.join(GRAFICOS_DIR, nome)
    plt.tight_layout()
    plt.savefig(caminho, dpi=100)
    plt.close()
    print(f"  Salvo: {caminho}")
    return nome, titulo


# Leitura do Parquet
print("Lendo Parquet...")
df = pd.read_parquet(PARQUET)

# Amostra para gráficos de dispersão (evita lentidão)
amostra = df.sample(5000, random_state=42)

graficos = []


# Gráfico 1 - Distribuição de horas de jogo diárias
fig, ax = plt.subplots(figsize=(9, 4))
sns.histplot(df["daily_gaming_hours"], bins=40, kde=True, ax=ax, color="#5DCAA5")
ax.set_title("Distribuição de horas de jogo diárias")
ax.set_xlabel("Horas por dia")
ax.set_ylabel("Frequência")
graficos.append(salvar("g1_distribuicao_horas_jogo.png",
                        "Distribuição de horas de jogo diárias"))


# Gráfico 2 - Score de ansiedade por gênero
fig, ax = plt.subplots(figsize=(9, 4))
sns.boxplot(data=df, x="gender", y="anxiety_score", ax=ax, palette="Set2")
ax.set_title("Score de ansiedade por gênero")
ax.set_xlabel("Gênero")
ax.set_ylabel("Score de ansiedade")
graficos.append(salvar("g2_ansiedade_por_genero.png",
                        "Score de ansiedade por gênero"))


# Gráfico 3 - Horas de jogo vs depressão
fig, ax = plt.subplots(figsize=(9, 4))
sns.scatterplot(data=amostra, x="daily_gaming_hours", y="depression_score",
                alpha=0.4, s=15, ax=ax, color="#D85A30")
ax.set_title("Horas de jogo diárias vs score de depressão")
ax.set_xlabel("Horas de jogo por dia")
ax.set_ylabel("Score de depressão")
graficos.append(salvar("g3_jogo_vs_depressao.png",
                        "Horas de jogo diárias vs score de depressão"))


# Gráfico 4 - Distribuição do nível de vício
fig, ax = plt.subplots(figsize=(9, 4))
sns.histplot(df["addiction_level"], bins=30, kde=True, ax=ax, color="#378ADD")
ax.set_title("Distribuição do nível de vício em jogos")
ax.set_xlabel("Nível de vício")
ax.set_ylabel("Frequência")
graficos.append(salvar("g4_nivel_vicio.png",
                        "Distribuição do nível de vício em jogos"))


# Gráfico 5 - Horas de sono vs felicidade
fig, ax = plt.subplots(figsize=(9, 4))
sns.scatterplot(data=amostra, x="sleep_hours", y="happiness_score",
                alpha=0.4, s=15, ax=ax, color="#EF9F27")
ax.set_title("Horas de sono vs score de felicidade")
ax.set_xlabel("Horas de sono")
ax.set_ylabel("Score de felicidade")
graficos.append(salvar("g5_sono_vs_felicidade.png",
                        "Horas de sono vs score de felicidade"))


# Geração do Markdown
print("\nGerando relatório Markdown...")

linhas = ["# Relatório de Gráficos — Camada Silver\n\n"]
linhas.append(f"Dataset: `{PARQUET}`  \n")
linhas.append(f"Total de linhas: {len(df):,}  \n")
linhas.append(f"Gráficos de dispersão usam amostra de 5.000 linhas.\n\n")

for i, (arquivo, titulo) in enumerate(graficos, 1):
    linhas.append(f"## Gráfico {i} — {titulo}\n\n")
    linhas.append(f"![{titulo}](graficos/{arquivo})\n\n")

with open(RELATORIO, "w", encoding="utf-8") as f:
    f.writelines(linhas)

print(f"Relatório salvo em: {RELATORIO}")
print("Gráficos concluídos!")