import os
import pandas as pd

# Caminhos
RAW_PATH   = "data/raw/gaming_mental_health_database.csv"
SILVER_DIR = "data/silver"
PARQUET    = os.path.join(SILVER_DIR, "dataset_clean.parquet")

os.makedirs(SILVER_DIR, exist_ok=True)


# Verificando o database, não é necessário realizar esta etapa, mas é requisitado na atividade
def padronizar_colunas(df):
    df.columns = (df.columns
                    .str.strip()
                    .str.lower()
                    .str.replace(r"[\s\-]+", "_", regex=True))
    return df


def remover_duplicatas(df):
    antes = len(df)
    df = df.drop_duplicates()
    removidas = antes - len(df)
    print(f"  Duplicatas removidas : {removidas:,}")
    return df


def converter_tipos(df):

    # Colunas binárias → boolean
    colunas_bool = ["esports_interest", "headset_usage", "parental_supervision"]
    for col in colunas_bool:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    # Coluna categórica
    if "gender" in df.columns:
        df["gender"] = df["gender"].astype("category")

    return df


def tratar_nulos(df):
    """
    Trata valores ausentes:
    - Colunas numéricas: imputa com a mediana
    - Colunas de texto: imputa com 'unknown'
    Exibe quantos nulos foram tratados.
    """
    nulos_antes = df.isnull().sum().sum()

    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("unknown")

    nulos_depois = df.isnull().sum().sum()
    print(f"  Nulos tratados       : {nulos_antes - nulos_depois:,}")
    return df


#   Executa todas as etapas de limpeza em sequência
def limpar(df):

    print("\nIniciando limpeza...")
    df = padronizar_colunas(df)
    df = remover_duplicatas(df)
    df = converter_tipos(df)
    df = tratar_nulos(df)
    print(f"  Shape final          : {df.shape[0]:,} linhas × {df.shape[1]} colunas")
    return df


if __name__ == "__main__":
    print("Lendo CSV...")
    df = pd.read_csv(RAW_PATH, low_memory=False)

    df = limpar(df)

    df.to_parquet(PARQUET, index=False)
    print(f"\nParquet salvo em: {PARQUET}")
    print("Limpeza concluída!")