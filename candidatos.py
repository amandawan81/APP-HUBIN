from arquivos import carregar_dados, salvar_dados
from usuarios import limpar_tela


# campos do perfil e da vaga, com o nome que aparece na tela
CAMPOS_PERFIL = {"nome": "Nome", "telefone": "Telefone", "cidade": "Cidade", "area": "Área de interesse",
                 "habilidades": "Habilidades", "experiencia": "Experiência"}
CAMPOS_VAGA = {"titulo": "Vaga", "empresa": "Empresa", "area": "Área", "cidade": "Cidade",
               "salario": "Salário", "requisitos": "Requisitos", "descricao": "Descrição"}


def mostrar(dicionario, campo):
    """retorna o valor do campo, ou "Não informado" se estiver vazio."""
    valor = dicionario.get(campo, "")
    if valor == "" or valor == []:
        return "Não informado"
    return valor


def carregar_candidato(email, titulo):
    """abre os dados, mostra o título e acha o perfil do candidato (cria no primeiro acesso)."""
    dados = carregar_dados()
    limpar_tela()
    print(f"\n=== {titulo} ===")
    for candidato in dados["candidatos"]:
        if candidato["email"] == email:
            return dados, candidato

    # primeiro acesso: cria o perfil com o nome usado no cadastro (usuarios.py)
    for usuario in dados["usuarios"]:
        if usuario["email"] == email:
            candidato = {"nome": usuario["nome"], "email": email, "telefone": "", "cidade": "", "area": "",
                         "habilidades": "", "experiencia": "", "favoritas": []}
            dados["candidatos"].append(candidato)
            return dados, candidato


def ja_curtiu(dados, email, id_vaga):
    """verifica se o candidato já curtiu (se candidatou) a vaga."""
    for candidatura in dados["candidaturas"]:
        if candidatura["email_candidato"] == email and candidatura["id_vaga"] == id_vaga:
            return True
    return False


def explorar_vagas(email):
    """mostra as vagas uma por vez (estilo Tinder): curtir, favoritar ou passar."""
    dados, candidato = carregar_candidato(email, "Explorar vagas")
    vagas = []
    for vaga in dados["vagas"]:
        if vaga.get("ativa", True) and not ja_curtiu(dados, email, vaga["id"]):
            vagas.append(vaga)

    numero = 0
    for vaga in vagas:
        numero += 1
        limpar_tela()
        print(f"\n=== Vaga {numero} de {len(vagas)} ===")
        for campo in CAMPOS_VAGA:
            print(f"{CAMPOS_VAGA[campo]}: {mostrar(vaga, campo)}")
        opcao = input("\n1 - Curtir (candidatar-se)\n2 - Favoritar / desfavoritar\n3 - Passar\n0 - Parar"
                      "\n\nEscolha uma opção: ").strip()

        if opcao == "0":
            break
        elif opcao == "1":
            candidatura = {"id_vaga": vaga["id"], "titulo_vaga": mostrar(vaga, "titulo"),
                           "empresa": mostrar(vaga, "empresa"), "email_candidato": email,
                           "nome_candidato": candidato["nome"], "status": "Em análise"}
            dados["candidaturas"].append(candidatura)
            print("\nVaga curtida! Candidatura enviada.")
        elif opcao == "2" and vaga["id"] in candidato["favoritas"]:
            candidato["favoritas"].remove(vaga["id"])
            print("\nVaga removida das favoritas!")
        elif opcao == "2":
            candidato["favoritas"].append(vaga["id"])
            print("\nVaga adicionada às favoritas!")
        else:
            continue  # 3 ou outra tecla: passa para a próxima vaga

        salvar_dados(dados)
        input("\nPressione Enter para ver a próxima vaga...")

    print("\nNão há mais vagas para mostrar.")


def meu_perfil(email):
    """mostra o perfil do candidato e permite editar."""
    dados, candidato = carregar_candidato(email, "Meu perfil")
    print(f"Email: {email}")
    for campo in CAMPOS_PERFIL:
        print(f"{CAMPOS_PERFIL[campo]}: {mostrar(candidato, campo)}")

    if input("\n1 - Editar perfil\n0 - Voltar\n\nEscolha uma opção: ").strip() != "1":
        return

    limpar_tela()
    print("\n=== Editar perfil ===")
    print("\n(Pressione Enter para manter a informação atual)")
    for campo in CAMPOS_PERFIL:
        novo = input(f"{CAMPOS_PERFIL[campo]}: ").strip()
        if novo != "":
            candidato[campo] = novo

    # mantém o nome igual no cadastro de usuários (usado no login)
    for usuario in dados["usuarios"]:
        if usuario["email"] == email:
            usuario["nome"] = candidato["nome"]

    salvar_dados(dados)
    limpar_tela()
    print("\nPerfil atualizado com sucesso!")
