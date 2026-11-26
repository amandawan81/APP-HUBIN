"""Registra o interesse das empresas e confirma matches por vaga."""

from arquivos import carregar_dados, salvar_dados
from vagas import buscar_vaga


def verificar_match(dados, candidato_email, vaga_id):
    """Confirma o match quando os dois lados demonstram interesse na mesma vaga."""
    decisao = next(
        (interacao["decisao"] for interacao in dados.get("interacoes", [])
         if interacao["candidato_email"] == candidato_email and interacao["vaga_id"] == vaga_id),
        None,
    )
    if decisao is None:
        # Perfis antigos podem guardar favoritos que ainda não foram migrados.
        favorita = any(
            candidato["email"] == candidato_email and vaga_id in candidato.get("favoritas", [])
            for candidato in dados.get("candidatos", [])
        )
        if favorita:
            decisao = "gostei"

    if decisao != "gostei":
        return

    for interesse in dados.get("interesses_empresas", []):
        if interesse["candidato_email"] == candidato_email and interesse["vaga_id"] == vaga_id:
            if not interesse["confirmado"]:
                interesse["confirmado"] = True
                print("\n===== NOVO MATCH! =====")
            return


def empresa_interesse(usuario):
    """Lista candidatos e permite registrar interesse para uma vaga da empresa."""
    dados = carregar_dados()
    candidatos = {
        str(numero): conta
        for numero, conta in enumerate(
            (conta for conta in dados["usuarios"] if conta["tipo"] == "Candidato"), 1
        )
    }
    if not candidatos:
        print("\nNenhum candidato encontrado.")
        return

    perfis = {perfil["email"]: perfil for perfil in dados["candidatos"]}
    print("\n--- CANDIDATOS ---")
    for numero, candidato in candidatos.items():
        print(f"{numero} - {candidato['nome']}")
        area = perfis.get(candidato["email"], {}).get("area")
        if area:
            print(f"Área de interesse: {area}")

    escolha = input("\nEscolha um candidato ou 0 para voltar: ").strip()
    if escolha == "0":
        return
    if escolha not in candidatos:
        print("Opção inválida!")
        return

    email = usuario["email"]
    vagas = [
        vaga for vaga in dados["vagas"]
        if vaga.get("email_empresa") == email and vaga.get("ativa", True)
    ]
    if not vagas:
        print("\nVocê precisa de uma vaga ativa para registrar interesse.")
        return

    print("\n--- MINHAS VAGAS ATIVAS ---")
    for vaga in vagas:
        print(f"{vaga['id']} - {vaga['titulo']}")

    vaga = buscar_vaga(dados, usuario)
    if vaga is None:
        return
    if not vaga.get("ativa", True):
        print("Escolha uma vaga ativa.")
        return

    candidato_email = candidatos[escolha]["email"]
    interesses = dados.setdefault("interesses_empresas", [])
    for interesse in interesses:
        if (interesse["empresa_email"] == email and interesse["vaga_id"] == vaga["id"]
                and interesse["candidato_email"] == candidato_email):
            print("\nInteresse já registrado!")
            return

    interesses.append({
        "empresa_email": email,
        "candidato_email": candidato_email,
        "vaga_id": vaga["id"],
        "confirmado": False,
    })
    print("\nInteresse da empresa registrado!")
    verificar_match(dados, candidato_email, vaga["id"])
    salvar_dados(dados)


def consultar_matches(usuario):
    """Mostra os matches confirmados das vagas da empresa autenticada."""
    dados = carregar_dados()
    email = usuario["email"]
    vagas = {vaga["id"]: vaga for vaga in dados["vagas"] if vaga.get("email_empresa") == email}
    nomes = {conta["email"]: conta["nome"] for conta in dados["usuarios"]}

    print("\n--- MATCHES REALIZADOS ---")
    encontrou = False
    for interesse in dados.get("interesses_empresas", []):
        vaga = vagas.get(interesse["vaga_id"])
        if interesse["empresa_email"] != email or not interesse["confirmado"] or vaga is None:
            continue

        encontrou = True
        candidato = interesse["candidato_email"]
        print(f"\nVaga: {vaga['titulo']} (ID {vaga['id']})")
        print(f"Candidato: {nomes.get(candidato, candidato)}")
        print("Status: MATCH CONFIRMADO")

    if not encontrou:
        print("Nenhum match encontrado.")
