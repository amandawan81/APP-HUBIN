"""Lê e grava os dados do aplicativo no arquivo JSON."""

import json
from pathlib import Path


ARQUIVO_DADOS = Path(__file__).resolve().with_name("dados.json")


def carregar_dados():
    """Lê dados.json e retorna um dicionário vazio se o arquivo faltar ou for inválido."""
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados

    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return {}

    except json.JSONDecodeError:
        print("Erro! O arquivo JSON está vazio ou inválido.")
        return {}


def salvar_dados(dados):
    """Grava o dicionário completo em dados.json, substituindo o conteúdo anterior."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
