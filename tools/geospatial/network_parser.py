import os
import re
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def extrair_metadados_log(caminho_ficheiro: str) -> dict:
    """
    Lê o ficheiro de log de tráfego de rede e extrai os campos usando Expressões Regulares (RegEx).
    """
    with open(caminho_ficheiro, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Padrões de extração por Regex
    ip_src = re.search(r"SRC_IP=([^\s|]+)", conteudo)
    ip_dst = re.search(r"DST_IP=([^\s|]+)", conteudo)
    email = re.search(r"USER_EMAIL=([^\s|]+)", conteudo)
    action = re.search(r"ACTION=([^\s|]+)", conteudo)
    user_agent = re.search(r'USER_AGENT="([^"]+)"', conteudo)

    return {
        "src_ip": ip_src.group(1) if ip_src else None,
        "dst_ip": ip_dst.group(1) if ip_dst else None,
        "email": email.group(1) if email else None,
        "action": action.group(1) if action else None,
        "user_agent": user_agent.group(1) if user_agent else None,
        "raw_log": conteudo.strip()
    }

def processar_e_geolocalizar(custodia_id: int, caminho_ficheiro: str):
    """
    Processa os metadados do log, simula/resolve a geolocalização do IP malicioso
    e regista a evidência vetorial no PostGIS.
    """
    dados = extrair_metadados_log(caminho_ficheiro)

    # Simulação de Geolocalização IP (DST_IP 45.142.214.100 -> Amsterdão / Holanda)
    # Em produção, este bloco pode consumir a API MaxMind GeoIP2 ou ipinfo.io
    latitude = 52.3676
    longitude = 4.9041

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5435")
    )
    cursor = conn.cursor()

    sql = """
    INSERT INTO tb_evidencias_geo (
        custodia_id, origem_evidencia, tipo_vetor, ip_address, 
        latitude, longitude, geom, detalhes_tecnicos
    )
    VALUES (
        %s, %s, %s, %s, 
        %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s::jsonb
    )
    RETURNING id;
    """

    detalhes_json = f"""{{
        "src_ip": "{dados['src_ip']}",
        "dst_ip": "{dados['dst_ip']}",
        "user_email": "{dados['email']}",
        "action": "{dados['action']}",
        "user_agent": "{dados['user_agent']}"
    }}"""

    cursor.execute(sql, (
        custodia_id,
        "network_traffic.log",
        "EXFILTRATION_LOG",
        dados['dst_ip'],
        latitude,
        longitude,
        longitude,  # ST_MakePoint aceita (longitude, latitude)
        latitude,
        detalhes_json
    ))

    evidencia_geo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    print(f"[+] Evidência Geoespacial Registada com Sucesso!")
    print(f"    - ID GeoINT: {evidencia_geo_id}")
    print(f"    - Custódia ID: {custodia_id}")
    print(f"    - Target IP: {dados['dst_ip']}")
    print(f"    - Coordenadas (WGS84): Lat {latitude}, Lon {longitude}")
    print(f"    - Geometria PostGIS: Point(4326) Gerado.")

if __name__ == "__main__":
    print("Módulo de Parse e Geolocalização GeoINT Carregado.")