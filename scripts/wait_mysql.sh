#!/bin/bash
# Verifica se o MySQL está acessível
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  echo "🟡 Waiting for MySQL Database Startup ($MYSQL_HOST:$MYSQL_PORT) ..."
  sleep 5
done

echo "✅ MySQL Database Started Successfully ($MYSQL_HOST:$MYSQL_PORT)"

# Verifica se o banco de dados 'my_database' existe
echo "Verificando se o banco de dados existe..."
MYSQL_CMD="mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_ROOT_PASSWORD"

# Cria o banco de dados, caso não exista
echo "Criando banco de dados 'my_database' se não existir..."
$MYSQL_CMD -e "CREATE DATABASE IF NOT EXISTS my_database;"