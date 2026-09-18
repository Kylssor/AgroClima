# AgroClima

API REST para que un campesino registre sus plantaciones y reciba
recordatorios de cuidado (riego, fertilización, etc.), alertas de lo que
está vencido o por vencer, y recomendaciones para prevenir plagas.

- Especificación funcional completa → [`SPEC.md`](./SPEC.md)
- Índice de "qué hay en cada archivo" y convenciones de código →
  [`docs/referencias/mapa.md`](./docs/referencias/mapa.md)

## Stack
- Python + FastAPI + SQLModel/SQLAlchemy
- PostgreSQL, migraciones con Alembic
- Inyección de dependencias con `dependency-injector`
- Auth por JWT (`python-jose`) + bcrypt (`passlib`) para las contraseñas

## Estructura del repo
```
/backend      → toda la API (Controllers, Services, Models, Schemas, etc.)
/database     → Migrations/ (alembic.ini vive en la raíz del repo)
/frontend     → todavía no existe código de frontend
/docs         → documentación, incluye /docs/referencias (índice del repo)
/tests        → suite de pytest
```

---

## Cómo correrlo desde cero

Todos los comandos se corren **desde la raíz del repo**.

### 1. Requisitos previos
- Python 3.11+
- PostgreSQL corriendo, con una base de datos ya creada (vacía está bien):
  ```sql
  CREATE DATABASE agroclima;
  ```

### 2. Entorno virtual e instalación
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r backend/requirements.txt
```

### 3. Variables de entorno
```bash
cp .env.example .env
```
El `.env` se lee siempre desde la raíz del repo, sin importar desde dónde
ejecutes el comando. Completá estos valores:

| Variable | Para qué sirve | Ejemplo |
|---|---|---|
| `DB_ENGINE` | Motor de base de datos | `postgresql` |
| `DB_HOST` | Host de la base | `localhost` |
| `DB_PORT` | Puerto | `5432` |
| `DB_USER` | Usuario | `postgres` |
| `DB_PASSWORD` | Contraseña | — |
| `DB_NAME` | Nombre de la base creada en el paso 1 | `agroclima` |
| `JWT_SECRET_KEY` | Clave para firmar los JWT. **Sin esto el server no arranca** (a propósito: no hay valor por defecto en el código) | generar con `python -c "import secrets; print(secrets.token_hex(32))"` |
| `CORS_ORIGINS` | Orígenes del frontend separados por comas. Vacío = ninguno permitido. Nunca usar `*` | `http://localhost:5173` |

### 4. Crear las tablas
```bash
alembic upgrade head
```
Esto aplica todas las migraciones en orden y deja el esquema al día.

### 5. Levantar el servidor
```bash
uvicorn main:app --reload --app-dir backend
```
- API disponible en `http://localhost:8000`, con todas las rutas bajo el
  prefijo `/api`.
- Documentación interactiva (Swagger) en `http://localhost:8000/docs` —
  es la forma más rápida de probar los endpoints a mano.
- `GET http://localhost:8000/` responde `"service is working"`, sirve como
  health check.

> **`--app-dir backend` no es opcional.** Hace que Python resuelva los
> imports internos (`Config.x`, `Continair.x`, …) tomando `backend/` como
> raíz. Sin ese flag, el import falla al arrancar.

---

## Cómo funciona

### Flujo de una request
```
HTTP  →  Controller  →  Service  →  Repository genérico  →  PostgreSQL
         (router)      (negocio)   (SqlAlchemyGenericRepository)
```
Todo se cablea en un contenedor de inyección de dependencias
(`backend/Continair/container.py`): el controller no instancia nada, recibe
el service ya armado.

Dos decisiones que explican buena parte del código:

- **No hay repositorios por entidad.** Todas usan el mismo
  `SqlAlchemyGenericRepository`, parametrizado con el modelo. Agregar una
  entidad nueva no implica escribir un repo.
