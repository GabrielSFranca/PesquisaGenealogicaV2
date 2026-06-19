"""
Script de teste para validação da tabela Uniao usando Pydantic
"""
from pydantic import ValidationError
from app.models.uniao import UniaoCreateSchema

def testar_uniao():
    """Testa vários cenários de validação da Uniao"""
    print("=" * 60)
    print("TESTES DE VALIDAÇÃO DA TABELA UNIAO COM PYDANTIC")
    print("=" * 60)
    # Teste 1: Dados válidos (casamento completo)
    print("\n[TESTE 1] Casamento completo com data:")
    try:
        dados1 = {
            "conjuge_id1": 1,
            "conjuge_id2": 2,
            "dia_casamento": 15,
            "mes_casamento": 5,
            "ano_casamento": 2000,
            "local_id": 1
        }
        uniao1 = UniaoCreateSchema(**dados1)
        print(f"✓ PASSOU: {uniao1}")
    except ValidationError as e:
        print(f"✗ FALHOU: {e.errors()[0]['msg']}")
    
    # Teste 2: Dados válidos (casamento sem data)
    print("\n[TESTE 2] Casamento sem data especificada:")
    try:
        dados2 = {
            "conjuge_id1": 3,
            "conjuge_id2": 4
        }
        uniao2 = UniaoCreateSchema(**dados2)
        print(f"✓ PASSOU: {uniao2}")
    except ValidationError as e:
        print(f"✗ FALHOU: {e.errors()[0]['msg']}")
    
    # Teste 3: IDs iguais (cônjuges diferentes)
    print("\n[TESTE 3] Validação: cônjuges devem ser diferentes:")
    try:
        dados3 = {
            "conjuge_id1": 5,
            "conjuge_id2": 5  # ERRO: mesma pessoa
        }
        uniao3 = UniaoCreateSchema(**dados3)
        print(f"✓ PASSOU: {uniao3}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    # Teste 4: Dia sem mês
    print("\n[TESTE 4] Validação: dia sem mês deve falhar:")
    try:
        dados4 = {
            "conjuge_id1": 6,
            "conjuge_id2": 7,
            "dia_casamento": 20,
            "ano_casamento": 2015
        }
        uniao4 = UniaoCreateSchema(**dados4)
        print(f"✓ PASSOU: {uniao4}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    # Teste 5: Data inválida no calendário
    print("\n[TESTE 5] Validação: data inválida no calendário:")
    try:
        dados5 = {
            "conjuge_id1": 8,
            "conjuge_id2": 9,
            "dia_casamento": 31,
            "mes_casamento": 2,  # Fevereiro não tem 31 dias
            "ano_casamento": 2020
        }
        uniao5 = UniaoCreateSchema(**dados5)
        print(f"✓ PASSOU: {uniao5}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    # Teste 6: Ano futuro
    print("\n[TESTE 6] Validação: ano futuro deve falhar:")
    try:
        dados6 = {
            "conjuge_id1": 10,
            "conjuge_id2": 11,
            "dia_casamento": 1,
            "mes_casamento": 1,
            "ano_casamento": 2099  # Futuro!
        }
        uniao6 = UniaoCreateSchema(**dados6)
        print(f"✓ PASSOU: {uniao6}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    # Teste 7: ID negativo
    print("\n[TESTE 7] Validação: ID deve ser positivo:")
    try:
        dados7 = {
            "conjuge_id1": -1,  # ERRO: ID negativo
            "conjuge_id2": 12
        }
        uniao7 = UniaoCreateSchema(**dados7)
        print(f"✓ PASSOU: {uniao7}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    # Teste 8: Mês inválido
    print("\n[TESTE 8] Validação: mês deve estar entre 1 e 12:")
    try:
        dados8 = {
            "conjuge_id1": 13,
            "conjuge_id2": 14,
            "dia_casamento": 5,
            "mes_casamento": 13,  # ERRO: 13 meses?
            "ano_casamento": 2010
        }
        uniao8 = UniaoCreateSchema(**dados8)
        print(f"✓ PASSOU: {uniao8}")
    except ValidationError as e:
        print(f"✗ FALHOU (esperado): {e.errors()[0]['msg']}")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("=" * 60)

if __name__ == "__main__":
    testar_uniao()
