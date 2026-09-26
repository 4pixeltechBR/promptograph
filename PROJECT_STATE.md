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
- **O que o projeto faz (estado atual):** Toolkit para navegar, comparar (diff), validar deterministicamente (0-100%, 13 regras) e sintetizar system prompts de IA. Base indexada de 20.475 prompts reais (~97M tokens), interface web offline stdlib, servidor FastMCP com 7 tools e manifesto operacional com 226 skills curadas em 37 domínios.
- **Está em produção?** Sim (repositório ativo no GitHub com v0.3.1 oficial e tags sincronizadas).
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
- **Está pronto quando:** Repositório publicado e ativo em `https://github.com/4pixeltechBR/promptograph` com tags v0.2.0, v0.3.0 e v0.3.1 disponíveis
- **Próximo passo explícito:** Divulgação, conexões em plataformas como Awesome-MCP-Servers e expansão de novas tools sob demanda.

---

## Mapa do Caos (preenchido na R1 / Atualizado na R5)
### Stack encontrada
- **Linguagem:** Python 3.10+
- **Frameworks/Libs principais:** FastMCP, Standard Library (`http.server`, `json`, `csv`, `re`, `argparse`), Vanilla JS / Tailwind / Lucide Icons na UI web estática.
- **Banco de dados:** JSON flat files (`index.json`, `index_filtered.json`)
- **Autenticação:** Nenhuma (ferramenta local/offline)
- **Hospedagem atual:** GitHub Pages (docs estáticos) e execução local

### Estrutura de arquivos atual
- `data/index_filtered.json`: Dataset principal de 20.475 system prompts (~5.2 MB, 94M tokens).
- `data/curated_skills_manifest.json`: Manifesto de 226 skills curadas em 37 categorias com links e metadados.
- `generator/`: `builder.py`, `parser.py`, `refine_index.py` (motores de parsing e construção).
- `validators/quality.py`: Validador heurístico de 13 regras.
- `static/`: Interface gráfica offline (HTML/CSS/JS) com abas de Prompts, Diff e Skills MCP.
- `scripts/`: Ferramentas CLI, FastMCP Server (7 tools) e testes automatizados.
- `src/skills/promptograph/`: Módulo python encapsulado (`builder.py`, `validator.py`, `skills_registry.py`).

### O que funciona
- Servidor web offline (`python server.py 8765`) respondendo com abas completas e endpoints de skills.
- Servidor FastMCP com 7 tools operacionais (`scripts/promptograph_mcp_server.py`).
- Validador heurístico (13 regras, notas A+ a F).
- CLI de busca ultrarrápida (`scripts/search_promptograph.py`).
- Registro dinâmico de 226 skills com extração de blueprints markdown.

### O que precisa de atenção / Risco potencial
- Manter o manifesto de skills sincronizado com adições de novas skills no ecossistema local.
- Respeitar a regra de nunca vazar dados de credenciais nem paths pessoais nos commits do GitHub.

---

## Lista de Triagem (preenchida na R2 / Concluída na R5)

### P0 — Crítico (Segurança e Integridade)
| # | Problema | Localização | Está pronto quando | Status |
|---|----------|-------------|--------------------|--------|
| 1 | Garantir que nenhum arquivo contenha tokens, chaves ou nomes proprietários internos | Todo o repositório | Scan de segredos passar com zero alertas | Concluído |
| 2 | `.gitignore` blindado contra `.env`, dados temporários e caches | `.gitignore` | Regras explícitas comitadas | Concluído |

### P1 — Urgente (Conformidade e Valor)
| # | Problema | Localização | Está pronto quando | Status |
|---|----------|-------------|--------------------|--------|
| 3 | Seleção criteriosa dos prompts de baixo risco para empacotar | `data/` | Dataset de 20.475 prompts sanitizado e categorizado | Concluído |
| 4 | Integração dos scripts e servidor FastMCP na árvore oficial do git | `scripts/` e `src/` | Código integrado, testado (7 tools MCP) e documentado | Concluído |

---

## Decision Log
- **[2026-09-17] [Tipo 1] Ativação da Governança VibeDev (Trilha Vermelha):** Decidido aplicar o framework VibeDev para gerenciar a preparação e auditoria do projeto Promptograph antes de qualquer commit/push no repositório `4pixeltechBR/promptograph`.
- **[2026-09-25] [Tipo 2] Release v0.3.1 (Skills MCP Hub & 20.475 Prompts):** Harmonização integral da documentação, expansão do FastMCP para 7 tools (4 prompts + 3 skills), suporte a 226 skills curadas em 37 categorias e release oficial tag v0.3.1.
