
import os
from arquivos import carregar_dados, salvar_dados


def limpar_tela():
    """limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def cadastrar_usuario():
    """cadastra um novo usuário no sistema."""
    dados = carregar_dados()

    print("\n=== Cadastro de usuário ===")

    nome = input("Digite seu nome completo: ")
    email = input("Digite seu email: ").strip().lower()

    # verifica se o email já está cadastrado
    for usuario in dados["usuarios"]:
        if usuario["email"].lower() == email:
            print("Email já está cadastrado!")
            return

    senha = input("Digite sua senha: ")

    print("\n1 - Candidato")
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

    print("\nUsuário cadastrado com sucesso!")


def login_usuario():
    """realiza o login do usuário no sistema."""
    dados = carregar_dados()

    while True:
        limpar_tela()

        print("\n=== Login de usuário ===")

        email = input("Digite seu email: ").strip().lower()
        senha = input("Digite sua senha: ")

        for usuario in dados["usuarios"]:
            if usuario["email"] == email and usuario["senha"] == senha:
                print("\nLogin realizado com sucesso!")
                print(f"Bem-vindo(a), {usuario['nome']}!")

                return usuario["tipo"], usuario["email"]

        print("\nEmail ou senha incorretos!")

        opcao = input(
            "Pressione Enter para tentar novamente ou 0 para voltar: "
        )

        if opcao == "0":
            return None, None

