import pandas as pd

# Configuração e leitura
SOURCE = "data/raw/gaming_mental_health_database.csv"
print("Lendo dataset...\n")
df = pd.read_csv(SOURCE, low_memory=False)

numericas = df.select_dtypes(include="number")
categoricas = df.select_dtypes(include="object")

# Visão geral
print("=" * 45)
print("VISÃO GERAL DO DATASET")
print("=" * 45)
print(f"  Linhas             : {df.shape[0]:,}")
print(f"  Colunas            : {df.shape[1]}")
print(f"  Células totais     : {df.size:,}")
print(f"  Colunas numéricas  : {len(numericas.columns)}")
print(f"  Colunas categóricas: {len(categoricas.columns)}")
print(f"  Duplicatas         : {df.duplicated().sum():,}")
print(f"  Nulos totais       : {df.isnull().sum().sum():,}")
print(f"  Memória (MB)       : {df.memory_usage(deep=True).sum() / 1024**2:.2f}")

# Tipos de colunas
print("\n" + "=" * 45)
print("TIPOS DE COLUNAS")
print("=" * 45)
for col, dtype in df.dtypes.items():
    nulos = df[col].isnull().sum()
    print(f"  {col:<35} {str(dtype):<10} nulos: {nulos}")

# Estatísticas descritivas (numéricas)
print("\n" + "=" * 45)
print("ESTATÍSTICAS DESCRITIVAS — NUMÉRICAS")
print("=" * 45)
stats = pd.DataFrame({
    "média"        : numericas.mean(),
    "mediana"      : numericas.median(),
    "desvio_pad"   : numericas.std(),
    "variância"    : numericas.var(),
    "mínimo"       : numericas.min(),
    "máximo"       : numericas.max(),
    "amplitude"    : numericas.max() - numericas.min(),
    "q1 (25%)"     : numericas.quantile(0.25),
    "q3 (75%)"     : numericas.quantile(0.75),
    "IQR"          : numericas.quantile(0.75) - numericas.quantile(0.25),
    "assimetria"   : numericas.skew(),
    "curtose"      : numericas.kurt(),
    "nulos"        : numericas.isnull().sum(),
}).round(2)

print(stats.to_string())

# Estatísticas descritivas (categóricas)
if not categoricas.empty:
    print("\n" + "=" * 45)
    print("ESTATÍSTICAS DESCRITIVAS — CATEGÓRICAS")
    print("=" * 45)
    for col in categoricas.columns:
        print(f"\n  Coluna: {col}")
        print(f"    Valores únicos : {df[col].nunique()}")
        print(f"    Mais frequente : {df[col].mode()[0]} ({df[col].value_counts().iloc[0]:,} ocorrências)")
        print(f"    Menos frequente: {df[col].value_counts().index[-1]} ({df[col].value_counts().iloc[-1]:,} ocorrências)")
        print(f"    Distribuição:")
        for valor, contagem in df[col].value_counts().items():
            pct = contagem / len(df) * 100
            print(f"      {valor:<20} {contagem:>10,}  ({pct:.1f}%)")

# Correlações mais altas com saúde mental
print("\n" + "=" * 45)
print("TOP 10 CORRELAÇÕES COM ANXIETY_SCORE")
print("=" * 45)
corr = numericas.corr()["anxiety_score"].drop("anxiety_score").abs().sort_values(ascending=False)
for col, val in corr.head(10).items():
    print(f"  {col:<35} {val:.4f}")

print("\n" + "=" * 45)
print("TOP 10 CORRELAÇÕES COM DEPRESSION_SCORE")
print("=" * 45)
corr2 = numericas.corr()["depression_score"].drop("depression_score").abs().sort_values(ascending=False)
for col, val in corr2.head(10).items():
    print(f"  {col:<35} {val:.4f}")
