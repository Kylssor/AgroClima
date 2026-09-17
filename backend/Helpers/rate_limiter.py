import threading
import time
from collections import defaultdict

from Exceptions.too_many_requests_exception import TooManyRequestsException


class RateLimiter():
    """Limitador en memoria, por proceso: suficiente para un solo worker.
    Si el API llega a correr con varios workers/instancias, esto hay que
    moverlo a un store compartido (ej. Redis)."""

    def __init__(self, max_attempts: int, window_seconds: int):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()


    def check(self, key: str) -> None:
        now = time.time()
        with self._lock:
            attempts = self._attempts[key]
            attempts[:] = [t for t in attempts if now - t < self.window_seconds]

            if len(attempts) >= self.max_attempts:
                raise TooManyRequestsException(
                    "Demasiados intentos. Espera unos minutos antes de volver a intentarlo."
                )

            attempts.append(now)


    def reset(self, key: str) -> None:
        with self._lock:
            self._attempts.pop(key, None)
