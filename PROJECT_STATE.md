# PROJECT_STATE — Promptograph (4pixeltechBR)

> Fonte única de verdade do VibeDev.
> A IA lê este arquivo no início de TODA sessão e atualiza ao final.
> Conversa contradiz arquivo → arquivo vence. Sinalize divergência.

---

## Contexto para novo agente/sessão
Estamos preparando, saneando e empacotando o projeto **Promptograph** para release e sincronização segura com o repositório oficial `https://github.com/4pixeltechBR/promptograph`. O objetivo central é auditar o código e dataset existentes, selecionar conteúdos e ferramentas de baixo risco do ecossistema de Skills (prompts curados, validadores, templates, MCP) e garantir conformidade absoluta com o ToS do GitHub (zero vazamento de chaves/tokens, sem violações DMCA, sem ferramentas de ataque).

---

## Identidade
- **Projeto:** Promptograph
- **Repositório:** `https://github.com/4pixeltechBR/promptograph`
- **Pasta Local:** `E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph`
- **Trilha:** 🔴 Vermelha (Rescue / Saneamento & Open-Source Packaging)
- **Modo do usuário:** `tecnico`
- **O que o projeto faz (estado atual):** Toolkit para navegar, comparar (diff), validar deterministicamente (0-100%, 13 regras) e sintetizar system prompts de IA. Possui interface web offline em Python, servidor FastMCP com 4 tools e dataset de prompts.
- **Está em produção?** Parcialmente (repositório ativo no GitHub com v0.1.0 inicial; novas versões e scripts aguardando auditoria e saneamento).
- **Problema principal que motivou o rescue:** Saneamento preventivo antes de commits públicos. Necessidade de auditar dados, remover riscos de ToS/DMCA e integrar apenas ativos de baixo risco e alto valor das Skills.
- **Kill criteria:** Abandono de publicação pública se houver risco não mitigável de vazamento de credenciais ou infração direta de copyright comercial.
- **Restrições:** Zero chaves de API / segredos; conformidade com ToS do GitHub; arquivos individuais < 50 MB; código 100% testado e funcional.
- **Ambiente AI:** Antigravity / Gemini
- **Criado em:** 2026-09-17

---

## Mapa de fases
- [x] FASE R1 — Arqueologia (Mapeamento profundo do repo local, git diff e inventário de ativos em E:\Skills)
- [x] FASE R2 — Triagem & Matriz de Risco (Classificação de ativos: 34 Verdes, 5 Amarelas, 8 Falsos Positivos, 5 Vermelhas Isoladas)
- [x] FASE R3 — Estabilização & Blindagem (.gitignore estrito, desacoplamento de goal.py, zero vazamento de caminhos pessoais)
- [x] FASE R4 — Remediação & Integração de Valor (FastMCP Server v0.3.1 com 7 tools, 226 skills em 37 categorias, manifesto gerado)
- [x] FASE R5 — Documentação, Validação Final e Graduação (README bilíngue atualizado, suíte de testes 100% verde, release GitHub v0.3.1)
- [➔] → Trilha Verde (Evolução contínua: expansão de blueprints, registry web e indexação contínua de skills)

Marcação: `[➔]` fase atual · `[x]` concluída · `[ ]` futura

---

## Fase atual
- **Fase:** Trilha Verde — Evolução Contínua
- **Sub-tarefa ativa:** G1.0 — Monitoramento do repositório público, documentação de integração MCP para usuários e catalogação incremental
- **Está pronto quando:** Repositório publicado e ativo em `https://github.com/4pixeltechBR/promptograph` com tags v0.2.0 e v0.3.1 disponíveis
- **Próximo passo explícito:** Divulgação, conexões em plataformas como Awesome-MCP-Servers e expansão de novas tools sob demanda.

---

## Mapa do Caos (preenchido na R1)
### Stack encontrada
- **Linguagem:** Python 3.10+
- **Frameworks/Libs principais:** FastMCP, Standard Library (`http.server`, `json`, `csv`, `re`, `argparse`), Vanilla JS / Tailwind / Lucide Icons na UI web estática.
- **Banco de dados:** JSON flat files (`index.json`, `index_filtered.json`)
- **Autenticação:** Nenhuma (ferramenta local/offline)
- **Hospedagem atual:** GitHub Pages (docs estáticos) e execução local

### Estrutura de arquivos atual
- `data/index_filtered.json`: Dataset principal de 5.317 system prompts (~5.6 MB).
- `generator/`: `builder.py`, `parser.py`, `refine_index.py` (motores de parsing e construção).
- `validators/quality.py`: Validador heurístico de 13 regras.
- `static/`: Interface gráfica offline (HTML/CSS/JS).
- `scripts/`: Ferramentas CLI, FastMCP Server e testes automatizados.
- `src/skills/promptograph/`: Módulo python encapsulado (`builder.py`, `validator.py`, `goal.py`).

### O que funciona
- Servidor web offline (`python server.py`) respondendo em http://localhost:8000.
- Servidor FastMCP com 4 tools operacionais (`scripts/promptograph_mcp_server.py`).
- Validador heurístico (13 regras, notas A+ a F).
- CLI de busca ultrarrápida (`scripts/search_promptograph.py`).

### O que precisa de atenção / Risco potencial
- `data/index_filtered.json` contém 5.317 prompts extraídos de várias fontes públicas da internet (necessário validar se há prompts com dados pessoais, chaves vazadas ou prompts comerciais protegidos).
- Presença de caminhos absolutos ou referências a projetos internos que precisam ser sanitizados.
- Configuração do `.gitignore` para garantir que arquivos de ambiente ou testes locais nunca subam.

---

## Lista de Triagem (preenchida na R2)

### P0 — Crítico (Segurança e Integridade)
| # | Problema | Localização | Está pronto quando | Status |
|---|----------|-------------|--------------------|--------|
| 1 | Garantir que nenhum arquivo contenha tokens, chaves ou nomes proprietários internos | Todo o repositório | Scan de segredos passar com zero alertas | Aberto |
| 2 | `.gitignore` blindado contra `.env`, dados temporários e caches | `.gitignore` | Regras explícitas comitadas | Aberto |

### P1 — Urgente (Conformidade e Valor)
| # | Problema | Localização | Está pronto quando | Status |
|---|----------|-------------|--------------------|--------|
| 3 | Seleção criteriosa dos prompts de baixo risco para empacotar | `data/` | Dataset filtrado e categorizado com segurança | Aberto |
| 4 | Integração dos scripts e servidor FastMCP na árvore oficial do git | `scripts/` e `src/` | Código integrado, testado e documentado | Aberto |

---

## Decision Log
- **[2026-09-17] [Tipo 1] Ativação da Governança VibeDev (Trilha Vermelha):** Decidido aplicar o framework VibeDev para gerenciar a preparação e auditoria do projeto Promptograph antes de qualquer commit/push no repositório `4pixeltechBR/promptograph`.
