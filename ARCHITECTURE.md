# 🏛️ DOCUMENTO MESTRE DE ARQUITETURA E IMPLEMENTAÇÃO (A a Z)
## Laboratório Forense Digital, OSINT e Inteligência Geoespacial
**Projeto:** MAM_InvestigacaoDigital
**Caso Prático:** Operação Sombra Digital
**Autor / Lead Investigator:** Eng.º Malone Manuel
**Versão:** 2.0 (Refatorado - Clean Build)

---

## 📋 SUMÁRIO EXECUTIVO

Este documento estabelece os requisitos técnicos, padrões de segurança, esquemas de dados, topologia de rede/containers e o guia de execução de A a Z para a investigação forense e análise espacial do caso Operação Sombra Digital.

O objetivo primário do pipeline é garantir a cadeia de custódia (integração e imutabilidade dos dados via SHA-256), efetuar o parsing automatizado de evidências heterogéneas (logs, e-mails, metadados EXIF) e correlacionar visualmente os vetores de ataque geográficos utilizando PostGIS e QGIS.

---

## 📑 MAPA GERAL DA IMPLEMENTAÇÃO (FASE A à FASE Z)

* FASE A: Topologia da Infraestrutura e Isolamento do Ambiente
* FASE B: Mapeamento da Árvore de Diretórios do Laboratório
* FASE C: Governança e Regras da Cadeia de Custódia (ISO/IEC 27037)
* FASE D: Especificação dos Containers Docker (PostgreSQL + PostGIS)
* FASE E: Modelo de Dados Relacional e Espacial (Esquema DDL)
* FASE F: Ingestão de Evidências Brutas (Caso: Operação Sombra Digital)
* FASE G: Desenvolvimentos das Ferramentas em Python (tools/)
* FASE H: Conexão e Integração Espacial com o QGIS
* FASE Z: Checklist de Execução e Manutenção Continuada
