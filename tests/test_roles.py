"""Regresión: 'roles.user'/'roles.rolesty' se llamaban 'user_id'/
'rolesty_id' en el modelo pero 'user'/'rolesty' en la base real, y
'user.roles' formaba una FK circular NOT NULL con 'roles.user' — así era
imposible crear un User o un Role desde cero. Ver backend/Models/User/user.py
y backend/Models/Roles/roles.py, y la migración 16bb9f2f8187.
"""
from Models.Roles.roles import Roles
from Models.Roles.rolesTy import RolesTy
from Models.User.user import User
from Schemas.Roles.roles_schema import Roles_schema
from Services.Roles.roles_service import Roles_service


def test_usuario_se_crea_sin_rol_asignado(repo_factory):
    repo_user = repo_factory(User)

    creado = repo_user.add(User(name="Juan", last_name="Perez", email="juan@test.com", password="hash"))

    assert creado.roles is None


def test_crear_un_role_asigna_user_y_rolesty_correctamente(repo_factory):
    repo_user = repo_factory(User)
    repo_rolesty = repo_factory(RolesTy)
    service = Roles_service(repo_factory(Roles))

    usuario = repo_user.add(User(name="Ana", last_name="Gomez", email="ana@test.com", password="hash"))
    tipo = repo_rolesty.add(RolesTy(name="Admin"))

    role = service.create(Roles_schema(name="Admin de Ana", user_id=usuario.id, rolesty_id=tipo.id))

    assert role.user == usuario.id
    assert role.rolesty == tipo.id
