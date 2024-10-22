# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Instalar o Poetry
RUN pip install poetry

# Copiar o restante do código da aplicação
COPY . .

# Instalar as dependências do projeto
RUN poetry install

# Expor a porta em que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn seazone.main:app --host 0.0.0.0 --port 8000"]