# Desafio técnico - Seazone

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Testes](#testes)

## Instalação

### Clonando o Repositório

```bash
git clone git@github.com:CezarNegreiros/Sistema-reservas.git
cd .\Sistema-reservas\
```
## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis
```bash
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/database"
DATABASE_PASSWORD=password
DATABASE_USER=user
DATABASE_NAME=name
```
## Execução

### Buildando e Iniciando os Contêineres

Para construir as imagens Docker e iniciar a aplicação, execute:
```bash
docker-compose up --build
```
### Acessando a aplicação

Após inicializar, a aplicação estará disponível em:
- API: [localhost:8000](http://localhost:8000)
- Swagger: [localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [localhost:8000/redoc](http://localhost:8000/redoc)

## Testes
### Executando os testes

1. Acesse o container da aplicação:
```bash
docker-compose up -d  # executa os contêineres em segundo plano
docker-compose exec web bash
```
2. Execute os testes com o Pytest
```bash
poetry run pytest -v
```
3. Caso queira ver o coverage dos testes
```bash
poetry run pytest --cov=seazone.application.usecases test/
```
