"""Organiza a navegação do Hubin e direciona cada conta à sua área."""


from usuarios import cadastrar_usuario, login_usuario
from candidatos import meu_perfil
from empresa import menu_perfil_empresa
from interacoes import explorar_vagas, vagas_favoritas
from vagas import menu_gerenciar_vagas, publicar_vaga
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
    """Apresenta as opções de vagas, favoritos e perfil para o candidato autenticado."""
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
            if explorar_vagas(email):
                pausar()

        elif opcao == 2:
            print("\nAqui estarão suas candidaturas.")
            pausar()

        elif opcao == 3:
            if vagas_favoritas(email):
                pausar()

        elif opcao == 4:
            meu_perfil(email)
            pausar()

        elif opcao == 0:
            break

        elif opcao is not None:
            print("\nOpção não encontrada no menu!")
            pausar()


def menu_empresa(usuario):
    """Apresenta as opções da empresa autenticada."""
    while True:
        limpar_tela()

        print("\n===== ÁREA DA EMPRESA =====")
        print("1 - Publicar vaga")
        print("2 - Gerenciar vagas")
        print("3 - Perfil da empresa")
        print("0 - Voltar ao menu principal")

        opcao = ler_opcao()

        if opcao == 1:
            publicar_vaga(usuario)
            pausar()

        elif opcao == 2:
            menu_gerenciar_vagas(usuario)

        elif opcao == 3:
            menu_perfil_empresa(usuario)

        elif opcao == 0:
            break

        elif opcao is not None:
            print("\nOpção não encontrada no menu!")
            pausar()


def menu_principal():
    """Inicia a navegação, chama cadastro ou login e verifica o tipo de conta."""
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
            usuario = login_usuario()

            if usuario is None:
                continue
            if usuario["tipo"] == "Candidato":
                limpar_tela()
                menu_candidato(usuario["email"])

            elif usuario["tipo"] == "Empresa":
                print("\nVocê não pode acessar a área de candidato com uma conta de empresa.")
                pausar()

        elif opcao == 2:
            limpar_tela()
            usuario = login_usuario()

            if usuario is None:
                continue
            if usuario["tipo"] == "Empresa":
                limpar_tela()
                menu_empresa(usuario)

            elif usuario["tipo"] == "Candidato":
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
