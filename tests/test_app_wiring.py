"""Smoke test: la app completa (todos los controllers + el container de
dependency-injector) importa y monta todas las rutas sin errores. No abre
una conexión real a la base de datos (create_engine no conecta hasta el
primer query), así que no hace falta un Postgres real para esto.
"""


def test_la_app_monta_todas_las_rutas_esperadas():
    import main

    paths = {route.path for route in main.app.routes if hasattr(route, "path")}

    esperadas = {
        "/api/auth/signIn",
        "/api/auth/signUp",
        "/api/auth/signOut",
        "/api/auth/checkSession",
        "/api/Plantas/",
        "/api/Plagas/",
        "/api/Plagsxplants/",
        "/api/Plantaciones/",
        "/api/Roles/",
        "/api/RecordatoriosCuidados/",
        "/api/SintomasPlanta/",
        "/api/Alertas/",
    }

    faltantes = esperadas - paths
    assert not faltantes, f"Rutas esperadas que no se montaron: {faltantes}"
