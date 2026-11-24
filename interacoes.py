"""Gerencia as decisões de swipe e as vagas favoritas dos candidatos."""

from arquivos import carregar_dados, salvar_dados
from candidatos import mostrar
from usuarios import limpar_tela


def carregar_interacoes(email):
    """Carrega os dados e migra favoritos antigos do perfil para a lista de interações."""
    dados = carregar_dados()
    if "interacoes" not in dados:
        dados["interacoes"] = []
    if "candidatos" not in dados:
        return dados

    for candidato in dados["candidatos"]:
        if candidato["email"] != email or "favoritas" not in candidato or not candidato["favoritas"]:
            continue

        # Migra os favoritos antigos sem sobrescrever decisões existentes.
        for id_vaga in candidato["favoritas"]:
            if buscar_interacao(dados, email, id_vaga) is None:
                dados["interacoes"].append({"candidato_email": email, "vaga_id": id_vaga, "decisao": "gostei"})
        candidato["favoritas"] = []
        salvar_dados(dados)
        break

    return dados


def buscar_interacao(dados, email, id_vaga):
    """Retorna a decisão do candidato para a vaga, ou None se ela ainda não existir."""
    for interacao in dados["interacoes"]:
        if interacao["candidato_email"] == email and interacao["vaga_id"] == id_vaga:
            return interacao
    return None


def vagas_por_id(dados):
    """Organiza as vagas por ID, usando a primeira se houver repetição."""
    vagas = {}
    if "vagas" not in dados:
        return vagas

    for vaga in dados["vagas"]:
        if "id" not in vaga:
            continue
        id_vaga = vaga["id"]
        if id_vaga is not None and id_vaga not in vagas:
            vagas[id_vaga] = vaga
    return vagas


def registrar_interacao(email, id_vaga, decisao):
    """Salva a primeira decisão válida para uma vaga existente, sem criar duplicatas."""
    if decisao != "gostei" and decisao != "nao gostei":
        return None

    dados = carregar_interacoes(email)
    if id_vaga not in vagas_por_id(dados):
        return
    if buscar_interacao(dados, email, id_vaga) is not None:
        return None

    dados["interacoes"].append({"candidato_email": email, "vaga_id": id_vaga, "decisao": decisao})
    salvar_dados(dados)


def mostrar_vaga(vaga):
    """Exibe os principais campos disponíveis de uma vaga no terminal."""
    campos = {"titulo": "Vaga", "empresa": "Empresa", "salario": "Salário", "modalidade": "Modalidade"}
    for campo in campos:
        if campo in vaga:
            print(campos[campo] + ":", vaga[campo])


def explorar_vagas(email):
    """Mostra vagas ativas ainda não avaliadas e registra gostei ou não gostei.

    Gostar adiciona aos favoritos, mas não envia candidatura. Retorna True
    quando as vagas acabam e False quando o candidato escolhe voltar."""
    limpar_tela()
    dados = carregar_interacoes(email)
    decisoes = {"D": "gostei", "E": "nao gostei"}
    vagas = vagas_por_id(dados)
    for id_vaga in vagas:
        vaga = vagas[id_vaga]
        if "ativa" in vaga and not vaga["ativa"]:
            continue
        if buscar_interacao(dados, email, id_vaga) is not None:
            continue

        print("\n=== Explorar vagas ===")
        mostrar_vaga(vaga)
        while True:
            opcao = input("\nD - Gostei | E - Não gostei | 0 - Voltar\nEscolha uma opção: ").strip().upper()
            if opcao == "0":
                return False
            if opcao in decisoes:
                break
            print("\nOpção inválida. Tente novamente.")

        registrar_interacao(email, id_vaga, decisoes[opcao])
        limpar_tela()
        if opcao == "D":
            print("\nVaga adicionada aos favoritos!")

    print("\nNão há mais vagas disponíveis para avaliar.")
    return True


def remover_favorita(email, id_vaga):
    """Apaga a decisão de gostar para que a vaga possa aparecer novamente."""
    dados = carregar_interacoes(email)
    interacao = buscar_interacao(dados, email, id_vaga)
    if interacao is not None and interacao["decisao"] == "gostei":
        dados["interacoes"].remove(interacao)
        salvar_dados(dados)


def vagas_favoritas(email):
    """Lista vagas marcadas com gostei e permite removê-las.

    Retorna True se a lista estiver vazia e False quando o candidato voltar."""
    while True:
        dados = carregar_interacoes(email)
        print("\n=== Vagas favoritas ===")
        opcoes = {}
        vagas = vagas_por_id(dados)
        for id_vaga in vagas:
            interacao = buscar_interacao(dados, email, id_vaga)
            if interacao is None or interacao["decisao"] != "gostei":
                continue
            vaga = vagas[id_vaga]
            numero = str(len(opcoes) + 1)
            opcoes[numero] = id_vaga
            print("\n" + numero + " -", mostrar(vaga, "titulo"))
            print("Empresa:", mostrar(vaga, "empresa"))

        if not opcoes:
            print("\nVocê não tem vagas favoritas para exibir.")
            return True

        opcao = input("\nDigite o número da vaga para remover ou 0 para voltar: ").strip()
        if opcao == "0":
            return False
        elif opcao in opcoes:
            remover_favorita(email, opcoes[opcao])
            print("\nVaga removida dos favoritos!")
        else:
            print("\nOpção inválida. Tente novamente.")
