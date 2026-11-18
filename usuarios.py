
from arquivos import carregar_dados, salvar_dados
from menu_hubin import limpar_tela


def cadastrar_usuario():
    """cadastra um novo usuário no sistema."""
    dados = carregar_dados()

    print("\n=== Cadastro de usuario ===")

    nome = input("Digite seu nome completo: ")
    email = input("Digite seu email: ").strip().lower()

    for usuario in dados["usuarios"]:
        if usuario["email"].lower() == email:
            print("Email já esta cadastrado!")
            return
    

    senha = input("Digite sua senha: ")

    print("1 - Candidato")
    print("2 - Empresa")

    tipo = input("Escolha uma opção: ")

    if tipo == "1":
        tipo = "Candidato"
    elif tipo == "2":
        tipo = "Empresa"
    else:
        print("Opção inválida!")
        return

    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "tipo": tipo
    }

    dados["usuarios"].append(usuario)
    salvar_dados(dados)

    print("Usuário cadastrado com sucesso!")



def login_usuario():
    """realiza o login do usuário no sistema."""
    dados = carregar_dados()
    

    while True:
        print("\n=== Login de usuário ===")

        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")

        for usuario in dados["usuarios"]:
            if usuario["email"] == email and usuario["senha"] == senha:
                print(f"Login realizado com sucesso! Bem-vindo(a), {usuario['nome']}!")
                return usuario["tipo"]

        print("\nEmail ou senha incorretos!")
        print("aperte qualquer tecla para tentar novamente ou digite 0 para sair.")
        

        opcao = input("Escolha: ")
        limpar_tela()

        if opcao == "0":
            return None

