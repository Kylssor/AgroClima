# Mapa del proyecto

> Índice de navegación. Consulta esto ANTES de explorar con Grep/Glob.
> No es exhaustivo línea por línea, solo dice dónde está cada cosa.
> El código Python vive dentro de `/backend` (carpetas PascalCase:
> `Config`, `Continair`, `Contracts`, `Controllers`, `Exceptions`,
> `Helpers`, `Middlewares`, `Models`, `Schemas`, `Services`, `Utils`,
> `main.py`, `requirements.txt`). Las migraciones viven en
> `/database/Migrations`. `alembic.ini` se quedó en la raíz del repo
> (con `script_location = database/Migrations` y `prepend_sys_path =
> backend`). `/frontend` y `/tests` siguen vacíos.

## Entrypoint y configuración
| Archivo | Qué hay |
|---|---|
| `backend/main.py` | App FastAPI, monta middlewares y prefijo `/api` (`Project_config.API_PREFIX()`). Se corre con `uvicorn main:app --reload --app-dir backend` desde la raíz del repo |
| `backend/Config/project_config.py` | Config vía `.env` (DB_HOST/USER/PASSWORD/PORT/ENGINE/NAME, JWT, CORS, API_PREFIX). Carga el `.env` de la raíz del repo con `Path(__file__).resolve().parents[2] / ".env"` (independiente del working directory) |
| `.env.example` (raíz) | Plantilla de variables que necesita `project_config.py`; copiar a `.env` en la raíz y completar |
| `backend/Continair/container.py` | Contenedor DI (`dependency-injector`). Por entidad: provider de repo genérico + provider de service. `wiring_config.modules` debe incluir cada controller |
| `backend/Controllers/routes.py` | Registra todos los `APIRouter` de `Controllers/*` |
| `alembic.ini` (raíz) + `database/Migrations/env.py` | Config Alembic: `script_location = database/Migrations`, `prepend_sys_path = backend`. Se corre desde la raíz del repo (`alembic upgrade head`, `alembic revision --autogenerate -m "..."`) |
| `database/Migrations/versions/` | Migraciones en orden cronológico por nombre de archivo (hash + descripción `agroclima1_1_x`); la última define el estado actual del esquema |

## Por entidad (patrón Controller → Service → Model → Schema)
Todas las entidades siguen el mismo patrón; usar `Plagas` como referencia
si hay que agregar una entidad nueva.

| Entidad | Controller | Service | Model | Schema |
|---|---|---|---|---|
| Auth (login/registro/JWT) | `backend/Controllers/Auth/auth_controller.py` | `backend/Services/Auth/authentication_service.py` | `backend/Models/Token/token_blacklist.py` | `backend/Schemas/Auth/sign_in_schema.py`, `backend/Schemas/Auth/token_schema.py` |
| Usuario | — (se maneja vía Auth) | `backend/Services/User/user_service.py` | `backend/Models/User/user.py` | `backend/Schemas/User/user_schema.py`, `backend/Schemas/User/user_info_schema.py` |
| Plantas | `backend/Controllers/Plantas/plantas_controller.py` | `backend/Services/Plantas/plantas_service.py` | `backend/Models/Plantas/plantas.py` | `backend/Schemas/Plantas/plantas_schema.py` |
| Plantas Catálogo | `backend/Controllers/Plantas/plantasCat_controller.py` | `backend/Services/Plantas/plantasCat_service.py` | `backend/Models/Plantas/plantas_Cat.py` | `backend/Schemas/Plantas/plantasCat_schema.py` |
| Plagas | `backend/Controllers/Plagas/plagas_controller.py` | `backend/Services/Plagas/plagas_service.py` | `backend/Models/Plagas/plagas.py` | `backend/Schemas/Plagas/plagas_schema.py` |
| Plaga x Planta (relación) | `backend/Controllers/PlagXPlants/plagxplants_controller.py` | `backend/Services/PlagxPlants/plagxplants_service.py` | `backend/Models/PlagXPlants/plagxplants.py` | `backend/Schemas/PlagxPlants/plagxplants_schema.py` |
| Plantaciones | `backend/Controllers/Plantaciones/plantaciones_controller.py` | `backend/Services/Plantaciones/plantaciones_service.py` | `backend/Models/Plantaciones/plantaciones.py` | `backend/Schemas/Plantaciones/plantaciones_schema.py` |
| Roles | `backend/Controllers/Roles/roles_controller.py` | `backend/Services/Roles/roles_service.py` | `backend/Models/Roles/roles.py`, `backend/Models/Roles/rolesTy.py` | `backend/Schemas/Roles/roles_schema.py` |
| Recordatorios de cuidado | (sin controller/service propio todavía) | — | `backend/Models/RecordatoriosCuidados/recordCui.py` | — |

