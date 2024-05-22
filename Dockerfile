FROM postgres:latest

# Copiar o script SQL para o diretório de inicialização do PostgreSQL
COPY ./hellodiet_database.sql /docker-entrypoint-initdb.d/