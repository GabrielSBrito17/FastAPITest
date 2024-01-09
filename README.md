# FastAPI Project

Este é um projeto FastAPI com estrutura básica para um aplicativo web.

## Estrutura do Projeto

- **crud**: Módulos para operações CRUD no banco de dados.
- **database**: Configurações e inicialização do banco de dados.
- **models**: Definições de modelos de banco de dados.
- **routers**: Rotas do FastAPI.
- **schemas**: Esquemas Pydantic para validação de dados.
- **security**: Configurações de segurança e autenticação.
- **.env**: Arquivo de configuração do ambiente.
- **alembic.ini**: Configurações do Alembic para migrações de banco de dados.
- **docker-compose.yaml**: Configurações do Docker Compose.
- **Dockerfile**: Arquivo Docker para construir a imagem do aplicativo.
- **init.sql**: Script SQL de inicialização do banco de dados.
- **main.py**: Arquivo principal do FastAPI.
- **requirements.txt**: Dependências do Python.
- **test_main.http**: Arquivo para testar requisições HTTP com VSCode REST Client.

## Configuração do Ambiente

### Requisitos

* Python 3.11 ou superior
* Docker e Docker Compose

### Instalação e Execução

1. Clone o repositório:

```bash
git clone https://github.com/GabrielSBrito17/FastAPITest.git
cd FastAPITest
```
2. Execute o projeto usando o Docker Compose:
```
docker-compose up --build
```
## Rotas
### Criar SuperUsers
`POST /users/`
#### Parâmetros da Requisição
* Body: Deve conter os dados do novo usuário no formato JSON.

```
{
  "username": "novousuario",
  "email": "novousuario@example.com",
  "password": "senha123",
  "is_active": true,
  "is_superuser": false(alterar pra true para SuperUser)
}
```
### Autenticação

`POST /users/token`

Rota para obter um token de acesso.
#### Exemplo de Requisição utilizando o Postman:
```
1. Abra o Postman.

2. Selecione o método POST.

3. Insira a URL da sua aplicação com o caminho da rota /users/token.

4. Vá para a seção Body.

5. Selecione form-data.

6. Adicione duas chaves: username e password.

7. Defina os valores para as chaves. Por exemplo, para username,
você pode inserir um nome de usuário existente no seu sistema,
e para password, insira a senha correspondente.

8. Clique em "Send" para enviar a solicitação.
```
#### Retorno da requisição semelhando a isso:
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZSIsInNjb3BlcyI6WyJpc19zdXBlcnVzZXIiXSwiZXhwIjoxNzA0ODM3MjI3fQ.hzDpIMaTQy7dnTvC_6-cwDkoeLS2roVNBnHi3cblvbQ",
    "token_type": "bearer"
}
```
* *Esse token servirá para conseguir acessar os dados das demais rotas.*

### Listar todos os usuários cadastrados(somente SuperUser tem acesso):
`GET /users/all`
#### Parâmetros da Requisição
* Headers:
  - Authorization(Bearer Token): Token de acesso válido.

#### Retorno:
```
[
    {
        "username": "teste",
        "email": "teste@teste.com",
        "id": 1
    }
]
```

### Listar um usuário cadastrado(somente SuperUser tem acesso):
`GET /users/{user_id}`
#### Parâmetros da Requisição
* Headers:
  - Authorization(Bearer Token): Token de acesso válido.
* Parâmetros de Caminho:
  - user_id: ID do usuário a ser recuperado.
    
#### Retorno:
```
    {
        "username": "teste",
        "email": "teste@teste.com",
        "id": 1
    }
```
### Alterar campos de um usuário cadastrado(somente SuperUser tem acesso):
`PUT /users/{user_id}`
#### Parâmetros da Requisição
* Headers:
  - Authorization(Bearer Token): Token de acesso válido.
* Parâmetros de Caminho:
  - user_id: ID do usuário a ser recuperado.
* Corpo da Requisição:
  - UserUpdate:
    - email (opcional): Novo endereço de e-mail do usuário.
    - password (opcional): Nova senha do usuário.
    - is_active (opcional): Novo status de ativação do usuário.
    - is_superuser (opcional): Novo status de superusuário do usuário.
#### Corpo da requisição:
```
{
  "username": "usuario1",
  "email": "usuario1@example.com",
  "password":"teste",
  "is_active": true,
  "is_superuser": false
}
```
### Deletar um usuário cadastrado(somente SuperUser tem acesso):
`DELETE /users/{user_id}`
#### Parâmetros da Requisição
* Headers:
  - Authorization(Bearer Token): Token de acesso válido.
* Parâmetros de Caminho:
  - user_id: ID do usuário a ser recuperado.
