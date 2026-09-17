# AgroClima

API para que un campesino registre sus plantaciones y reciba recordatorios
de cuidado (riego, fertilización, etc.) y recomendaciones para mantenerlas
sanas y prevenir plagas. Ver [`SPEC.md`](./SPEC.md) para la especificación
completa y [`CLAUDE.md`](./CLAUDE.md) para la arquitectura del código.

## Stack
- Python + FastAPI + SQLModel/SQLAlchemy
- PostgreSQL, migraciones con Alembic
- Inyección de dependencias con `dependency-injector`
- Auth por JWT (`python-jose`)

## Estructura del repo
```
/backend      → toda la API (Controllers, Services, Models, Schemas, etc.)
/database     → Migrations/ (alembic.ini vive en la raíz del repo)
/frontend     → todavía no existe código de frontend
/docs         → documentación, incluye /docs/referencias (índice para agentes)
/tests        → todavía vacío, no hay suite de tests
```

## Cómo correr el proyecto desde cero
Todos los comandos se corren desde la raíz del repo.

1. Instalar dependencias:
   ```
   pip install -r backend/requirements.txt
   ```
2. Configurar variables de entorno:
   ```
   cp .env.example .env
   ```
   y completar `.env` con los datos reales de tu base de datos (`DB_ENGINE`,
   `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`), un
   `JWT_SECRET_KEY` propio (generarlo con
   `python -c "import secrets; print(secrets.token_hex(32))"` — el server
   no arranca sin esto) y, cuando exista frontend, `CORS_ORIGINS` con los
   orígenes permitidos separados por comas (vacío = ninguno).
3. Correr las migraciones:
   ```
   alembic upgrade head
   ```
4. Levantar el servidor:
   ```
   uvicorn main:app --reload --app-dir backend
   ```
   La API queda disponible en `http://localhost:8000`, bajo el prefijo
   `/api`.

## Notas
- No hay suite de tests automatizados todavía.
- Las contraseñas se guardan hasheadas con bcrypt (`passlib`). El JWT
  usa `JWT_SECRET_KEY` del `.env` — no hay un valor por defecto en el
  código a propósito, para no repetir el error de tener un secreto
  hardcodeado y commiteado.
- Riesgos de seguridad conocidos y pendientes (sin rol de administrador
  para los catálogos globales, sin rate limiting en login, etc.): ver la
  sección "Riesgos de seguridad conocidos" en [`SPEC.md`](./SPEC.md).
