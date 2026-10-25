# 🛡️ MAM - Laboratório Forense Digital, GeoINT & Web Cyber Range

### 📋 Caso Prático: Operação Sombra Digital
* **Investigador / Lead Analyst:** Eng.º Malone Manuel
* **Conformidade:** ISO/IEC 27037 (Cadeia de Custódia e Integridade da Prova) & Diretivas APD (Proteção de Dados)

---

## 🏛️ Sobre o Projeto

Ambiente isolado de triagem, preservação e análise de evidências digitais (logs de rede, cabeçalhos de e-mail e metadados EXIF) com geolocalização e mapas de calor de ameaças em tempo real, integrado com um **Laboratório de Simulação e Hardening Web (PHP 8.3 / Nginx)**.

---

## 🛠️ Stack Tecnológica

* **Ambiente de Execução:** WSL2 (Ubuntu Linux) & Python 3.12 (`.venv`)
* **Banco de Dados Espacial:** PostgreSQL 16 + PostGIS 3.4 (Porta `5439`)
* **Servidor Web & Application Range:** Nginx Alpine (Porta `8090`) + PHP 8.3-FPM
* **Segurança & Hardening:** Controlo `open_basedir`, `disable_functions` e mitigação de LFI/RCE (APD)
* **Visualização Espacial & Forense:** QGIS 3.x & Parsers EXIF/GPS customizados
* **Criptografia & Integridade:** SHA-256 (Hashing em modo binário)

---

## 🚀 Como Executar o Laboratório

### 1. Ativar o Ambiente Virtual e Subir a Stack Docker

```bash
# Ativar o ambiente Python
source .venv/bin/activate
pip install -r requirements.txt

# Inicializar os containers em segundo plano
docker compose up -d
