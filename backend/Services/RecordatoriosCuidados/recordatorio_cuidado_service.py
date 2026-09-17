import uuid
from datetime import datetime, timedelta, timezone

from Contracts.abc_generic_repository import AbcGenericRepository
from Exceptions.unauthorized_exception import UnauthorizedException
from Helpers.uuid_helper import Uuid_helper
from Models.Plantaciones.plantaciones import Plants_mp
from Models.RecordatoriosCuidados.recordCui import RecordCui
from Schemas.RecordatoriosCuidados.recordatorio_cuidado_schema import RecordatorioCuidado_schema


class RecordatorioCuidado_service():

    def __init__(
        self,
        repository: AbcGenericRepository[RecordCui],
        plantaciones_repository: AbcGenericRepository[Plants_mp],
    ):
        self.repository = repository
        self.plantaciones_repository = plantaciones_repository


    def _check_plantacion_ownership(self, plantacion_id: uuid.UUID, user_id: uuid.UUID) -> None:
        plantacion = self.plantaciones_repository.read_by_id(plantacion_id)
        if plantacion.user_id != user_id:
            raise UnauthorizedException("Esta plantación no te pertenece.")


    def get_by_plantacion(self, plantacion_id: uuid.UUID, user_id: uuid.UUID) -> list[RecordCui]:
        Uuid_helper.check_valid_uuid(plantacion_id)
        self._check_plantacion_ownership(plantacion_id, user_id)

        criterion = lambda: (RecordCui.plantacion_id == plantacion_id)
        return self.repository.read_by_options(criterion)


    def get_alertas(self, user_id: uuid.UUID, dias_proximos: int = 3) -> list[RecordCui]:
        criterion_plantaciones = lambda: (Plants_mp.user_id == user_id)
        plantaciones = self.plantaciones_repository.read_by_options(criterion_plantaciones)
        plantacion_ids = [plantacion.id for plantacion in plantaciones]

        if not plantacion_ids:
            return []

        limite = datetime.now(timezone.utc) + timedelta(days=dias_proximos)
        criterion = lambda: (
            RecordCui.plantacion_id.in_(plantacion_ids)
            & (RecordCui.activo == True)
            & (RecordCui.proxima_fecha <= limite)
        )
        return self.repository.read_by_options(criterion)


    def create(self, data: RecordatorioCuidado_schema, user_id: uuid.UUID) -> RecordCui:
        Uuid_helper.check_valid_uuid(data.plantacion_id)
        self._check_plantacion_ownership(data.plantacion_id, user_id)

        proxima_fecha = data.proxima_fecha or (
            datetime.now(timezone.utc) + timedelta(days=data.frecuencia_dias)
        )

        entity = RecordCui(
            plantacion_id=data.plantacion_id,
            tipo_cuidado=data.tipo_cuidado,
            frecuencia_dias=data.frecuencia_dias,
            proxima_fecha=proxima_fecha,
            activo=True,
        )

        return self.repository.add(entity)


    def marcar_cumplido(self, id: uuid.UUID, user_id: uuid.UUID) -> RecordCui:
        Uuid_helper.check_valid_uuid(id)

        recordatorio = self.repository.read_by_id(id)
        self._check_plantacion_ownership(recordatorio.plantacion_id, user_id)

        nueva_fecha = datetime.now(timezone.utc) + timedelta(days=recordatorio.frecuencia_dias)
        entity = RecordCui(id=id, proxima_fecha=nueva_fecha)

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID, user_id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)

        recordatorio = self.repository.read_by_id(id)
        self._check_plantacion_ownership(recordatorio.plantacion_id, user_id)

        return self.repository.delete_by_id(id)
