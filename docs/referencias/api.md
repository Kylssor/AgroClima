# API — referencia rápida

Todos los paths llevan prefijo global `/api` (agregado en `backend/main.py`
vía `Project_config.API_PREFIX()`). "Auth" = requiere JWT válido
(`Depends(auth_service.check_session)`). "Ownership" = además el service
filtra/valida que el recurso pertenezca al `user.id` del token (401 si no).

## Auth
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| POST | `/api/auth/signIn` | No (rate limit 5/5min por IP+email) | form-urlencoded `username`(email)/`password` | `token_schema` (JWT) |
| POST | `/api/auth/signUp` | No (rate limit 10/1h por IP) | `User_schema` (name, last_name, email, password) | `User_info_schema` |
| POST | `/api/auth/signOut` | Sí (bearer token) | — | invalida token (blacklist) |
| POST | `/api/auth/checkSession` | Sí | — | `User_info_schema` del usuario del token |

## Plantas (catálogo de tipos de planta)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Plantas/` | No | — | `list[Plantas]` |
| GET | `/api/Plantas/{id}` | No | — | `Plantas` |
| POST | `/api/Plantas/` | Sí | `Plantas_schema` | `Plantas` |
| PATCH | `/api/Plantas/` | Sí | `Plantas_schema` (incluye `id`) | `Plantas` |
| DELETE | `/api/Plantas/{id}` | Sí | — | 204 |

## Plantas Categoría (catálogo de categorías, tabla `plantas_cat`)
Nota: el path real es `/plantascategory`, no `/PlantasCat` (así está en el código).
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/plantascategory/` | No | — | `list[Plantas_Cat]` |
| GET | `/api/plantascategory/{id}` | No | — | `Plantas_Cat` |
| POST | `/api/plantascategory/` | Sí | `PlantasCat_schema` | `Plantas_Cat` |
| PATCH | `/api/plantascategory/` | Sí | `PlantasCat_schema` | `Plantas_Cat` |
| DELETE | `/api/plantascategory/{id}` | Sí | — | 204 |

## Plagas (catálogo de plagas, modelo `Plags`)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Plagas/` | No | — | `list[Plags]` |
| GET | `/api/Plagas/{id}` | No | — | `Plags` |
| POST | `/api/Plagas/` | Sí | `Plagas_schema` | `Plags` |
| PATCH | `/api/Plagas/` | Sí | `Plagas_schema` | `Plags` |
| DELETE | `/api/Plagas/{id}` | Sí | — | 204 |

## PlagXPlants (relación N:M plaga↔planta, modelo `Plagsxplants`)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Plagsxplants/` | No | — | `list[Plagsxplants]` |
| GET | `/api/Plagsxplants/{id}` | No | — | `Plagsxplants` |
| POST | `/api/Plagsxplants/` | Sí | `PlagxPlants_schema` | `Plagsxplants` |
| PATCH | `/api/Plagsxplants/` | Sí | `PlagxPlants_schema` | `Plagsxplants` |
| DELETE | `/api/Plagsxplants/{id}` | Sí | — | 204 |

## Plantaciones (modelo `Plants_mp`) — filtra por dueño
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Plantaciones/` | Sí + ownership | — | `list[Plants_mp]` del usuario |
| GET | `/api/Plantaciones/{id}` | Sí + ownership | — | `Plants_mp` (401 si no es dueño) |
| POST | `/api/Plantaciones/` | Sí | `Plantaciones_schema` | `Plants_mp` (dueño = user del token) |
| PATCH | `/api/Plantaciones/` | Sí + ownership | `Plantaciones_schema` | `Plants_mp` |
| DELETE | `/api/Plantaciones/{id}` | Sí + ownership | — | 204 |

## Roles
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Roles/` | No | — | `list[Roles]` |
| GET | `/api/Roles/{id}` | No | — | `Roles` |
| POST | `/api/Roles/` | Sí | `Roles_schema` | `Roles` |
| PATCH | `/api/Roles/` | Sí | `Roles_schema` | `Roles` |
| DELETE | `/api/Roles/{id}` | Sí | — | 204 |

## RecordatoriosCuidados (modelo `RecordCui`) — filtra por dueño (vía plantación)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/RecordatoriosCuidados/?plantacion_id={id}` | Sí + ownership | query `plantacion_id` | `list[RecordCui]` |
| POST | `/api/RecordatoriosCuidados/` | Sí + ownership | `RecordatorioCuidado_schema` | `RecordCui` |
| PATCH | `/api/RecordatoriosCuidados/{id}/cumplido` | Sí + ownership | — | `RecordCui` con `proxima_fecha` recalculada (+`frecuencia_dias`) |
| DELETE | `/api/RecordatoriosCuidados/{id}` | Sí + ownership | — | 204 |

## SintomasPlanta (modelo `Sintoma_Planta`)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/SintomasPlanta/?planta_id={id}` | No | query `planta_id` opcional | `list[Sintoma_Planta]` (filtra por planta si viene el query) |
| GET | `/api/SintomasPlanta/{id}` | No | — | `Sintoma_Planta` |
| POST | `/api/SintomasPlanta/` | Sí | `SintomaPlanta_schema` | `Sintoma_Planta` |
| PATCH | `/api/SintomasPlanta/` | Sí | `SintomaPlanta_schema` | `Sintoma_Planta` |
| DELETE | `/api/SintomasPlanta/{id}` | Sí | — | 204 |

## Alertas (agregador, sin Model/Schema propios)
| Método | Path | Auth | Entrada | Salida |
|---|---|---|---|---|
| GET | `/api/Alertas/?dias_proximos=3` | Sí | query `dias_proximos` (default 3) | `list[RecordCui]` vencidos/próximos de todas las plantaciones del usuario |

## Notas
- Varios `response_model` devuelven el modelo SQLModel de tabla directo
  (`Plants_mp`, `Plags`, `Plagsxplants`, `RecordCui`, `Sintoma_Planta`,
  `Roles`) en vez de un schema de salida — ver riesgo conocido en `SPEC.md`.
- Errores HTTP: 400/404/409/401/500 vía `Exceptions/` +
  `exception_handler_middleware.py`; 429 (rate limit) vía
  `TooManyRequestsException` en `signIn`/`signUp`.
