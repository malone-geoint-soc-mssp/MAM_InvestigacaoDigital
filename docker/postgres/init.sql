CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS tb_cadeia_custodia (
    id SERIAL PRIMARY KEY,
    nome_ficheiro VARCHAR(255) NOT NULL,
    caminho_relativo TEXT NOT NULL,
    hash_sha256 CHAR(64) NOT NULL UNIQUE,
    tamanho_bytes BIGINT NOT NULL,
    coletado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    investigador VARCHAR(100) DEFAULT 'Eng.º Malone Manuel'
);

CREATE TABLE IF NOT EXISTS tb_evidencias_geo (
    id SERIAL PRIMARY KEY,
    custodia_id INT REFERENCES tb_cadeia_custodia(id),
    caso_id VARCHAR(50) DEFAULT 'operacao_sombra_digital',
    origem_evidencia VARCHAR(100) NOT NULL,
    tipo_vetor VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    geom GEOMETRY(Point, 4326),
    detalhes_tecnicos JSONB,
    registado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidencias_geo_geom ON tb_evidencias_geo USING GIST(geom);
