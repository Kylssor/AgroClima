"""Auth: hashing de contraseñas (antes se guardaban y comparaban en texto
plano), validaciones de sign_up/sign_in, y el rate limiter básico contra
fuerza bruta en /auth/signIn y /auth/signUp.
"""
import pytest

from Exceptions.app_exception import AppException
from Exceptions.too_many_requests_exception import TooManyRequestsException
from Exceptions.unauthorized_exception import UnauthorizedException
from Helpers.rate_limiter import RateLimiter
from Models.Token.token_blacklist import Token_blacklist
from Models.User.user import User
from Schemas.Auth.sign_in_schema import Sign_in_schema
from Schemas.User.user_schema import User_schema
from Services.Auth.authentication_service import Authentication_service
from Services.Cryptography.token_service import Token_service
from Services.User.user_service import User_service


@pytest.fixture()
def auth_service(repo_factory):
    user_service = User_service(repo_factory(User))
    token_service = Token_service(repo_factory(Token_blacklist))
    return Authentication_service(user_service, token_service)


def test_sign_up_guarda_password_hasheada_no_en_texto_plano(auth_service):
    creado = auth_service.sign_up(User_schema(
        name="Juan", last_name="Perez", email="juan@test.com", password="miClaveSegura123",
    ))

    assert creado.password != "miClaveSegura123"
    assert creado.password.startswith("$2b$")


def test_sign_up_rechaza_email_duplicado(auth_service):
    auth_service.sign_up(User_schema(name="Juan", last_name="Perez", email="juan@test.com", password="x1234567"))

    with pytest.raises(AppException):
        auth_service.sign_up(User_schema(name="Otro", last_name="Nombre", email="juan@test.com", password="y1234567"))


def test_sign_up_rechaza_email_invalido(auth_service):
    with pytest.raises(AppException):
        auth_service.sign_up(User_schema(name="Juan", last_name="Perez", email="no-es-un-email", password="x1234567"))


def test_sign_in_con_password_correcta_devuelve_token(auth_service):
    auth_service.sign_up(User_schema(name="Juan", last_name="Perez", email="juan@test.com", password="miClaveSegura123"))

    token = auth_service.sign_in(Sign_in_schema(email="juan@test.com", password="miClaveSegura123"))

    assert isinstance(token, str) and len(token) > 10


def test_sign_in_rechaza_password_incorrecta(auth_service):
    auth_service.sign_up(User_schema(name="Juan", last_name="Perez", email="juan@test.com", password="miClaveSegura123"))

    with pytest.raises(UnauthorizedException):
        auth_service.sign_in(Sign_in_schema(email="juan@test.com", password="incorrecta"))


def test_sign_in_rechaza_email_no_registrado(auth_service):
    with pytest.raises(UnauthorizedException):
        auth_service.sign_in(Sign_in_schema(email="nadie@test.com", password="loquesea"))


def test_check_session_detecta_token_en_blacklist(auth_service):
    import asyncio

    auth_service.sign_up(User_schema(name="Juan", last_name="Perez", email="juan@test.com", password="miClaveSegura123"))
    token = auth_service.sign_in(Sign_in_schema(email="juan@test.com", password="miClaveSegura123"))

    user = asyncio.run(auth_service.check_session(token))
    assert user.email == "juan@test.com"

    auth_service.sign_out(token)

    with pytest.raises(UnauthorizedException):
        asyncio.run(auth_service.check_session(token))


def test_rate_limiter_bloquea_tras_el_maximo_de_intentos():
    limiter = RateLimiter(max_attempts=3, window_seconds=60)

    limiter.check("1.2.3.4:juan@test.com")
    limiter.check("1.2.3.4:juan@test.com")
    limiter.check("1.2.3.4:juan@test.com")

    with pytest.raises(TooManyRequestsException):
        limiter.check("1.2.3.4:juan@test.com")


def test_rate_limiter_no_mezcla_distintas_keys():
    limiter = RateLimiter(max_attempts=1, window_seconds=60)

    limiter.check("1.2.3.4:juan@test.com")

    # Otra IP u otro email no debería verse afectado.
    limiter.check("5.6.7.8:juan@test.com")
    limiter.check("1.2.3.4:otro@test.com")
