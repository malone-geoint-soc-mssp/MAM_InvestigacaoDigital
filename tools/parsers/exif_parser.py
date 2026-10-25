import os
import psycopg2
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from dotenv import load_dotenv

# Importação direta do mesmo diretório
try:
    from tools.parsers.custody import calcular_hash_sha256
except ModuleNotFoundError:
    from custody import calcular_hash_sha256

load_dotenv()

def converter_para_graus_decimais(coordenada, ref):
    """
    Converte coordenadas EXIF (Graus, Minutos, Segundos) para Graus Decimais (WGS84).
    """
    d, m, s = coordenada
    graus = float(d) + float(m) / 60.0 + float(s) / 3600.0
    if ref in ['S', 'W']:
        graus = -graus
    return graus

def extrair_exif_gps(caminho_imagem: str) -> dict:
    """
    Extrai metadados EXIF e converte a tag GPS para latitude e longitude decimais.
    """
    imagem = Image.open(caminho_imagem)
    exif_data = imagem._getexif()
    
    if not exif_data:
        return {}

    metadados = {}
    gps_info = {}

    for tag_id, value in exif_data.items():
        nome_tag = TAGS.get(tag_id, tag_id)
        if nome_tag == "GPSInfo":
            for key in value:
                sub_tag = GPSTAGS.get(key, key)
                gps_info[sub_tag] = value[key]
        else:
            if isinstance(value, (str, int, float)):
                metadados[nome_tag] = value

    lat = None
    lon = None

    if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
        lat = converter_para_graus_decimais(gps_info["GPSLatitude"], gps_info["GPSLatitudeRef"])
    if "GPSLongitude" in gps_info and "GPSLongitudeRef" in gps_info:
        lon = converter_para_graus_decimais(gps_info["GPSLongitude"], gps_info["GPSLongitudeRef"])

    metadados["latitude"] = lat
    metadados["longitude"] = lon
    return metadados

def processar_evidencia_imagem(caminho_imagem: str, investigador: str = "Eng.º Malone Manuel"):
    """
    Executa a cadeia de custódia ISO/IEC 27037 e ingere as coordenadas EXIF no PostGIS.
    """
    if not os.path.exists(caminho_imagem):
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")

    print("[*] A registar custódia da imagem...")
    hash_val, tamanho = calcular_hash_sha256(caminho_imagem)
    nome_ficheiro = os.path.basename(caminho_imagem)

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5435")
    )
    cursor = conn.cursor()

    # Inserção resiliente para tratar re-execuções sem violar a regra ISO/IEC 27037
    sql_custodia = """
    INSERT INTO tb_cadeia_custodia (nome_ficheiro, caminho_relativo, hash_sha256, tamanho_bytes, investigador)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (hash_sha256) 
    DO UPDATE SET nome_ficheiro = EXCLUDED.nome_ficheiro
    RETURNING id;
    """
    cursor.execute(sql_custodia, (nome_ficheiro, caminho_imagem, hash_val, tamanho, investigador))
    custodia_id = cursor.fetchone()[0]
    cursor.execute(sql_custodia, (nome_ficheiro, caminho_imagem, hash_val, tamanho, investigador))
    custodia_id = cursor.fetchone()[0]

    # Extrair EXIF e Gravar no PostGIS (tb_evidencias_geo)
    exif = extrair_exif_gps(caminho_imagem)
    lat = exif.get("latitude")
    lon = exif.get("longitude")
    dispositivo = str(exif.get("Make", "Desconhecido")) + " " + str(exif.get("Model", ""))

    if lat and lon:
        sql_geo = """
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
            "camera_make": "{exif.get('Make', 'N/A')}",
            "camera_model": "{exif.get('Model', 'N/A')}",
            "software": "{exif.get('Software', 'N/A')}",
            "datetime_original": "{exif.get('DateTimeOriginal', 'N/A')}"
        }}"""

        cursor.execute(sql_geo, (
            custodia_id,
            nome_ficheiro,
            "EXIF_IMAGE_GPS",
            "N/A",
            lat,
            lon,
            lon,
            lat,
            detalhes_json
        ))
        geo_id = cursor.fetchone()[0]
        conn.commit()

        print(f"[+] Imagem Processada e Geolocalizada com Sucesso!")
        print(f"    - Custódia ID: {custodia_id}")
        print(f"    - GeoINT ID: {geo_id}")
        print(f"    - Dispositivo: {dispositivo}")
        print(f"    - Coordenadas GPS EXIF: Lat {lat}, Lon {lon}")
    else:
        conn.commit()
        print(f"[!] Custódia ID {custodia_id} gravada, mas a imagem não contém coordenadas GPS EXIF.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Módulo de Parse EXIF Forense Carregado.")