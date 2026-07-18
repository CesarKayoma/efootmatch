### API Routes

Convenção: app Flask + Jinja2 (server-rendered), forms com Flask-WTF/WTForms. Rotas de escrita seguem o padrão `/criar` e `/<id>/editar`, cada uma aceitando `GET` (exibe o form) e `POST` (processa o submit) na mesma rota. Sem rotas de `DELETE` (ver `tasks.MD`, seção Backlog, e a decisão sobre RESTRICT natural do banco).

#### Teams

- `GET /teams` — lista todos os times
- `GET, POST /teams/criar` — form de criação de time (`name`)
- `GET /teams/<id>` — detalhe de um time (inclui jogadores)
- `GET, POST /teams/<id>/editar` — form de edição (correção de nome)

#### Players

- `GET /players` — lista jogadores (filtro opcional `?team_id=`)
- `GET, POST /players/criar` — form de criação de jogador (`name`, `team_id`)
  - BR02 — jogador precisa pertencer a um time existente
  - BR04 — nome único dentro do mesmo time
- `GET /players/<id>` — detalhe de um jogador
- `GET, POST /players/<id>/editar` — form de edição (correção de nome)

#### Matches

Uma partida é criada e editada como uma unidade só: o form tem os gols (via `FieldList` do WTForms, linhas que se repetem dinamicamente conforme o usuário preenche) e o MOTM, tudo submetido junto num único `POST`. Não existe rota própria pra gol individual — criar/editar/remover um gol acontece sempre através do form da partida inteira.

- `GET /matches` — lista partidas
- `GET, POST /matches/criar` — form de criação: gols (linhas dinâmicas) + MOTM, tudo em um POST só
  - BR01 — partida precisa ter MOTM definido na criação
  - BR03 — cada gol precisa ser de um jogador existente
  - BR05 — gol contra deve contar como gol do time adversário ao registrado
  - BR06 — quem marca não pode ser quem assiste
- `GET /matches/<id>` — detalhe da partida, incluindo os gols (FR07)
- `GET /matches/<id>/timeline` — timeline dos eventos (gols) da partida, em ordem (FR05)
- `GET, POST /matches/<id>/editar` — reabre o mesmo form de criação preenchido; ao salvar, substitui o conjunto de gols da partida pelos que vierem no submit (permite corrigir, adicionar ou remover gols, e corrigir o MOTM)

#### Dashboard

- `GET /dashboard` — visão geral com as principais estatísticas do sistema (FR06)
