from arquivos import carregar_dados, salvar_dados
from usuarios import limpar_tela

def buscar_empresa(dados, email):
    """procura o perfil da empresa pelo email de login."""
    for empresa in dados["empresas"]:
        if empresa["email"] == email:
            return empresa

    return None

def ler_cnpj(dados):
    """pede o cnpj ate ser valido e nao repetido."""
    while True:
        cnpj = input("CNPJ ( so os 14 numeros, sem pontos e traco): ")

        try:
            int(cnpj)
        except ValueError:
            print("Erro! Digite apenas numeros. ")
            continue

        if len(cnpj) != 14:
           print("CNPJ invalido! Ele precisa ter 14 numeros. ")
           continue

        repetido = False
        for empresa in dados["empresas"]:
           if empresa["cnpj"] == cnpj:
                repetido = True

        if repetido:
            print("Este CNPJ ja esta cadastrado! ")
        else:
            return cnpj

def cadastrar_perfil_empresa(usuario):
    """cria o perfil da empresa logada"""
    dados = carregar_dados()
    if buscar_empresa(dados, usuario["email"]) is not None:
        print("\nSua empresa ja tem um perfil cadastrado. Use a opcao editar.")
        return

    print("\n=== Cadastro do perfil da empresa ===")

    nome = input("Nome da empresa: ")
    cnpj = ler_cnpj(dados)
    setor = input("Setor de atuacao: ")
    cidade = input("Cidade: ")
    descricao = input("Sobre a empresa: ")

    empresa = {
        "email": usuario["email"],
        "nome": nome,
        "cnpj": cnpj,
        "setor": setor,
        "cidade": cidade,
        "descricao": descricao
    }

    dados["empresas"].append(empresa)
    salvar_dados(dados)

    print("\nPerfil cadastrado com sucesso!")

def ver_perfil_empresa(usuario):
    """mostra o perfil da empresa logada"""
    dados = carregar_dados()
    empresa = buscar_empresa(dados, usuario["email"])

    if empresa is None:
        print("\nVoce ainda nao cadastrou o perfil dessa empresa.")
        return

    print("\n=== Perfil da empresa ===")
    print("nome:", empresa["nome"])
    print("cnpj:", empresa["cnpj"])
    print("setor:", empresa["setor"])
    print("Cidade:", empresa["cidade"])
    print("Sobre:", empresa["descricao"])

def editar_perfil_empresa(usuario):
    """altera o perfil. Enter em branco mantem o valor antigo."""
    dados = carregar_dados()
    empresa = buscar_empresa(dados, usuario["email"])

    if empresa is None:
        print("\nVoce ainda nao cadastrou o perfil da empresa.")
        return

    print("\n=== Editar perfil da empresa ===")
    print("Aperte Enter sem digitar nada para manter o valor atual. \n")

    nome = input(f"Nome ({empresa['nome']}): ")
    if nome != "":
        empresa["nome"] = nome

    setor = input(f"Setor ({empresa['setor']}): ")
    if setor != "":
        empresa["setor"] = setor

    cidade = input(f"Cidade ({empresa['cidade']}): ")
    if cidade != "":
        empresa["cidade"] = cidade

    descricao = input(f"Sobre ({empresa['descricao']}): ")
    if descricao != "":
        empresa["descricao"] = descricao

    salvar_dados(dados)

    print("\nPerfil atualizado com sucesso!")

def menu_perfil_empresa(usuario):
    while True:
        limpar_tela()

        print("\n==== Perfil Da Empresa ====")
        print("1 - Cadastrar perfil")
        print("2 - Ver perfil")
        print("3 - Editar perfil")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            cadastrar_perfil_empresa(usuario)

        elif opcao == "2":
            ver_perfil_empresa(usuario)

        elif opcao == "3":
            editar_perfil_empresa(usuario)

        elif opcao == "0":
            break

        else:
            print("\nOpcao nao encontrada no menu!")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    usuario_teste = {"email": "teste@empresa.com"}
    menu_perfil_empresa(usuario_teste)
