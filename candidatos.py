from arquivos import carregar_dados, salvar_dados
from usuarios import limpar_tela


# campos do perfil e da vaga com o nome mostrado na tela
CAMPOS_PERFIL = {"nome": "Nome", "telefone": "Telefone", "cidade": "Cidade",
                 "area": "Área de interesse", "habilidades": "Habilidades", "experiencia": "Experiência"}
CAMPOS_VAGA = {"empresa": "Empresa", "area": "Área", "cidade": "Cidade", "salario": "Salário",
               "requisitos": "Requisitos", "descricao": "Descrição"}


def texto(valor):
    """deixa listas e campos vazios prontos para exibir."""
    return (", ".join(valor) if isinstance(valor, list) else valor) or "Não informado"


def carregar_candidato(email, titulo):
    """carrega os dados e o perfil do candidato (criando no primeiro acesso) e mostra o título."""
    dados = {"usuarios": [], "candidatos": [], "vagas": [], "candidaturas": [], **carregar_dados()}
    candidato = next((c for c in dados["candidatos"] if c["email"] == email), None)
    usuario = next((u for u in dados["usuarios"] if u["email"] == email), None)

    if candidato is None and usuario is not None:
        candidato = {**dict.fromkeys(CAMPOS_PERFIL, ""), "nome": usuario["nome"], "email": email}
        dados["candidatos"].append(candidato)

    if candidato is None:
        print("\nCandidato não encontrado!")
    else:
        candidato.setdefault("favoritas", [])
        limpar_tela()
        print(f"\n=== {titulo} ===")
    return dados, candidato


def id_vaga(dados, vaga):
    """retorna o id da vaga, ou a posição dela se não tiver id."""
    return vaga.get("id", dados["vagas"].index(vaga) + 1)


def swipe(dados, candidato, vagas, vazio):
    """mostra as vagas uma por vez (estilo Tinder): curtir, favoritar ou passar."""
    if not vagas:
        print(f"\n{vazio}")
        return

    for numero, vaga in enumerate(vagas, start=1):
        limpar_tela()
        print(f"\n=== Vaga {numero} de {len(vagas)} ===\n{texto(vaga.get('titulo'))}")
        for campo, nome in CAMPOS_VAGA.items():
            print(f"{nome}: {texto(vaga.get(campo))}")

        codigo = id_vaga(dados, vaga)
        favorita = codigo in candidato["favoritas"]
        opcao = input(f"\n1 - Curtir (candidatar-se)\n2 - {'Desfavoritar' if favorita else 'Favoritar'}"
                      "\n3 - Passar\n0 - Parar\n\nEscolha uma opção: ").strip()

        if opcao == "0":
            break
        elif opcao == "1" and any(c["email_candidato"] == candidato["email"] and c["id_vaga"] == codigo
                                  for c in dados["candidaturas"]):
            print("\nVocê já se candidatou a esta vaga!")
        elif opcao == "1":
            dados["candidaturas"].append({
                "id": max((c.get("id", 0) for c in dados["candidaturas"]), default=0) + 1,
                "id_vaga": codigo, "titulo_vaga": vaga.get("titulo", ""), "empresa": vaga.get("empresa", ""),
                "email_candidato": candidato["email"], "nome_candidato": candidato["nome"], "status": "Em análise"})
            print("\nCandidatura realizada com sucesso!")
        elif opcao == "2" and favorita:
            candidato["favoritas"].remove(codigo)
            print("\nVaga removida das favoritas!")
        elif opcao == "2":
            candidato["favoritas"].append(codigo)
            print("\nVaga adicionada às favoritas!")
        else:
            continue  # 3 ou qualquer outra tecla passa para a próxima vaga

        salvar_dados(dados)
        input("\nPressione Enter para ver a próxima vaga...")

    print("\nFim das vagas!")


def explorar_vagas(email):
    """mostra as vagas abertas que o candidato ainda não curtiu, com filtro opcional."""
    dados, candidato = carregar_candidato(email, "Explorar vagas")
    if not candidato:
        return

    filtro = input("Filtrar por palavra (Enter para ver todas): ").strip().lower()
    curtidas = [c["id_vaga"] for c in dados["candidaturas"] if c["email_candidato"] == email]
    vagas = [v for v in dados["vagas"] if v.get("ativa", True) and id_vaga(dados, v) not in curtidas
             and filtro in " ".join(map(str, v.values())).lower()]
    swipe(dados, candidato, vagas, "Nenhuma vaga nova encontrada.")


def vagas_favoritas(email):
    """mostra as vagas favoritas do candidato no mesmo swipe."""
    dados, candidato = carregar_candidato(email, "Vagas favoritas")
    if candidato:
        vagas = [v for v in dados["vagas"] if id_vaga(dados, v) in candidato["favoritas"]]
        swipe(dados, candidato, vagas, "Você ainda não tem vagas favoritas.")


def minhas_candidaturas(email):
    """lista as candidaturas do candidato e permite cancelar uma delas."""
    dados, candidato = carregar_candidato(email, "Minhas candidaturas")
    if not candidato:
        return

    candidaturas = [c for c in dados["candidaturas"] if c["email_candidato"] == email]
    if not candidaturas:
        print("\nVocê ainda não se candidatou a nenhuma vaga.")
        return

    for numero, c in enumerate(candidaturas, start=1):
        print(f"{numero} - {c['titulo_vaga']} | {texto(c['empresa'])} | Status: {c['status']}")

    opcao = input("\nNúmero da candidatura para cancelar (0 para voltar): ").strip()
    if opcao.isdigit() and 1 <= int(opcao) <= len(candidaturas):
        if input("Confirmar cancelamento? (s/n): ").strip().lower() == "s":
            dados["candidaturas"].remove(candidaturas[int(opcao) - 1])
            salvar_dados(dados)
            print("\nCandidatura cancelada com sucesso!")
    elif opcao != "0":
        print("\nOpção não encontrada!")


def meu_perfil(email):
    """mostra o perfil do candidato e permite editar."""
    dados, candidato = carregar_candidato(email, "Meu perfil")
    if not candidato:
        return

    print(f"Email: {email}")
    for campo, nome in CAMPOS_PERFIL.items():
        print(f"{nome}: {texto(candidato.get(campo))}")
    if input("\n1 - Editar perfil\n0 - Voltar\n\nEscolha uma opção: ").strip() != "1":
        return

    print("\n(Pressione Enter para manter a informação atual)")
    for campo, nome in CAMPOS_PERFIL.items():
        novo = input(f"{nome} [{texto(candidato.get(campo))}]: ").strip()
        if novo:
            candidato[campo] = [h.strip() for h in novo.split(",")] if campo == "habilidades" else novo

    salvar_dados(dados)
    print("\nPerfil atualizado com sucesso!")
