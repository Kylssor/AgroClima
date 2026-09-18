# Mapa del proyecto

> Índice de navegación: conviene mirarlo antes de buscar a mano por todo
> el repo. No es exhaustivo línea por línea, solo dice dónde está cada cosa.
> El código Python vive dentro de `/backend` (carpetas PascalCase:
> `Config`, `Continair`, `Contracts`, `Controllers`, `Exceptions`,
> `Helpers`, `Middlewares`, `Models`, `Schemas`, `Services`, `Utils`,
> `main.py`, `requirements.txt`). Las migraciones viven en
> `/database/Migrations`. `alembic.ini` se quedó en la raíz del repo
> (con `script_location = database/Migrations` y `prepend_sys_path =
> backend`). `/tests` ya tiene una suite de pytest (ver más abajo).
> `/frontend` sigue vacío.

## Entrypoint y configuración
| Archivo | Qué hay |
|---|---|
| `backend/main.py` | App FastAPI, monta middlewares y prefijo `/api` (`Project_config.API_PREFIX()`). Se corre con `uvicorn main:app --reload --app-dir backend` desde la raíz del repo |
| `backend/Config/project_config.py` | Config vía `.env` (DB_HOST/USER/PASSWORD/PORT/ENGINE/NAME, JWT, CORS, API_PREFIX). Carga el `.env` de la raíz del repo con `Path(__file__).resolve().parents[2] / ".env"` (independiente del working directory) |
| `.env.example` (raíz) | Plantilla de variables que necesita `project_config.py`; copiar a `.env` en la raíz y completar |
| `backend/Continair/container.py` | Contenedor DI (`dependency-injector`). Por entidad: provider de repo genérico + provider de service. `wiring_config.modules` debe incluir cada controller |
| `backend/Controllers/routes.py` | Registra todos los `APIRouter` de `Controllers/*` |
| `backend/Controllers/Alertas/alertas_controller.py` | Endpoint agregador `GET /api/Alertas?dias_proximos=3`, sin Model/Schema propios — reutiliza `RecordatorioCuidado_service.get_alertas(user_id, dias_proximos)` para listar recordatorios vencidos/próximos de todas las plantaciones del usuario autenticado |
| `alembic.ini` (raíz) + `database/Migrations/env.py` | Config Alembic: `script_location = database/Migrations`, `prepend_sys_path = backend`. Se corre desde la raíz del repo (`alembic upgrade head`, `alembic revision --autogenerate -m "..."`) |
| `database/Migrations/versions/` | Migraciones en orden cronológico por nombre de archivo (hash + descripción `agroclima1_1_x`); la última define el estado actual del esquema |
| `database/Migrations/versions/16bb9f2f8187_agroclima1_1_9.py` | Relaja `user.roles` a NULLABLE. Corrige la FK circular `user.roles`/`roles.user` (ambos `NOT NULL` en el modelo original) que hacía imposible crear un usuario nuevo — ver detalle en `docs/referencias/esquema-db.md` |
| `database/Migrations/versions/e8d9adf5a163_...token_blacklist.py` | Crea la tabla `token_blacklist` (faltaba por completo contra Postgres — el modelo nunca estuvo importado en `env.py`, así que ningún `autogenerate` anterior la había detectado; rompía `checkSession`/`signOut` con 500 en cualquier entorno real, aunque los tests pasaban porque usan SQLite con `create_all`) |
| `database/Migrations/versions/a642cd723535_...fix_plags_recom_column.py` | Última migración: renombra `plags.recomenda` → `plags.recom` para que coincida con el modelo (`backend/Models/Plagas/plagas.py`); rompía `GET /api/Plagas` con 500 contra Postgres |
| `database/Migrations/env.py` | Ahora importa también `Sintoma_Planta` y `Token_blacklist` (antes faltaban, ver arriba). **Nota pendiente**: un `autogenerate` sobre el estado actual todavía va a proponer (a) agregar un `UNIQUE` constraint sobre `sintoma_planta.id` (inofensivo, ya es PK) y (b) **borrar** el constraint `user_email_key` porque `User.email` no tiene `unique=True` en el modelo — la unicidad de email hoy solo se valida en `authentication_service.sign_up` (capa de servicio), no en el modelo. No se tocó a propósito: es una decisión de diseño (mantener o no el constraint a nivel DB), no un bug obvio. Revisar la migración generada antes de aplicar el próximo `autogenerate`. |

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
| Roles | `backend/Controllers/Roles/roles_controller.py` | `backend/Services/Roles/roles_service.py` | `backend/Models/Roles/roles.py` (campos `user` FK→`user.id` y `rolesty` FK→`rolesty.id`, no `rolesty_id`), `backend/Models/Roles/rolesTy.py` | `backend/Schemas/Roles/roles_schema.py` |
| Recordatorios de cuidado | `backend/Controllers/RecordatoriosCuidados/recordatorios_cuidados_controller.py` | `backend/Services/RecordatoriosCuidados/recordatorio_cuidado_service.py` (`RecordatorioCuidado_service`) | `backend/Models/RecordatoriosCuidados/recordCui.py` (`RecordCui`) | `backend/Schemas/RecordatoriosCuidados/recordatorio_cuidado_schema.py` (`RecordatorioCuidado_schema`) |
| Sintoma de planta | `backend/Controllers/SintomaPlanta/sintoma_planta_controller.py` | `backend/Services/SintomaPlanta/sintoma_planta_service.py` (`SintomaPlanta_service`) | `backend/Models/SintomaPlanta/sintoma_planta.py` (`Sintoma_Planta`, tabla `sintoma_planta`) | `backend/Schemas/SintomaPlanta/sintoma_planta_schema.py` (`SintomaPlanta_schema`) |

