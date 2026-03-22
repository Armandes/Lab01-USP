import os
from datetime import datetime

# Caminhos
RAW_DIR  = "data/raw"
SOURCE   = os.path.join(RAW_DIR, "gaming_mental_health_database.csv")
LOG_FILE = os.path.join(RAW_DIR, "ingestao_log.txt")


def ingerir_bronze():
    # Verifica se o CSV tá na pasta correta
    if not os.path.exists(SOURCE):
        raise FileNotFoundError(f"Arquivo não encontrado: {SOURCE}")

    # Coleta metadados
    total_linhas = sum(1 for _ in open(SOURCE, encoding="utf-8")) - 1
    tamanho_mb   = round(os.path.getsize(SOURCE) / (1024 * 1024), 2)
    data_ingestao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Exibe e salva o log
    log = (
        f"arquivo       : {SOURCE}\n"
        f"data_ingestao : {data_ingestao}\n"
        f"tamanho_mb    : {tamanho_mb}\n"
        f"total_linhas  : {total_linhas}\n"
        f"status        : RAW - sem alteracoes\n"
    )

    print("\n=== Relatório inicial ===\n" + log)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(log)

    print(f"Log salvo em: {LOG_FILE}")


if __name__ == "__main__":
    ingerir_bronze()