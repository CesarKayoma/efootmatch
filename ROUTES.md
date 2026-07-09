### API Routes

Convenção: REST por recurso (Team, Player, Match), com Goal como sub-recurso de Match, e rotas dedicadas para as visões agregadas (timeline, dashboard) que não mapeiam pra uma entidade só.

#### Teams

* `GET /teams` — lista todos os times
* `POST /teams` — cria um time (`name`)
* `GET /teams/<id>` — detalhe de um time (inclui jogadores)

#### Players

* `GET /players` — lista jogadores (filtro opcional `?team_id=`)
* `POST /players` — cria um jogador (`name`, `team_id`)
  - BR02 — jogador precisa pertencer a um time existente
  - BR04 — nome único dentro do mesmo time
* `GET /players/<id>` — detalhe de um jogador

#### Matches

* `GET /matches` — lista partidas
* `POST /matches` — cria uma partida, já com `man_of_the_match` definido
  - BR01 — partida precisa ter MOTM definido na criação
* `GET /matches/<id>` — detalhe da partida (FR07)
* `GET /matches/<id>/timeline` — timeline dos eventos (gols) da partida, em ordem (FR05)

#### Goals (sub-recurso de Match)

* `POST /matches/<id>/goals` — registra um gol (`scorer_id`, `assister_id` opcional, `own_goal`)
  - BR03 — gol precisa ser de um jogador existente
  - BR05 — gol contra deve contar como gol do time adversário ao registrado
  - BR06 — quem marca não pode ser quem assiste
* `GET /matches/<id>/goals` — lista os gols de uma partida

#### Dashboard

* `GET /dashboard` — visão geral com as principais estatísticas do sistema (FR06)