Nota: la carpeta "PlagxPlants" tiene casing inconsistente entre capas
(`backend/Controllers/PlagXPlants` y `backend/Models/PlagXPlants` con X
mayúscula, vs `backend/Services/PlagxPlants` y `backend/Schemas/PlagxPlants`
con x minúscula). Es así en el repo real, no es error de este mapa —
cuidado al escribir imports.

Nota: `Plantaciones` y `Recordatorios de cuidado` filtran TODAS sus
operaciones (`get_all`, `get_by_id`, `update`, `delete`, y en el caso de
recordatorios también `create`) por el `user_id` del usuario autenticado
(dueño de la plantación). No es una validación superflua para quitar
"por simplicidad" — sin ella un usuario podría leer/editar plantaciones o
recordatorios de otro usuario.

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
| `backend/Helpers/password_helper.py` | `Password_helper`: hash/verify de contraseñas con bcrypt (`passlib`), usado desde `Services/Auth/authentication_service.py` |
| `backend/Helpers/rate_limiter.py` | `RateLimiter`: rate limiting en memoria por proceso (no sirve con varios workers, documentado en el propio archivo); usado en `POST /auth/signIn` (5/5min) y `POST /auth/signUp` (10/1h) desde `auth_controller.py` |
| `backend/Exceptions/too_many_requests_exception.py` | `TooManyRequestsException`, mapeada a 429 en `exception_handler_middleware.py`; la lanza `RateLimiter` |
| `backend/Utils/singleton.py` | Decorador singleton |
| `backend/requirements.txt` | Dependencias Python (UTF-8; antes estaba en UTF-16, ya corregido) |

## Documentación (/docs)
| Archivo | Qué hay |
|---|---|
| `docs/referencias/mapa.md` | Este archivo |
| `docs/referencias/api.md` | Lista de endpoints |
| `docs/referencias/esquema-db.md` | Tablas y relaciones clave |
| `docs/referencias/componentes.md` | N/A en este proyecto (no hay frontend implementado todavía) |
| `README.md` (raíz) | Instrucciones de instalación/arranque desde cero |

## Tests (/tests)
| Archivo | Qué hay |
|---|---|
| `tests/README.md` | Explica por qué son tests de service (no HTTP end-to-end) y sus límites — leer ahí antes de asumir cobertura E2E |
| `tests/conftest.py` | Fixtures: BD SQLite temporal + repos |
| `tests/test_generic_repository.py`, `test_plagas.py`, `test_roles.py`, `test_auth.py`, `test_plantaciones.py`, `test_recordatorios_y_alertas.py`, `test_sintoma_planta.py`, `test_app_wiring.py` | Un archivo de test por área. Se corren con `pytest` desde la raíz del repo (26 tests) |

## Nota sobre imports
Los imports internos del código siguen siendo del estilo `from Config.x
import ...`, `from Continair.x import ...` (sin prefijo `backend.`),
porque `backend/` se usa como raíz de imports (`--app-dir backend` en
uvicorn, `prepend_sys_path = backend` en alembic.ini), no como paquete
Python normal. No "corregir" estos imports a `from backend.Config...`
sin avisar, rompería el arranque.

---
**Mantenimiento**: actualizar este mapa cada vez que se agregue una entidad
o un archivo con responsabilidad propia. Si algo no figura acá o quedó
desactualizado, revisar esa parte puntual en el código y corregir la
entrada correspondiente — no asumir que el mapa entero está mal.
