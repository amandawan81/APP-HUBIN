
from usuarios import cadastrar_usuario, login_usuario
from candidatos import explorar_vagas, meu_perfil
import os


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa o programa até o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")


def ler_opcao():
    """Lê a opção digitada e trata entradas inválidas."""
    try:
        opcao = int(input("\nEscolha uma opção: "))
        return opcao

    except ValueError:
        print("\nErro! Digite apenas números.")
        pausar()
        return None


def menu_candidato(email):
    while True:
        limpar_tela()

        print("\n===== ÁREA DO CANDIDATO =====")
        print("1 - Explorar vagas")
        print("2 - Minhas candidaturas")
        print("3 - Vagas favoritas")
        print("4 - Meu perfil")
        print("0 - Voltar ao menu principal")

        opcao = ler_opcao()

        if opcao == 1:
            explorar_vagas(email)
            pausar()

        elif opcao == 2:
            print("\nAqui estarão suas candidaturas.")
            pausar()

        elif opcao == 3:
            print("\nAqui estarão suas vagas favoritas.")
            pausar()

        elif opcao == 4:
            meu_perfil(email)
            pausar()

        elif opcao == 0:
            break

        elif opcao is not None:
            print("\nOpção não encontrada no menu!")
            pausar()


def menu_empresa():
    while True:
        limpar_tela()

        print("\n===== ÁREA DA EMPRESA =====")
        print("1 - Publicar vaga")
        print("2 - Gerenciar vagas")
        print("3 - Ver candidatos")
        print("4 - Ver matches")
        print("5 - Perfil da empresa")
        print("0 - Voltar ao menu principal")

        opcao = ler_opcao()

        if opcao == 1:
            print("\nCadastro de vagas.")
            pausar()

        elif opcao == 2:
            print("\nGerenciamento das vagas.")
            pausar()

        elif opcao == 3:
            print("\nLista de candidatos.")
            pausar()

        elif opcao == 4:
            print("\nMatches da empresa.")
            pausar()

        elif opcao == 5:
            print("\nInformações da empresa.")
            pausar()

        elif opcao == 0:
            break

        elif opcao is not None:
            print("\nOpção não encontrada no menu!")
            pausar()


def menu_principal():
    while True:
        limpar_tela()

        print("\n========== HUBIN ==========")
        print("1 - Entrar como candidato")
        print("2 - Entrar como empresa")
        print("3 - Cadastrar-se")
        print("0 - Sair")

        opcao = ler_opcao()

        if opcao == 1:
            limpar_tela()
            tipo, email = login_usuario()

            if tipo == "Candidato":
                limpar_tela()
                menu_candidato(email)

            elif tipo == "Empresa":
                print("\nVocê não pode acessar a área de candidato com uma conta de empresa.")
                pausar()

        elif opcao == 2:
            limpar_tela()
            tipo, email = login_usuario()

            if tipo == "Empresa":
                limpar_tela()
                menu_empresa()

            elif tipo == "Candidato":
                print("\nVocê não pode acessar a área de empresa com uma conta de candidato.")
                pausar()

        elif opcao == 3:
            limpar_tela()
            cadastrar_usuario()
            pausar()

        elif opcao == 0:
            print("\nEncerrando o Hubin...")
            break

        elif opcao is not None:
            print("\nOpção não encontrada no menu!")
            pausar()


if __name__ == "__main__":
    menu_principal()