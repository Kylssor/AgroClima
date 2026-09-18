# Especificación: AgroClima

Este documento es la fuente de verdad del proyecto: lo que esté acá manda
sobre cualquier otra referencia. Si algo no está definido, conviene
resolverlo y documentarlo acá antes de implementarlo.

## Visión
App para que un campesino (con una o varias plantaciones, de cualquier
tamaño) registre qué cultivos tiene y reciba, sin tener que pedirlo:
- **Recordatorios** de los cuidados regulares que ese cultivo necesita
  (riego, fertilización, etc.).
- **Recomendaciones** para resolver lo que vea en la planta (ej. "está
  marchita") consultando la ficha de esa planta.
- **Prevención de plagas** específicas de cada tipo de planta.

La pantalla principal de la app son las **alertas pendientes**, no un
dashboard de progreso ni una bitácora de crecimiento.

## Entidades

### User
id, nombre, apellido, email (único), password_hash, ciudad_o_region,
creado_en.
- `ciudad_o_region` es la ubicación general que el usuario configura una
  vez (no por plantación) — queda lista para cuando se integre clima.

### Planta (catálogo)
id, nombre, descripción, instrucciones_cultivo, frecuencia_riego_dias,
condiciones_ideales, creado_en.
- Es el catálogo de tipos de planta (ya existe parcialmente como
  `Plantas`/`Plantas_Cat`); hay que confirmar/completar los campos de
  cuidado.

### SintomaPlanta (nueva)
id, planta_id (Planta), sintoma, diagnostico, recomendacion.
- La "mini FAQ" por tipo de planta: el usuario busca un síntoma (ej.
  "hojas amarillas") y obtiene diagnóstico + qué hacer.

### Plaga
id, nombre, descripción, recomendacion_prevencion.
- Ya existe como `Plagas`. Confirmar que tenga el texto de prevención, no
  solo la descripción de la plaga.

### PlagaPlanta (relación N:M)
plaga_id, planta_id.
- Ya existe como `PlagXPlants`/`PlagxPlants` (nota: el repo usa casing
  inconsistente entre carpetas — documentado en `docs/referencias/mapa.md`,
  no es un error a "corregir" sin avisar).

### Plantacion
id, usuario_id (User, dueño), planta_id (Planta), nombre_opcional,
fecha_registro.
- Es lo que el usuario "tiene": una instancia de un tipo de Planta que le
  pertenece. Un usuario puede tener 0, 1 o muchas.
- Hereda la ubicación del `User` dueño (no tiene ubicación propia en v1).

### RecordatorioCuidado
id, plantacion_id (Plantacion), tipo_cuidado (riego / fertilizacion /
poda / otro), frecuencia_dias, proxima_fecha, activo.
- Hoy el modelo existe (`RecordatoriosCuidados`) pero sin service ni
  controller — hay que darle lógica completa.

## Reglas de negocio mínimas
- Un usuario solo ve y gestiona sus propias plantaciones y los
  recordatorios asociados a ellas.
- Las "alertas pendientes" (home) son los `RecordatorioCuidado` con
  `proxima_fecha <= hoy`, de todas las plantaciones del usuario
  autenticado.
- Al marcar un recordatorio como cumplido, se recalcula `proxima_fecha`
  sumando `frecuencia_dias`.
- Buscar un síntoma en una `Planta` devuelve su recomendación y, si el
  síntoma corresponde a una plaga conocida (vía `PlagaPlanta`), también la
  prevención de esa plaga.

## Endpoints (backend) — estado real
```
POST   /api/auth/signUp
POST   /api/auth/signIn                        → devuelve JWT
POST   /api/auth/signOut
POST   /api/auth/checkSession

GET    /api/Plantas                            → catálogo de tipos de planta
GET    /api/Plantas/{id}

GET    /api/SintomasPlanta?planta_id={id}      → ficha de síntomas/recomendaciones de una planta [HECHO]
GET    /api/SintomasPlanta/{id}
POST   /api/SintomasPlanta                     [HECHO]
PATCH  /api/SintomasPlanta                     [HECHO]
DELETE /api/SintomasPlanta/{id}                [HECHO]

GET    /api/Plagas                             → catálogo de plagas
GET    /api/Plagas/{id}
GET    /api/Plagsxplants                       → plagas asociadas a plantas (con prevención)

GET    /api/Plantaciones                       → plantaciones del usuario autenticado [ahora sí filtra por dueño]
GET    /api/Plantaciones/{id}
POST   /api/Plantaciones                       → registrar plantación (elige un tipo de Planta)
PATCH  /api/Plantaciones
DELETE /api/Plantaciones/{id}

GET    /api/RecordatoriosCuidados?plantacion_id={id}   [HECHO]
POST   /api/RecordatoriosCuidados                       [HECHO]
PATCH  /api/RecordatoriosCuidados/{id}/cumplido         → marcar cumplido, reprograma proxima_fecha [HECHO]
DELETE /api/RecordatoriosCuidados/{id}                  [HECHO]

GET    /api/Alertas?dias_proximos=3            → recordatorios vencidos/próximos del usuario [HECHO, agregador]
```
Todas las rutas de escritura (`POST`/`PATCH`/`DELETE`) requieren sesión
(JWT). Las de `Plantaciones` y `RecordatoriosCuidados` además verifican
que el recurso pertenezca al usuario autenticado — si no, responden 401.

## Pantallas esperadas (frontend — todavía no existe código de frontend)
1. Login / Registro (incluye ciudad o región)
2. Alertas pendientes (home)
3. Mis plantaciones (lista) → detalle de una plantación con sus
   recordatorios y acceso a la ficha de su tipo de Planta
4. Ficha de Planta: instrucciones de cultivo, síntomas comunes, plagas que
   la afectan y cómo prevenirlas
5. Formulario para registrar una plantación nueva (elige tipo de Planta)

## Fuera de alcance (v1)
- Integración real con API de clima. Solo se deja el campo
  `ciudad_o_region` en `User` preparado para cuando se implemente.
- Seguimiento cuantitativo de crecimiento (medidas, fotos, series de
  tiempo). No es el objetivo del producto.
- Notificaciones push/email de los recordatorios (por ahora se consultan
  vía `GET /Alertas`).

## Riesgos de seguridad conocidos (pendientes, no bloqueantes para v1)
Detectados en una auditoría de seguridad, documentados a propósito para que
no se pierdan:
- **Sin roles/permisos**: cualquier usuario autenticado puede crear,
  editar o borrar los catálogos globales (`Roles`, `Plagas`, `PlagXPlants`,
  `SintomaPlanta`), que son compartidos por todos. El modelo `Roles` ya
  funciona (ver abajo) pero todavía no se usa para restringir nada — falta
  decidir cómo se asigna el primer administrador antes de construir el
  gate de permisos.
- Varios `response_model` devuelven directamente el modelo SQLModel de la
  tabla (`Plants_mp`, `Plags`, `Plagsxplants`, `RecordCui`,
  `Sintoma_Planta`, `Roles`) en vez de un schema de salida dedicado — hoy
  no exponen nada sensible, pero cualquier columna nueva que se agregue a
  esas tablas se expondría automáticamente sin decisión explícita.

Ya resueltos en esta iteración: contraseñas hasheadas, `JWT_SECRET_KEY`
fuera del código, CORS restringido, rate limiting básico en
`signIn`/`signUp`, y el bug de `Roles`/`User` que hacía imposible crear un
usuario contra Postgres real (FK circular `user.roles` ↔ `roles.user`
con ambos lados `NOT NULL` desde la migración original).

## Definición de "terminado" por área
- Backend: endpoint responde con el formato correcto, tiene manejo de
  errores básico (404, 401, 400/409 vía las excepciones ya existentes en
  `Exceptions/`), y tiene al menos una prueba.
- Frontend: pantalla renderiza, consume la API real (no datos
  hardcodeados), maneja estado de carga y error.
- Database: migración corre sin errores desde cero (`alembic upgrade
  head`).
- Docs: la documentación en `/docs` (y el README) explica cómo instalar y
  correr el proyecto desde cero, y `docs/referencias/mapa.md` está al día
  con la estructura real.
