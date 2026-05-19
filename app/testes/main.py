#exemplo simples/sujo de uso de db.py
from app.testes.db import DBManager

database = DBManager("sqlite:///database.db")
def main_menu():
    while True:
        print("\nMENU PRINCIPAL")
        print("I - Adicionar indivíduo")
        print("B - Buscar indivíduo")
        print("C - Adicionar casamento")
        print("P - Adicionar parentesco")
        print("X - Sair")

        user_input = input("Digite: ").lower()

        match user_input:
            case "i":
                adicionar_individuo()
            case "b":
                buscar_individuo()
            case "c":
                casar()
            case "p":
                parentesco()
            case "exemplo":
                database.carregar_exemplo()
            case "x":
                return
            case _:
                print("Input não reconhecido!")

def adicionar_individuo():
    print("\nADICIONAR INDIVÍDUO")

    nome = input("Digite o nome do indivíduo: ")
    sobrenome = input("Digite o sobrenome do indivíduo: ")

    database.add_individuo(nome, sobrenome)
    print(f"Adicionado {nome} {sobrenome}.")
    return

def buscar_individuo():

    print("\nBUSCAR INDIVÍDUO")
    print("Deseja buscar pelo nome, sobrenome, ou ambos?")
    print("1-Nome")
    print("2-Sobrenome")
    print("3-Ambos")

    user_input = input("Digite: ")
    match user_input:
        case "1":
            nome = [input("Digite o nome do indivíduo: ")]
            sobrenome = None
        case "2":
            nome = None
            sobrenome = [input("Digite o sobrenome do indivíduo: ")]
        case "3":
            nome = [input("Digite o nome do indivíduo: ")]
            sobrenome = [input("Digite o sobrenome do indivíduo: ")]
        case _:
            print("Input não reconhecido!")
            return
    individuos = database.get_individuos(indi_nomes=nome, indi_sobrenomes=sobrenome)
    if not individuos:
        print("\nNenhum indivíduo encontrado.")
        return
    else:
        print("Encontrado:")
        for i, indi in enumerate(individuos):
            indi.nome
            indi.sobrenome
            print(f"{i} - {indi.nome} {indi.sobrenome}")

        print("Digite um número para acessar esse indivíduo.")
        print("Digite X para sair.")

    user_input = input("Digite: ")
    if user_input.lower() == "x":
        return
    int_input = int(user_input)
    if (int_input >=0) and (int_input < len(individuos)):
        acessar_individuo(individuos[int_input])
    else:
        print("Erro de input.")

def acessar_individuo(indi):
    print("\nINDIVÍDUO")
    print(indi.nome_sobrenome())

    casamentos = database.get_casamentos(indi)

    if not casamentos:
        print("Nunca casou")
    else:
        print("Casou com:")
        casado_ids = []
        for cas in casamentos:
            if cas.conjuge_a_id == indi.id:
                casado_ids.append(cas.conjuge_b_id)
            else:
                casado_ids.append(cas.conjuge_a_id)
        conjugues = database.get_individuos(casado_ids)


        for (conj, cas) in zip(conjugues, casamentos):
            print("  " + conj.nome_sobrenome())
            print("     Crianças: ", end="")
            for criança in database.get_crianças(pais=cas):
                print(criança.nome_sobrenome(), end=", ")
            print()

def casar():
    print("\nADICIONAR CASAMENTO")
    print("Indivíduos:")
    individuos = database.get_individuos()
    for i, indi in enumerate(individuos):
            indi.nome
            indi.sobrenome
            print(f"{i} - {indi.nome} {indi.sobrenome}")
    
    user_input = int(input("Digite o número do primeiro indivíduo a casar: "))
    if (user_input >=0) and (user_input < len(individuos)):
        conjuge_a = individuos[user_input]
    else:
        print("Erro de input.")
        return
    print("Casar " + conjuge_a.nome_sobrenome() + " à?")

    user_input = int(input("Digite o número do segundo indivíduo a casar: "))
    if (user_input >=0) and (user_input < len(individuos)):
        conjuge_b = individuos[user_input]
    else:
        print("Erro de input.")
        return
    database.add_casamento(conjuge_a, conjuge_b)
    print("Casado " + conjuge_a.nome_sobrenome() + " e " + conjuge_b.nome_sobrenome())

def parentesco():
    print("\nADICIONAR CASAMENTO")
    print("Indivíduos:")
    individuos = database.get_individuos()
    for i, indi in enumerate(individuos):
            indi.nome
            indi.sobrenome
            print(f"{i} - {indi.nome} {indi.sobrenome}")
    
    user_input = int(input("Digite o número do indivíduo cujos pais deseja adicionar: "))
    if (user_input >=0) and (user_input < len(individuos)):
        criança = individuos[user_input]
    else:
        print("Erro de input.")
        return
    print("Adicionar pais de " + criança.nome_sobrenome())


    individuos = database.get_individuos()
    for i, indi in enumerate(individuos):
            indi.nome
            indi.sobrenome
            print(f"{i} - {indi.nome} {indi.sobrenome}")


    user_input = int(input("Digite o número de um dos pais: "))
    if (user_input >=0) and (user_input < len(individuos)):
        pai_a = individuos[user_input]
    else:
        print("Erro de input.")
        return
    
    print("Adicionar pais de " + criança.nome_sobrenome())
    print(pai_a.nome_sobrenome() + " e:")
    user_input = int(input("Digite o número do(a) outro(a) pai(mãe): "))

    if (user_input >=0) and (user_input < len(individuos)):
        pai_b = individuos[user_input]
    else:
        print("Erro de input.")
        return
    
    cas = database.get_casamentos(pai_a,pai_b)
    if not cas:
        cas = database.add_casamento(pai_a, pai_b)
    else:
        cas = cas[0]

    database.add_criança(criança, cas)

main_menu()


    