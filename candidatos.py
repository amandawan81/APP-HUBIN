from arquivos import carregar_dados, salvar_dados
from usuarios import limpar_tela


# campos do perfil, com o nome que aparece na tela
CAMPOS_PERFIL = {"nome": "Nome", "telefone": "Telefone", "cidade": "Cidade", "area": "Área de interesse",
                 "habilidades": "Habilidades", "experiencia": "Experiência"}


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
