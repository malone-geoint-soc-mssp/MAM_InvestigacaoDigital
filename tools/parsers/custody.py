import hashlib
import os
import psycopg2
from dotenv import load_dotenv

# Carregar variáveis de ambiente do ficheiro .env oculto
load_dotenv()

def calcular_hash_sha256(caminho_ficheiro: str) -> tuple[str, int]:
    """
    Lê um ficheiro em blocos binários para evitar estouro de memória (RAM)
    e gera o hash SHA-256 e o tamanho em bytes.
    """
    sha256_hash = hashlib.sha256()
    tamanho_bytes = 0

    with open(caminho_ficheiro, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            sha256_hash.update(bloco)
            tamanho_bytes += len(bloco)

    return sha256_hash.hexdigest(), tamanho_bytes

def registar_custodia(caminho_ficheiro: str, investigador: str = "Eng.º Malone Manuel"):
    """
    Calcula a integridade do ficheiro e insere o registo na tabela tb_cadeia_custodia.
    """
    if not os.path.exists(caminho_ficheiro):
        raise FileNotFoundError(f"Ficheiro de evidência não encontrado: {caminho_ficheiro}")

    hash_val, tamanho = calcular_hash_sha256(caminho_ficheiro)
    nome_ficheiro = os.path.basename(caminho_ficheiro)

    # Conectar ao banco PostgreSQL usando as variáveis de ambiente na porta 5435
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5435")
    )
    cursor = conn.cursor()

    sql = """
    INSERT INTO tb_cadeia_custodia (nome_ficheiro, caminho_relativo, hash_sha256, tamanho_bytes, investigador)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, coletado_em;
    """

    cursor.execute(sql, (nome_ficheiro, caminho_ficheiro, hash_val, tamanho, investigador))
    custodia_id, coletado_em = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()

    print(f"[+] Custódia Registada com Sucesso!")
    print(f"    - ID da Custódia: {custodia_id}")
    print(f"    - Ficheiro: {nome_ficheiro}")
    print(f"    - SHA-256: {hash_val}")
    print(f"    - Tamanho: {tamanho} bytes")
    print(f"    - Data/Hora: {coletado_em}")

if __name__ == "__main__":
    print("Módulo de Custódia ISO/IEC 27037 Carregado.")