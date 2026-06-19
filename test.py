from app.models.database import init_db, SessionLocal
from app.controllers.individuo_controller import IndividuoController
from app.services.individuo_service import IndividuoService
from app.models.individuo import Individuo, IndividuoCreate
from app.services.individuo_evento_service import IndividuoEventoService
from pydantic import ValidationError

# x is None

# not x => não algo, qualquer dados vazio, {} [] false


# No nosso sistema genealógico, você provavelmente usará bastante ambos: is None para campos realmente opcionais e not ... para validar campos obrigatórios.


if __name__ == "__main__":  
    init_db()
    # ctrl=IndividuoController(SessionLocal)
    
    john={
        "nome": "João",
        "sobrenome": "Doria",
        "genero": "masculino",
        "eventos": {
            "dia": 1, 
            "mes": 2,
            "ano": 2000,
            "data_exata": True,
            "notas": "oi isso eh uma nota"
        }
    }
    # db=SessionLocal()
    try:
        service=IndividuoEventoService(SessionLocal)
        dados_validados=IndividuoCreate(**john)
        service.cadastro_indi_eventos(dados_validados)   
        # service.create_indiv_event(john)
            # validar dados
    except ValidationError as err:
            # erro capturado pelo pydantic
        raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")
    # finally:
    #     SessionLocal.close_all()
    
    
    
    
    
            #     "local": {
            #     "cidade": "Santa Maria",
            #     "estado": "Rio Grande do Sul",
            #     "regiao": "",
            #     "pais": "Brasil"
            # }
    
    
    
    
    # db=SessionLocal()
    # try:
    #     indi_service=IndividuoService(DBSessionMaker=db)
        
    #     joao={
    #         "nome": "joão",
    #         "sobrenome": "PARIZZOTTO",
    #         "genero": "masculino"
    #     }
        
    #     maria={
    #         "nome": "maria",
    #         "sobrenome": "PARIZZOTTO",
    #         "genero": "feminino"
    #     }
    
    #     # dados=[]
    #     individuos=[joao, maria]
        
        
    #     for individuo in individuos:
    #         indi_service.criar(**individuo)
        
        
    # finally:
    #     db.close()
        
# from app.models.database import init_db, SessionLocal
# from app.controllers.individuo_controller import IndividuoController
# from app.services.individuo_service import IndividuoService

# if __name__ == "__main__":  
#     init_db()
#     # ctrl=IndividuoController(SessionLocal)
    
#     db=SessionLocal()
#     try:
#         indi_service=IndividuoService(DBSessionMaker=db)
        
#         joao={
#             "nome": "joão",
#             "sobrenome": "PARIZZOTTO",
#             "genero": "masculino"
#         }
        
#         maria={
#             "nome": "maria",
#             "sobrenome": "PARIZZOTTO",
#             "genero": "feminino"
#         }
    
#         # dados=[]
#         individuos=[joao, maria]
        
        
#         for individuo in individuos:
#             indi_service.criar(**individuo)
        
        
#     finally:
#         db.close()
        
    
    
    
    
    
    
    # ctrl.criar("Felipe", "Andreoli", "masculino")
