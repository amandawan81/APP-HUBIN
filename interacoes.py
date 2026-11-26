"""Gerencia as decisões de swipe e as vagas favoritas dos candidatos."""

from arquivos import carregar_dados, salvar_dados
from candidatos import mostrar
from match import verificar_match
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

    empresas = {empresa["email"]: empresa["nome"] for empresa in dados.get("empresas", [])}
    for vaga in dados["vagas"]:
        if "id" not in vaga:
            continue
        id_vaga = vaga["id"]
        if id_vaga is not None and id_vaga not in vagas:
            nome_empresa = empresas.get(vaga.get("email_empresa"))
            if nome_empresa:
                vaga = {**vaga, "empresa": nome_empresa}
            vagas[id_vaga] = vaga
    return vagas


def registrar_interacao(email, id_vaga, decisao, reavaliar=False):
    """Salva uma decisão para a vaga ou atualiza a existente em uma reavaliação."""
    if decisao != "gostei" and decisao != "nao gostei":
        return None

    dados = carregar_interacoes(email)
    if id_vaga not in vagas_por_id(dados):
        return
    interacao = buscar_interacao(dados, email, id_vaga)
    if interacao is None:
        dados["interacoes"].append({"candidato_email": email, "vaga_id": id_vaga, "decisao": decisao})
    elif reavaliar and interacao["decisao"] != decisao:
        interacao["decisao"] = decisao
    else:
        return
    if decisao == "gostei":
        verificar_match(dados, email, id_vaga)
    salvar_dados(dados)


def mostrar_vaga(vaga):
    """Exibe os principais campos disponíveis de uma vaga no terminal."""
    campos = {"titulo": "Vaga", "empresa": "Empresa", "salario": "Salário", "modalidade": "Modalidade"}
    for campo in campos:
        if campo in vaga:
            print(campos[campo] + ":", vaga[campo])


def explorar_vagas(email):
    """Mostra vagas ativas e oferece reavaliá-las ao chegar ao fim.

    Retorna True se não houver vagas ativas e False ao voltar para o menu.
    """
    limpar_tela()
    decisoes = {"D": "gostei", "E": "nao gostei"}
    reavaliar = False
    while True:
        dados = carregar_interacoes(email)
        vagas_ativas = {
            id_vaga: vaga for id_vaga, vaga in vagas_por_id(dados).items() if vaga.get("ativa", True)
        }
        if not vagas_ativas:
            print("\nNão há vagas ativas no momento.")
            return True

        for id_vaga, vaga in vagas_ativas.items():
            interacao = buscar_interacao(dados, email, id_vaga)
            if interacao is not None and not reavaliar:
                continue

            print("\n=== Explorar vagas ===")
            mostrar_vaga(vaga)
            favorita = interacao is not None and interacao["decisao"] == "gostei"
            opcao_rejeitar = "Não gostei (remover dos favoritos)" if favorita else "Não gostei"
            while True:
                opcao = input(f"\nD - Gostei | E - {opcao_rejeitar} | 0 - Voltar\nEscolha uma opção: ").strip().upper()
                if opcao == "0":
                    return False
                if opcao in decisoes:
                    break
                print("\nOpção inválida. Tente novamente.")

            registrar_interacao(email, id_vaga, decisoes[opcao], reavaliar=reavaliar)
            if opcao == "D":
                mensagem = "Esta vaga já está nos favoritos!" if favorita else "Vaga adicionada aos favoritos!"
                print(f"\n{mensagem}")
                input("\nPressione Enter para continuar...")

            limpar_tela()
            if opcao == "E" and favorita:
                print("\nVaga removida dos favoritos!")

        print("\nNão há mais vagas disponíveis para avaliar.")
        while True:
            opcao = input("\n1 - Rever todas as vagas | 0 - Voltar ao menu\nEscolha uma opção: ").strip()
            if opcao == "0":
                return False
            if opcao == "1":
                break
            print("\nOpção inválida. Tente novamente.")

        reavaliar = True
        limpar_tela()


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
