#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Espera o PostgreSQL estar pronto para aceitar conexões
wait_psql.sh

# Coleta os arquivos estáticos do Django
collectstatic.sh

# Executa as migrações do Django
migrate.sh

# Injeta os dados teste (OPCIONAL)
python manage.py shell < /scripts/datas/model_database.py

# Inicia o servidor de desenvolvimento do Django
runserver.sh