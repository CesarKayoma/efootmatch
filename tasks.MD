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