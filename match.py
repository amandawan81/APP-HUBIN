
# ==========================================
# SISTEMA DE MATCH
# ==========================================

candidatos = {}
empresas = {}

interesses_candidatos = set()
interesses_empresas = set()

matches = set()


# CADASTRO DE CANDIDATOS
def cadastrar_candidato():

    print("\n--- CADASTRO DE CANDIDATO ---")

    nome = input("Nome: ")
    profissao = input("Profissão: ")
    habilidades = input("Habilidades: ")

    candidatos[nome] = {
        "profissao": profissao,
        "habilidades": habilidades
    }

    print("\nCandidato cadastrado com sucesso!")

# CADASTRO DE EMPRESAS
def cadastrar_empresa():

    print("\n--- CADASTRO DE EMPRESA ---")

    nome = input("Nome da empresa: ")
    vaga = input("Nome da vaga: ")
    requisitos = input("Requisitos da vaga: ")

    empresas[nome] = {
        "vaga": vaga,
        "requisitos": requisitos
    }

    print("\nEmpresa cadastrada com sucesso!")


# CANDIDATO CURTE UMA EMPRESA
def candidato_interesse():

    if not candidatos or not empresas:
        print("\nCadastre candidatos e empresas primeiro!")
        return

    print("\n--- ESCOLHER VAGA ---")

    lista_empresas = list(empresas.keys())

    for i, empresa in enumerate(lista_empresas):
        print(f"{i + 1} - {empresa}")
        print(f"Vaga: {empresas[empresa]['vaga']}")

    try:
        escolha = int(input("\nEscolha uma empresa: ")) - 1

        if escolha < 0 or escolha >= len(lista_empresas):
            print("Opção inválida!")
            return

        nome_candidato = input("Nome do candidato: ")

        if nome_candidato not in candidatos:
            print("Candidato não encontrado!")
            return

        nome_empresa = lista_empresas[escolha]

        interesse = (nome_candidato, nome_empresa)

        if interesse in interesses_candidatos:
            print("Interesse já registrado!")
            return

        interesses_candidatos.add(interesse)

        print("\nInteresse do candidato registrado!")

        verificar_match(nome_candidato, nome_empresa)

    except ValueError:
        print("Digite um número válido!")


# EMPRESA CURTE UM CANDIDATO
def empresa_interesse():

    if not candidatos or not empresas:
        print("\nCadastre candidatos e empresas primeiro!")
        return

    print("\n--- ESCOLHER CANDIDATO ---")

    lista_candidatos = list(candidatos.keys())

    for i, candidato in enumerate(lista_candidatos):
        print(f"{i + 1} - {candidato}")
        print(f"Profissão: {candidatos[candidato]['profissao']}")

    try:
        escolha = int(input("\nEscolha um candidato: ")) - 1

        if escolha < 0 or escolha >= len(lista_candidatos):
            print("Opção inválida!")
            return

        nome_empresa = input("Nome da empresa: ")

        if nome_empresa not in empresas:
            print("Empresa não encontrada!")
            return

        nome_candidato = lista_candidatos[escolha]

        interesse = (nome_empresa, nome_candidato)

        if interesse in interesses_empresas:
            print("Interesse já registrado!")
            return

        interesses_empresas.add(interesse)

        print("\nInteresse da empresa registrado!")

        verificar_match(nome_candidato, nome_empresa)

    except ValueError:
        print("Digite um número válido!")


# VERIFICAR INTERESSE MÚTUO
def verificar_match(candidato, empresa):

    interesse_candidato = (candidato, empresa)
    interesse_empresa = (empresa, candidato)

    if (interesse_candidato in interesses_candidatos
            and interesse_empresa in interesses_empresas):

        match = (candidato, empresa)

        if match not in matches:

            matches.add(match)

            print("\n")
            print("==============================")
            print("       NOVO MATCH!")
            print("==============================")
            print(f"Candidato: {candidato}")
            print(f"Empresa: {empresa}")
            print("Os dois demonstraram interesse!")
            print("==============================")


# CONSULTAR MATCHES
def consultar_matches():

    print("\n--- MATCHES REALIZADOS ---")

    if not matches:
        print("Nenhum match encontrado.")
        return

    for candidato, empresa in sorted(matches):

        print("\n------------------------------")
        print(f"Candidato: {candidato}")
        print(f"Empresa: {empresa}")
        print("Status: MATCH CONFIRMADO")
        print("------------------------------")


# MENU PRINCIPAL
def menu():

    while True:

        print("\n================================")
        print("       MATCH DE EMPREGOS")
        print("================================")
        print("1 - Cadastrar candidato")
        print("2 - Cadastrar empresa")
        print("3 - Candidato demonstrar interesse")
        print("4 - Empresa demonstrar interesse")
        print("5 - Consultar matches")
        print("0 - Sair")
        print("================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_candidato()

        elif opcao == "2":
            cadastrar_empresa()

        elif opcao == "3":
            candidato_interesse()

        elif opcao == "4":
            empresa_interesse()

        elif opcao == "5":
            consultar_matches()

        elif opcao == "0":
            print("Encerrando o aplicativo...")
            break

        else:
            print("Opção inválida!")


# INICIAR PROGRAMA
menu()