- **Los controllers no devuelven códigos HTTP a mano.** Los services lanzan
  excepciones propias (`NotFoundErrorException`, `DuplicatedErrorException`,
  `UnauthorizedException`, …) y un middleware las traduce
  centralizadamente a 404 / 409 / 401 / 400 / 500.

### Autenticación
1. `POST /api/auth/signUp` → crea el usuario (contraseña hasheada con bcrypt).
2. `POST /api/auth/signIn` → devuelve un JWT válido por 24 h.
3. Se manda en cada request protegida como header
   `Authorization: Bearer <token>`.
4. `POST /api/auth/signOut` → mete el token en una blacklist en base de
   datos, así deja de servir aunque todavía no haya expirado.
5. `POST /api/auth/checkSession` → valida token + blacklist y devuelve el
   usuario.

Los endpoints protegidos declaran la dependencia explícitamente
(`Depends(auth_service.check_session)`); no hay un decorador global que
proteja todo por defecto.

### Endpoints principales
Todos bajo el prefijo `/api`:

| Ruta | Qué expone |
|---|---|
| `/auth` | signUp, signIn, signOut, checkSession |
| `/Plantas` y `/plantascategory` | Catálogo de plantas y sus categorías |
| `/Plagas` | Catálogo de plagas |
| `/Plagsxplants` | Relación plaga ↔ planta |
| `/SintomasPlanta` | Síntomas asociados a una planta |
| `/Plantaciones` | Las plantaciones del usuario autenticado |
| `/RecordatoriosCuidados` | Recordatorios de riego, fertilización, etc. |
| `/Alertas` | Agregador: recordatorios vencidos y próximos a vencer (`?dias_proximos=3`) |
| `/Roles` | Roles de usuario |

El detalle de cada método está en
[`docs/referencias/api.md`](./docs/referencias/api.md) y, en vivo, en
`/docs`.

---

## Correr los tests
```bash
pytest
```
Corren contra SQLite temporal: no necesitan Postgres ni un `.env` real.
Son tests de lógica de negocio (capa de service), **no** HTTP end-to-end —
el alcance y sus límites están en [`tests/README.md`](./tests/README.md).

## Migraciones
```bash
alembic revision --autogenerate -m "descripción"   # generar
alembic upgrade head                               # aplicar
alembic downgrade -1                               # revertir la última
```
`alembic.ini` ya apunta a `database/Migrations` y agrega `backend/` al
`sys.path`, por eso se corre desde la raíz.

> Para que `--autogenerate` detecte una tabla, su modelo tiene que estar
> importado en `database/Migrations/env.py`. Si falta el import, Alembic no
> ve la tabla y la migración sale vacía sin avisar. **Revisá siempre la
> migración generada antes de aplicarla.**

## Problemas comunes

| Síntoma | Causa |
|---|---|
| `ModuleNotFoundError: Config` al arrancar | Falta `--app-dir backend` en el comando de uvicorn |
| El server no arranca y se queja del secreto | Falta `JWT_SECRET_KEY` en el `.env` |
| El navegador bloquea las llamadas por CORS | `CORS_ORIGINS` vacío o sin el origen del frontend |
| 500 en un endpoint que en los tests pasa | El esquema real de Postgres está desfasado: falta correr `alembic upgrade head` |

## Notas de seguridad
- Las contraseñas se guardan hasheadas con bcrypt. El JWT se firma con
  `JWT_SECRET_KEY` del `.env`: no hay valor por defecto en el código a
  propósito, para no repetir el error de tener un secreto hardcodeado y
  commiteado.
- Hay rate limiting en los endpoints de autenticación
  (`backend/Helpers/rate_limiter.py`): 5 intentos de `signIn` cada 5 min y
  10 de `signUp` por hora. Es un contador en memoria del proceso, así que
  **deja de ser efectivo si se levanta con varios workers** — en producción
  hay que moverlo a un store compartido (Redis) o al reverse proxy.
- Riesgos conocidos y pendientes (por ejemplo, que no existe un rol de
  administrador para proteger los catálogos globales): ver la sección
  "Riesgos de seguridad conocidos" en [`SPEC.md`](./SPEC.md).
