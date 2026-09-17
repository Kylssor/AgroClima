# Esquema de base de datos — referencia rápida

Todas las tablas heredan de `Base_Model` (`backend/Models/Base/Base_model.py`):
`id` (UUID, PK), `created_at`, `updated_at`. No se repiten abajo.

## Tablas

### `user` (modelo `User`, `backend/Models/User/user.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name, last_name | str | |
| email | str | único a nivel de negocio (no hay constraint explícita revisada acá) |
| password | str | hash bcrypt (`Password_helper`) |
| roles | UUID, **nullable** | FK → `roles.id`. Nullable desde la migración `16bb9f2f8187` (ver nota FK circular abajo) |

### `roles` (modelo `Roles`, `backend/Models/Roles/roles.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name | str | |
| user | UUID, NOT NULL | FK → `user.id` (dueño/creador del rol) |
| rolesty | UUID, NOT NULL | FK → `rolesty.id` |

### `rolesty` (modelo `RolesTy`, `backend/Models/Roles/rolesTy.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name | str | tipo de rol (ej. admin, usuario) |

### `plantas_cat` (modelo `Plantas_Cat`, `backend/Models/Plantas/plantas_Cat.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name | str | categoría de planta |

### `plantas` (modelo `Plantas`, `backend/Models/Plantas/plantas.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name, description, recom | str | catálogo de tipos de planta |
| plantas_cat_id | UUID, NOT NULL | FK → `plantas_cat.id` |

### `plags` (modelo `Plags`, `backend/Models/Plagas/plagas.py`)
| Columna | Tipo | Notas |
|---|---|---|
| name, description, recom | str | catálogo de plagas; `recom` = prevención |

### `plagsxplants` (modelo `Plagsxplants`, `backend/Models/PlagXPlants/plagxplants.py`)
| Columna | Tipo | Notas |
|---|---|---|
| Plantas_id | UUID, NOT NULL | FK → `plantas.id` |
| Plags_id | UUID, NOT NULL | FK → `plags.id` |
Relación N:M plaga↔planta.

### `plants_mp` (modelo `Plants_mp` = Plantación, `backend/Models/Plantaciones/plantaciones.py`)
| Columna | Tipo | Notas |
|---|---|---|
| direction | str | |
| latitude, longitude | Decimal | |
| plants_id | UUID, NOT NULL | FK → `plantas.id` (tipo de planta) |
| user_id | UUID, NOT NULL | FK → `user.id` (dueño) — todas las operaciones filtran por este campo |

### `recordcui` (modelo `RecordCui` = RecordatorioCuidado, `backend/Models/RecordatoriosCuidados/recordCui.py`)
| Columna | Tipo | Notas |
|---|---|---|
| plantacion_id | UUID, NOT NULL | FK → `plants_mp.id` |
| tipo_cuidado | str | riego / fertilizacion / poda / otro |
| frecuencia_dias | int | |
| proxima_fecha | datetime | se recalcula al marcar cumplido (+`frecuencia_dias`) |
| activo | bool | |

### `sintoma_planta` (modelo `Sintoma_Planta`, `backend/Models/SintomaPlanta/sintoma_planta.py`)
| Columna | Tipo | Notas |
|---|---|---|
| planta_id | UUID, NOT NULL | FK → `plantas.id` |
| sintoma, diagnostico, recomendacion | str | |

### `token_blacklist` (modelo `Token_blacklist`, `backend/Models/Token/token_blacklist.py`)
| Columna | Tipo | Notas |
|---|---|---|
| expires_token | str | JWT invalidado por `signOut` |

## Relaciones clave (resumen)
```
user (1) ── (N) plants_mp [plantacion, dueño]
plantas_cat (1) ── (N) plantas
plantas (1) ── (N) plants_mp
plantas (1) ── (N) sintoma_planta
plantas (N) ── (N) plags   vía plagsxplants
plants_mp (1) ── (N) recordcui
rolesty (1) ── (N) roles
user (1) ── (N) roles [roles.user]     ← lado NOT NULL
roles (1) ── (0/1) user [user.roles]   ← lado NULLABLE (ver nota abajo)
```

## Nota importante: FK circular `user.roles` ↔ `roles.user`
`user.roles` (FK a `roles.id`) y `roles.user` (FK a `user.id`) forman un
ciclo. La migración original creó AMBOS lados `NOT NULL`, lo cual hacía
**imposible crear un usuario nuevo** contra Postgres real: para insertar
un `user` hacía falta una fila en `roles` ya existente, y para insertar
esa fila en `roles` hacía falta el `user` al que apunta.

La migración `database/Migrations/versions/16bb9f2f8187_agroclima1_1_9.py`
relaja `user.roles` a **NULLABLE**. Flujo correcto ahora: se crea el
`user` con `roles = NULL` (`POST /api/auth/signUp`), y después se le
asigna un rol creando una fila en `roles` que apunta a ese `user`
(`roles.user`, que sigue siendo `NOT NULL`) y luego actualizando
`user.roles` con el id de esa fila.

**No "arreglar" esto poniendo `roles.user` nullable en su lugar** ni
volver a poner `user.roles` como `NOT NULL` sin resolver el orden de
creación — se reintroduciría el candado que bloqueaba el registro.
