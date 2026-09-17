# Tests

```
pip install -r backend/requirements.txt
pytest
```

## Por qué son tests de service, no de HTTP end-to-end

Cada controller hace `container = Container()` a nivel de módulo (efecto
secundario al importar), y el provider `db` del container es un
`Singleton` que arma la conexión a partir de `Project_config().DATABASE_URI`
apenas se resuelve por primera vez. Para pegarle a los endpoints reales con
`TestClient` haría falta una base de datos real (Postgres) o refactorizar
cómo se inyecta la config — ninguna de las dos entraba en el alcance de
esta pasada.

En su lugar, estos tests instancian los `Service` con un
`SqlAlchemyGenericRepository` apuntando a un SQLite temporal por test
(`conftest.py`), que es donde vive toda la lógica de negocio real
(ownership, cálculo de fechas, hashing, etc.) — los controllers son capas
finas encima que solo traducen HTTP ↔ service.

`test_app_wiring.py` es la excepción: importa `main` completo para
confirmar que el container y todos los controllers cablean sin errores
(agarra bugs como el de servicios inyectados por copy-paste). No necesita
una base de datos real porque `create_engine` no conecta hasta el primer
query.

## Limitación conocida

Las migraciones de Alembic (`database/Migrations/`) no se prueban acá:
usan `ALTER TABLE` con foreign keys, que SQLite no soporta. Los tests
crean el esquema directo desde los modelos (`SQLModel.metadata.create_all`).
Antes de aplicar las migraciones en un ambiente real, correr
`alembic upgrade head` contra un Postgres de prueba.
