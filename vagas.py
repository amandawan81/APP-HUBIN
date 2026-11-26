from arquivos import carregar_dados, salvar_dados
from usuarios import limpar_tela
from empresa import buscar_empresa

def escolher_modalidade():
    """mostra as modalidades e devolde a escolhida."""
    while True:
        print("\nModalidade: ")
        print("1 - Presencial")
        print("2 - Remoto")
        print("3 - Hibrido")

        opcao = input("Escolha uma modalidade: ")

        if opcao == "1":
            return "Presencial"
        elif opcao == "2":
            return "Remoto"
        elif opcao == "3":
            return "Hibrido"
        else:
            print("Opcao invaalida!")

def escolher_contrato():
    """mostra os tipos de contrato e devolve o escolhido."""
    while True:
        print("\nTipo de contrato: ")
        print("1 - CLT")
        print("2 - PJ")
        print("3 - Estagio")

        opcao = input("Escolha u tipo de contrato: ")

        if opcao == "1":
            return "CLT"
        elif opcao == "2":
            return "PJ"
        elif opcao == "3":
            return "Estagio"
        else:
            print("Opcao invalida!")

def ler_salario():
    """pede o salario ate a pessoa digitar um numero."""
    while True:
        try:
            salario = float(input("Salario em RS: (use ponto, ex: 2500.50): "))
            return salario

        except ValueError:
            print("Erro! Digite apenas numeros, com ponto no lugar da virgula.")

def gerar_id(dados):
    """Devolve o próximo ID livre: o maior ID já usado + 1."""
    maior_id = 0

    # procura o maior ID entre as vagas existentes
    if "vagas" in dados:
        for vaga in dados["vagas"]:
            if "id" in vaga and isinstance(vaga["id"], int):
                if vaga["id"] > maior_id:
                    maior_id = vaga["id"]

    # vagas apagadas podem deixar IDs nas interações, então olha elas também
    if "interacoes" in dados:
        for interacao in dados["interacoes"]:
            if "vaga_id" in interacao and isinstance(interacao["vaga_id"], int):
                if interacao["vaga_id"] > maior_id:
                    maior_id = interacao["vaga_id"]

    return maior_id + 1

def mostrar_vaga(vaga):
    """imprime os dados de uma vaga."""
    print("\n--------------------------------")
    print("id:", vaga["id"])
    print("Titulo:", vaga["titulo"])
    print("Area:", vaga["area"])
    print("Modalidade:", vaga["modalidade"])
    print("Contrato:", vaga["contrato"])
    print("Cidade:", vaga["cidade"])
    print("Salario: RS", vaga["salario"])
    print("Descricao:", vaga["descricao"])

def publicar_vaga(usuario):
    """CREATE: cadastra uma vaga nova."""
    dados = carregar_dados()

    empresa = buscar_empresa(dados, usuario["email"])
    if empresa is None:
        print("\nCadastre o perfil da empresa antes de publicar vagas (opcao 5).")
        return

    print("\n=== Publicar vaga ===")

    titulo = input("Titulo da vaga: ")
    area = input("Area: ")
    modalidade = escolher_modalidade()
    contrato = escolher_contrato()
    cidade = input("cidade: ")
    salario = ler_salario()
    descricao = input("Descricao: ")

    vaga = {
        "id": gerar_id(dados),
        "email_empresa": usuario["email"],
        "empresa": empresa["nome"],
        "titulo": titulo,
        "area": area,
        "modalidade": modalidade,
        "contrato": contrato,
        "cidade": cidade,
        "salario": salario,
        "descricao": descricao
    }

    dados["vagas"].append(vaga)
    salvar_dados(dados)

    print("\nVaga publicada com sucesso! id da vaga:", vaga["id"])


def vaga_da_empresa(vaga, email):
    return "email_empresa" in vaga and vaga["email_empresa"] == email


def listar_minhas_vagas(usuario):
    """READ: mostra so as vagas da empresa logada."""
    import os
    
    dados = carregar_dados()
    encontrou = False

    for vaga in dados["vagas"]:
        if vaga_da_empresa(vaga, usuario["email"]):
            mostrar_vaga(vaga)
            encontrou = True

    if encontrou == False:
        print("\nVoce ainda nao publicou nenhuma vaga.")

def buscar_vaga(dados, usuario):
    """pede o id e devolve a vaga, se ela for da empresa logada."""
    try:
        id_vaga = int(input("\nDigite o id da vaga: "))

    except ValueError:
        print("Erro! Digite apenas numeros.")
        return None
    for vaga in dados["vagas"]:
        if vaga["id"] == id_vaga and vaga_da_empresa(vaga, usuario["email"]):
            return vaga

    print("Vaga nao encontrada.")
    return None

def editar_vaga(usuario):
    """UPDATE: altera uma vaga. Enter em branco mantem o valor antigo."""
    listar_minhas_vagas(usuario)

    dados = carregar_dados()
    vaga = buscar_vaga(dados, usuario)

    if vaga is None:
        return

    print("\nAperte Enter sem digitar nada para manter o valor atual.\n")

    titulo = input(f"Titulo ({vaga['titulo']}): ")
    if titulo != "":
        vaga["titulo"] = titulo

    area = input(f"Area ({vaga['area']}): ")
    if area != "":
        vaga["area"] = area

    cidade = input(f"Cidade ({vaga['cidade']}): ")
    if cidade != "":
        vaga["cidade"] = cidade

    descricao = input(f"Descricao ({vaga['descricao']}): ")
    if descricao != "":
        vaga["descricao"] = descricao

    resposta = input("Deseja mudar a modalidade? (s/n): ").strip().lower()
    if resposta == "s":
        vaga["modalidade"] = escolher_modalidade()

    resposta = input("Deseja mudar o contrato (s/n): ").strip().lower()
    if resposta == "s":
        vaga["contrato"] = escolher_contrato()

    resposta = input("Deseja mudar o salario (s/n): ").strip().lower()
    if resposta == "s":
        vaga["salario"] = ler_salario()

    salvar_dados(dados)
    print("\nVaga atualizada com sucesso!")

def excluir_vaga(usuario):
    """DELETE: apaga uma vaga da empresa logada."""
    listar_minhas_vagas(usuario)

    dados = carregar_dados()
    vaga = buscar_vaga(dados, usuario)

    if vaga is None:
        return

    resposta = input(f"Tem certeza que deseja excluir '{vaga['titulo']}'? (s/n): ").strip().lower()

    if resposta == "s":
        dados["vagas"].remove(vaga)
        salvar_dados(dados)
        print("\nVaga excluida com sucesso!")
    else:
        print("\nExclusao cancelada!")

def menu_gerenciar_vagas(usuario):
    while True:
        limpar_tela()

        print("\n==== Gerenciar Vagas ====")
        print("1 - Listar minhas vagas")
        print("2 - Editar vaga")
        print("3 - Excluir vaga")
        print("0 - Voltar")

        opcao = input("\n Escolha uma opcao: ")

        if opcao == "1":
            listar_minhas_vagas(usuario)
        elif opcao == "2":
            editar_vaga(usuario)
        elif opcao == "3":
            excluir_vaga(usuario)
        elif opcao == "0":
            break
        else:
            print("\nOpcao nao encontrada no menu!")

        input("\nPressione Enter para continuar...")
