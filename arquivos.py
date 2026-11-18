import json


def carregar_dados():
    """le e retorna os dados armazenados no JSON."""
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados

    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return {}

    except json.JSONDecodeError:
        print("Erro! O arquivo JSON está vazio ou inválido.")
        return {}


def salvar_dados(dados):
    """salva as informações recebidas no JSON."""
    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)