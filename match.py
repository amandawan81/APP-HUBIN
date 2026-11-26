# ==========================================
# SISTEMA DE MATCH
# ==========================================

from arquivos import carregar_dados, salvar_dados
from empresa import buscar_empresa
from interacoes import buscar_interacao
from vagas import buscar_vaga, vaga_da_empresa


def candidato_gostou(dados, candidato_email, vaga_id):
    interacao = buscar_interacao(dados, candidato_email, vaga_id)
    if interacao is not None:
        return interacao["decisao"] == "gostei"

    # Perfis antigos guardavam favoritos antes da lista de interações.
    for candidato in dados["candidatos"]:
        if candidato["email"] == candidato_email and "favoritas" in candidato:
            return vaga_id in candidato["favoritas"]
    return False


def buscar_interesse(dados, empresa_email, candidato_email, vaga_id):
    if "interesses_empresas" in dados:
        for interesse in dados["interesses_empresas"]:
            if (interesse["empresa_email"] == empresa_email
                    and interesse["candidato_email"] == candidato_email
                    and interesse["vaga_id"] == vaga_id):
                return interesse
    return None


# EMPRESA CURTE UM CANDIDATO
def empresa_interesse(usuario):
    dados = carregar_dados()
    lista_candidatos = []
    for candidato in dados["usuarios"]:
        if candidato["tipo"] == "Candidato":
            lista_candidatos.append(candidato)

    if not lista_candidatos:
        print("\nNenhum candidato encontrado.")
        return

    print("\n--- ESCOLHER CANDIDATO ---")
    numero = 0
    for candidato in lista_candidatos:
        numero += 1
        print(f"{numero} - {candidato['nome']}")
        for perfil in dados["candidatos"]:
            if perfil["email"] == candidato["email"] and "area" in perfil and perfil["area"]:
                print(f"Área de interesse: {perfil['area']}")
                break

    try:
        escolha = int(input("\nEscolha um candidato ou 0 para voltar: "))
    except ValueError:
        print("Digite um número válido!")
        return

    if escolha == 0:
        return
    if escolha < 1 or escolha > len(lista_candidatos):
        print("Opção inválida!")
        return

    email = usuario["email"]
    vagas = []
    for vaga in dados["vagas"]:
        if vaga_da_empresa(vaga, email) and ("ativa" not in vaga or vaga["ativa"]):
            vagas.append(vaga)
    if not vagas:
        print("\nVocê precisa de uma vaga ativa para registrar interesse.")
        return

    print("\n--- MINHAS VAGAS ATIVAS ---")
    for vaga in vagas:
        print(f"{vaga['id']} - {vaga['titulo']}")

    vaga = buscar_vaga(dados, usuario)
    if vaga is None:
        return
    if vaga not in vagas:
        print("Escolha uma vaga ativa.")
        return

    candidato_email = lista_candidatos[escolha - 1]["email"]
    vaga_id = vaga["id"]
    if buscar_interesse(dados, email, candidato_email, vaga_id) is not None:
        print("\nInteresse já registrado!")
        return

    if "interesses_empresas" not in dados:
        dados["interesses_empresas"] = []
    interesse = {
        "empresa_email": email,
        "candidato_email": candidato_email,
        "vaga_id": vaga_id,
        "confirmado": False
    }
    dados["interesses_empresas"].append(interesse)
    print("\nInteresse da empresa registrado!")
    verificar_match(dados, candidato_email, vaga_id)
    salvar_dados(dados)


# VERIFICAR INTERESSE MÚTUO
def verificar_match(dados, candidato_email, vaga_id):
    for vaga in dados["vagas"]:
        if vaga["id"] == vaga_id:
            break
    else:
        return

    if "email_empresa" not in vaga:
        return
    email = vaga["email_empresa"]
    interesse = buscar_interesse(dados, email, candidato_email, vaga_id)
    if interesse is None or interesse["confirmado"]:
        return
    if not candidato_gostou(dados, candidato_email, vaga_id):
        return

    interesse["confirmado"] = True
    print("\n==============================")
    print("       NOVO MATCH!")
    print("==============================")
    print("Os dois demonstraram interesse!")
    print("==============================")


# CONSULTAR MATCHES
def consultar_matches(usuario):
    dados = carregar_dados()
    email = usuario["email"]
    empresa = buscar_empresa(dados, email)
    nome_empresa = usuario["nome"]
    if empresa is not None:
        nome_empresa = empresa["nome"]

    print("\n--- MATCHES REALIZADOS ---")
    encontrou = False
    if "interesses_empresas" in dados:
        for interesse in dados["interesses_empresas"]:
            if interesse["empresa_email"] != email or not interesse["confirmado"]:
                continue
            for vaga in dados["vagas"]:
                if vaga["id"] == interesse["vaga_id"] and vaga_da_empresa(vaga, email):
                    candidato = interesse["candidato_email"]
                    for conta in dados["usuarios"]:
                        if conta["email"] == candidato:
                            candidato = conta["nome"]
                            break
                    encontrou = True
                    print("\n------------------------------")
                    print(f"Candidato: {candidato}")
                    print(f"Empresa: {nome_empresa}")
                    print(f"Vaga: {vaga['titulo']} (ID {vaga['id']})")
                    print("Status: MATCH CONFIRMADO")
                    print("------------------------------")
                    break

    if not encontrou:
        print("Nenhum match encontrado.")
