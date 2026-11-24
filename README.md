## 🚀 Como executar — Swipe e Vagas Favoritas

Esta branch (`feature/swipe-favoritos`) contém a implementação do sistema de swipe e favoritos do Hubin, desenvolvido em Python e utilizando JSON para armazenar os dados.

### 📌 Como executar o projeto

**1. Clone o repositório:**

```bash
git clone https://github.com/borella-dev/APP-HUBIN.git
cd APP-HUBIN
```

**2. Acesse a branch:**

```bash
git fetch origin
git switch feature/swipe-favoritos
```

**3. Execute o programa:**

```bash
python menu_hubin.py
```

O programa será iniciado no terminal. Não é necessário instalar bibliotecas externas.

### 👤 Como utilizar

No menu principal do Hubin:

1. Selecione `1 - Entrar como candidato`.
2. Faça login com uma conta de teste ou crie uma pela opção `3 - Cadastrar-se`.
3. Após o login, será exibido o menu do candidato.

**Menu do candidato:**

```text
===== ÁREA DO CANDIDATO =====

1 - Explorar vagas
2 - Minhas candidaturas
3 - Vagas favoritas
4 - Meu perfil
0 - Voltar ao menu principal
```

### 💜 Sistema de Swipe

Selecione a opção `1 - Explorar vagas`.

O sistema apresenta uma vaga por vez, mostrando informações como empresa, título, salário e modalidade.

O candidato poderá escolher:

- **D — Gostei:** salva a vaga nos favoritos.
- **E — Não gostei:** registra o desinteresse e passa para a próxima vaga.
- **0 — Voltar:** retorna ao menu do candidato.

Cada decisão é salva no arquivo `dados.json`.

As vagas já avaliadas não aparecem novamente para aquele candidato, evitando repetições.

**Importante:** gostar de uma vaga não significa enviar uma candidatura automaticamente.

### ❤️ Vagas Favoritas

Selecione a opção `3 - Vagas favoritas`.

O sistema exibirá as vagas que o candidato marcou com `D`.

É possível:

- Visualizar as vagas favoritas.
- Remover uma vaga digitando o número correspondente.
- Voltar ao menu digitando `0`.

Ao remover uma favorita, a interação correspondente é apagada, permitindo que a vaga apareça novamente no swipe.

### 🧪 Dados fictícios utilizados

Para testar as funcionalidades, foram adicionados dados de demonstração ao arquivo `dados.json`.

**Cadastros de teste:**

- 2 contas de candidato.
- 2 perfis de candidato.

**Vagas de exemplo:**

| ID | Empresa | Vaga |
|---|---|---|
| 1 | iFood | Estágio em Desenvolvimento de Software |
| 2 | Nubank | Analista de Dados Júnior |
| 3 | Banco do Brasil | Assistente Administrativo |
| 4 | Amazon | Analista de Logística Júnior |
| 5 | Mercado Livre | Estágio em Design de Produto |

Essas vagas são apenas exemplos para testar o funcionamento do Hubin e não representam oportunidades reais.

Cada vaga possui um `id` único para facilitar sua identificação no sistema.

**Interações de teste:**

Foram adicionadas três decisões de exemplo para uma conta de teste:

- Vaga 1: `gostei`
- Vaga 2: `nao gostei`
- Vaga 3: `gostei`

Essas decisões ficam armazenadas na lista `"interacoes"` do JSON.

### ✅ Como testar

1. Execute `python menu_hubin.py`.
2. Crie um novo candidato para começar sem decisões anteriores.
3. Entre na área do candidato.
4. Selecione `1 - Explorar vagas`.
5. Digite `D` em uma vaga para adicioná-la aos favoritos.
6. Digite `E` em outra vaga para registrar que não gostou.
7. Volte ao menu e selecione `3 - Vagas favoritas`.
8. Confira se a vaga curtida aparece na lista.
9. Remova uma favorita digitando seu número.
10. Volte a explorar vagas para verificar se ela aparece novamente.

Também é possível abrir o `dados.json` para observar as alterações registradas pelo sistema.

**Observação:** execute o programa a partir da pasta principal do projeto, onde está localizado o `dados.json`.

### 📁 Arquivos principais

| Arquivo | Função |
|---|---|
| `interacoes.py` | Implementação do swipe e favoritos |
| `menu_hubin.py` | Menus e navegação pelo terminal |
| `usuarios.py` | Cadastro e login |
| `candidatos.py` | Perfil do candidato |
| `arquivos.py` | Leitura e gravação do JSON |
| `dados.json` | Armazenamento dos dados |

### ⚠️ Observações

- O swipe funciona pelo terminal, utilizando as teclas D e E.
- O sistema não envia candidaturas automaticamente.
- As funcionalidades de publicação de vagas, candidaturas e match ainda dependem de outras etapas do desenvolvimento.
- Os dados de demonstração devem ser substituídos por informações inteiramente fictícias antes de compartilhar o projeto, sem e-mails, telefones ou senhas reais.