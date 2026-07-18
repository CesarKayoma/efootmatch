- [X] Correct bugs in the models<br>
> models must have their attributes properly defined<br>
><br>
> they should also have `db.relationship()` attributes when convenient, using `back_populates` when appropriate<br>

- [X] Set up PostgreSQL and database migrations<br>
> replace the local SQLite URI with a local PostgreSQL connection, installing the required driver<br>
><br>
> configure Flask-Migrate/Alembic instead of relying on `db.create_all()`<br>
><br>
> keep the connection configurable via `DATABASE_URL`, so a hosted database (e.g. Neon) can be used later without code changes<br>

### Backlog / Decisões futuras

> Autenticação: dois usuários (eu + amigo), mesmo histórico de partidas compartilhado. Amigo tem acesso só de leitura (rotas GET); só eu posso registrar dados (POST). Vai precisar de um conceito de role (owner vs. viewer) no login, mas não deve exigir mudança nos models de domínio (Team/Player/Match/Goal) — é uma camada por cima das rotas. A decidir quando implementar.<br>
><br>
> Cartas duplicadas do eFootball: um mesmo jogador pode ter cartas diferentes (versões) no jogo. O schema atual não modela isso — `Player` é único por nome+time. Vai exigir mudança de schema quando for tratado. A decidir se/quando implementar.<br>