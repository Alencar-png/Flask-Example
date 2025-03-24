# Flask Example

Este é um exemplo de API construída com [Flask](https://flask.palletsprojects.com/) que utiliza [Alembic](https://alembic.sqlalchemy.org/) para gerenciar as migrações do banco de dados. A documentação interativa da API é servida via Swagger UI, com a especificação centralizada no arquivo `docs/swagger.yaml`.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Executando a API](#executando-a-api)
- [Documentação da API](#documentação-da-api)
- [Migrações com Alembic](#migrações-com-alembic)
- [Atualizando a Documentação](#atualizando-a-documentação)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Pré-requisitos

- Python 3.10+ (recomendado)
- [pip](https://pip.pypa.io/en/stable/)
- Banco de dados MySQL (ou MariaDB)
- Ambiente virtual (virtualenv, venv, poetry, etc.)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/flask-example.git
   cd flask-example
   ```

2. Crie e ative seu ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Executando a API

Antes de iniciar o servidor, defina a variável de ambiente `FLASK_APP` conforme seu sistema operacional:

- **No Linux/macOS:**

  ```bash
  export FLASK_APP=main.py
  flask run
  ```

- **No Windows (cmd):**

  ```bash
  set FLASK_APP=main.py
  flask run
  ```

- **No Windows (PowerShell):**

  ```powershell
  $env:FLASK_APP = "main.py"
  flask run
  ```

A API estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Documentação da API

A documentação interativa da API pode ser acessada em:

- **Swagger UI:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)
- **Especificação OpenAPI:** [http://127.0.0.1:5000/openapi.yaml](http://127.0.0.1:5000/openapi.yaml)

Essas rotas estão organizadas em um blueprint dedicado, localizado na pasta `routers` (arquivo `routers/docs.py`).

## Migrações com Alembic

### Criar uma Migração Manualmente

Para criar uma nova migração manualmente, use o comando:

```bash
alembic revision -m "Descrição da Migração"
```

Este comando cria um novo arquivo de migração em branco, onde você pode definir as alterações no esquema do banco de dados.

### Criar uma Migração com Autogeração

Para gerar automaticamente uma migração baseada nas mudanças detectadas nos modelos, utilize:

```bash
alembic revision --autogenerate -m "Descrição da Migração"
```

Este comando compara o estado atual dos modelos com o estado do banco de dados e gera as instruções de migração necessárias.

### Aplicar a Migração Mais Recente

Para aplicar a última migração criada ao banco de dados, execute:

```bash
alembic upgrade head
```

Este comando aplica todas as migrações pendentes até a versão mais recente.

### Reverter a Última Migração

Se precisar desfazer a última migração aplicada, use:

```bash
alembic downgrade -1
```

Este comando reverte a última migração, retornando o banco de dados ao estado anterior.

## Atualizando a Documentação

Para manter a documentação da API atualizada:

1. **Ao criar um novo módulo (novo blueprint ou rotas):**
   - Atualize o arquivo `docs/swagger.yaml` para incluir as novas rotas, parâmetros e respostas.  
   - Utilize a [especificação OpenAPI](https://swagger.io/specification/) como referência para definir os novos endpoints e modelos.

2. **Após atualizar a especificação:**
   - Reinicie o servidor para que a nova documentação seja carregada.
   - Verifique a documentação interativa em [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs).

## Contribuição

Contribuições são bem-vindas! Se você deseja ajudar a melhorar o projeto, por favor:

1. Faça um fork do repositório.
2. Crie uma branch com sua feature ou correção: `git checkout -b minha-feature`
3. Faça commit das suas alterações: `git commit -m 'Minha nova feature'`
4. Envie para a branch: `git push origin minha-feature`
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

--- 