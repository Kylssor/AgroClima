from dependency_injector import containers, providers

from Config.project_config import Project_config

from Models.Context.sqlalchemy_context import SqlalchemyContext
from Models.Plantas.plantas import Plantas
from Models.Plantas.plantas_Cat import Plantas_Cat
from Models.Repository.sqlalchemy_generic_repository import SqlAlchemyGenericRepository
from Models.Plagas.plagas import Plags
from Models.PlagXPlants.plagxplants import Plagsxplants
from Models.Plantaciones.plantaciones import Plants_mp
from Models.Token.token_blacklist import Token_blacklist
from Models.User.user import User
from Services.Auth.authentication_service import Authentication_service
from Services.Cryptography.token_service import Token_service
from Services.Plantas.plantas_service import Plantas_service
from Services.Plantas.plantasCat_service import PlantasCat_service
from Services.Plagas.plagas_service import Plagas_service
from Services.PlagxPlants.plagxplants_service import Plagxplants_service
from Services.User.user_service import User_service
from Services.Plantaciones.plantaciones_service import Plantaciones_service


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "Controllers.Auth.auth_controller",
            "Controllers.Plantas.plantasCat_controller",
            "Controllers.Plantas.plantas_controller",
            "Controllers.Plagas.plagas_controller",
            "Controllers.PlagXPlants.plagxplants_controller",
            "Controllers.Plantaciones.plantaciones_controller"
            
            
            
        ]
    )
    
    db = providers.Singleton(
        SqlalchemyContext,
        db_url = Project_config().DATABASE_URI
    )
    
    generic_repository_user = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=User
    )

    user_service = providers.Factory(
        User_service,
        repository=generic_repository_user
    )


    generic_repository_token = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Token_blacklist
    )

    token_service = providers.Factory(
        Token_service,
        repository=generic_repository_token
    )


    authentication_service = providers.Factory(
        Authentication_service,
        user_service=user_service,
        token_service=token_service
    )
    generic_repository_plantas_cat= providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Plantas_Cat
    )

    plantas_cat_service = providers.Factory(
        PlantasCat_service,
        repository=generic_repository_plantas_cat,
    )


    generic_repository_plantas = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Plantas
    )

    plantas_service = providers.Factory(
        Plantas_service,
        repository=generic_repository_plantas
    )
    
    generic_repository_plags = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Plags
    )

    plagas_service = providers.Factory(
        Plagas_service,
        repository=generic_repository_plags
    )
     
    generic_repository_plagsxplants = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Plagsxplants
    )

    plagsxplants_service = providers.Factory(
        Plagxplants_service,
        repository=generic_repository_plagsxplants
    )

    generic_repository_plantaciones = providers.Factory(
        SqlAlchemyGenericRepository,
        db_context=db.provided,
        entity=Plants_mp
    )

    plantaciones_service = providers.Factory(
        Plantaciones_service,
        repository=generic_repository_plantaciones
    )
