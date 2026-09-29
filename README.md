# 🛡️ MAM - Laboratório Forense Digital & Inteligência Geoespacial (GeoINT)

## 📋 Caso Prático: Operação Sombra Digital
**Investigador / Lead Analyst:** Eng.º Malone Manuel  
**Conformidade:** ISO/IEC 27037 (Cadeia de Custódia & Integridade da Prova)

---

## 🏛️ Sobre o Projeto
Ambiente isolado de triagem, preservação e análise de evidências digitais (logs de rede, cabeçalhos de e-mail e metadados EXIF) com geolocalização e mapas de calor de ameaças em tempo real.

### 🛠️ Stack Tecnológica
* **Ambiente de Execução:** WSL2 (Ubuntu Linux Kernel) & Python 3.12 (`.venv`)
* **Banco de Dados Espacial:** PostgreSQL 16 + PostGIS 3.4 (Container Docker)
* **Visualização Espacial:** QGIS 3.x
* **Criptografia & Integridade:** SHA-256 (Hashing em modo binário)

---

## 🚀 Como Executar o Laboratório

### 1. Ativar o Ambiente Virtual Python
```bash
source .venv/bin/activate
pip install -r requirements.txt