# 📖 MAM Investigação Digital — Guia Operacional & Bíblia Diária

Este documento reúne os procedimentos operacionais padrão (SOP) para gestão do ambiente de laboratório, testes de conformidade com diretivas de segurança (APD), comandos essenciais do Git e operações via GitHub CLI.

---

## 🐳 1. GESTÃO DA INFRAESTRUTURA DOCKER

### Subir e Parar o Laboratório
```bash
# Iniciar todos os containers em segundo plano (PostGIS, PHP 8.3-FPM, Nginx)
docker compose up -d

# Parar os containers mantendo os dados persistentes
docker compose stop

# Destruir containers e redes virtuais (mantém volumes de dados)
docker compose down

# Reiniciar um serviço específico
docker compose restart nginx_lab_server

# Listar status dos containers e portas mapeadas
docker compose ps

# Visualizar logs em tempo real (Stream)
docker compose logs -f

# Visualizar logs apenas do Nginx ou PHP
docker compose logs -f nginx_lab_server
docker compose logs -f php_lab_app

# Executar terminal interativo dentro de um container
docker exec -it db_cyber_intel bash
docker exec -it php_lab_app bash# 1. Teste de Bloqueio RCE (disable_functions no php.ini)
# Esperado: Fatal error: Uncaught Error: Call to undefined function system()
curl -i "http://localhost:8090/index.php?cmd=id"

# 2. Teste de Bloqueio LFI (open_basedir no php.ini)
# Esperado: Warning: include(): open_basedir restriction in effect.
curl -i "http://localhost:8090/index.php?page=../../../../etc/passwd"

# 3. Teste de Acesso Restrito Nginx (Ficheiros sensíveis)
# Esperado: HTTP/1.1 403 Forbidden
curl -i "http://localhost:8090/php/php.ini"
curl -i "http://localhost:8090/nginx/default.conf"# Verificar status resumido e alinhamento com o repositório remoto
git status -sb

# Comparar histórico local vs GitHub
git log origin/main -n 5 --oneline --graph

# Ver diferenças detalhadas entre o ambiente local e a branch remota
git diff --stat origin/main# 1. Preparar ficheiros para a zona de staging
git add <ficheiro_ou_diretorio>

# 2. Criar commit padronizado (feat, docs, fix, refactor, chore)
git commit -m "docs(sop): adicionar guia operacional diario"

# 3. Enviar alterações para o GitHub
git push origin main

# 4. Atualizar o repositório local sem alterar ficheiros em edição
git fetch origin# Criar uma nova versão assinada (Tag anotada)
git tag -a v1.0.1 -m "v1.0.1 - Atualizacao de documentacao operacional"

# Enviar a tag para o GitHub
git push origin v1.0.1# Autenticação e estado do perfil no terminal
gh auth status
gh auth login

# Atualizar metadados do repositório (Descrição e Tags)
gh repo edit --description "Laboratorio Forense Digital, GeoINT e Web Cyber Range (APD)." \
             --add-topic dfir,forensics,geoint,postgis,php-hardening,docker,cybersecurity,angola

# Listar e criar Releases no GitHub
gh release list
gh release create v1.0.0 --title "v1.0.0 - Lançamento Oficial" --notes "Release inicial da infraestrutura."# Autenticação e estado do perfil no terminal
gh auth status
gh auth login

# Atualizar metadados do repositório (Descrição e Tags)
gh repo edit --description "Laboratorio Forense Digital, GeoINT e Web Cyber Range (APD)." \
             --add-topic dfir,forensics,geoint,postgis,php-hardening,docker,cybersecurity,angola

# Listar e criar Releases no GitHub
gh release list
gh release create v1.0.0 --title "v1.0.0 - Lançamento Oficial" --notes "Release inicial da infraestrutura."
# Ativar o ambiente virtual isolado
source .venv/bin/activate

# Instalar dependências a partir do requirements.txt
pip install -r requirements.txt

# Executar testes dos parsers forenses de metadados
python3 tools/parsers/generate_test_image.py
python3 tools/parsers/exif_parser.py