Nota: la carpeta "PlagxPlants" tiene casing inconsistente entre capas
(`backend/Controllers/PlagXPlants` y `backend/Models/PlagXPlants` con X
mayúscula, vs `backend/Services/PlagxPlants` y `backend/Schemas/PlagxPlants`
con x minúscula). Es así en el repo real, no es error de este mapa —
cuidado al escribir imports.

## Infraestructura compartida
| Archivo | Qué hay |
|---|---|
| `backend/Models/Base/Base_model.py` | Modelo base SQLModel: `id` (UUID), `created_at`, `updated_at`. Todas las entidades heredan de acá |
| `backend/Models/Context/sqlalchemy_context.py` | Conexión/sesión de DB |
| `backend/Models/Repository/sqlalchemy_generic_repository.py` | `SqlAlchemyGenericRepository`, única implementación de repo, usada por todas las entidades (no hay repo por entidad) |
| `backend/Contracts/abc_generic_repository.py` | Interfaz que implementa el repo genérico |
| `backend/Services/Cryptography/token_service.py` | Genera/valida JWT, chequea blacklist |
| `backend/Exceptions/app_exception.py`, `not_found_error_exception.py`, `duplicated_error_exception.py`, `unauthorized_exception.py` | Excepciones custom de negocio |
| `backend/Middlewares/exception_handler_middleware.py` | Mapea las excepciones de `Exceptions/` a códigos HTTP (400/404/409/401/500) |
| `backend/Helpers/uuid_helper.py` | Valida UUIDs (`Uuid_helper.check_valid_uuid`) — usar antes de `get_by_id`/`update`/`delete` en services |
| `backend/Helpers/validate_helper.py` | Validaciones varias (ej. email) |
| `backend/Utils/singleton.py` | Decorador singleton |
| `backend/requirements.txt` | Dependencias Python (UTF-8; antes estaba en UTF-16, ya corregido) |

## Documentación (/docs)
| Archivo | Qué hay |
|---|---|
| `docs/referencias/mapa.md` | Este archivo |
| `docs/referencias/api.md` | Lista de endpoints (a crear/mantener por el agente docs) |
| `docs/referencias/esquema-db.md` | Tablas y relaciones clave (a crear/mantener por el agente docs) |
| `docs/referencias/componentes.md` | N/A en este proyecto (no hay frontend implementado todavía) |
| `README.md` (raíz) | Instrucciones de instalación/arranque desde cero |

## Nota sobre imports
Los imports internos del código siguen siendo del estilo `from Config.x
import ...`, `from Continair.x import ...` (sin prefijo `backend.`),
porque `backend/` se usa como raíz de imports (`--app-dir backend` en
uvicorn, `prepend_sys_path = backend` en alembic.ini), no como paquete
Python normal. No "corregir" estos imports a `from backend.Config...`
sin avisar, rompería el arranque.

---
**Mantenimiento**: este mapa lo mantiene el agente `docs` y debe
actualizarse cada vez que se agregue una entidad o archivo con
responsabilidad propia. Si un agente no encuentra algo acá o detecta que
está desactualizado, debe explorar manualmente esa parte puntual y avisar
al agente `docs` para que lo actualice — no asumir que el mapa está mal
para todo el repo.
