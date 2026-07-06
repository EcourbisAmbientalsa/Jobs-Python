# Jobs Python

Projeto em Python para geração de relatórios e processamento de dados a partir de um banco SQL Server.

## Estrutura do projeto

- `main.py`: ponto de entrada principal.
- `core/`: componentes compartilhados do fluxo de execução.
  - `database.py`: configuração de conexão com o banco via `.env`.
  - `executor.py`: execução dos jobs.
  - `template.py`: base para os jobs.
- `jobs/`: implementações dos relatórios/jobs disponíveis.

## Requisitos

- Python 3.10+
- Dependências do projeto (instale com `pip install -r requirements.txt` se existir)
- Driver ODBC para SQL Server
- Arquivo `.env` com as configurações do banco

## Configuração

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
DB_SERVER=seu_servidor,porta
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_DRIVER=ODBC Driver 17 for SQL Server
```

## Como executar

Ative o ambiente virtual e rode:

```bash
python main.py
```

## Observações

- O arquivo `.env` não deve ser enviado para o Git.
- Os jobs usam a conexão centralizada em `core/database.py`.
