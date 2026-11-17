import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    while True:
        limpar_tela()
        print("\n===== HUBIN =====")
        print("1 - Entrar como candidato")
        print("2 - Entrar como empresa")
        print("3 - Cadastrar-se")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("Menu do candidato")
        elif opcao == "2":
            print("Menu da empresa")
        elif opcao == "3":
            print("Cadastro")
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

menu_principal()
