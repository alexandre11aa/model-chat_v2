# Model Chat

Modelo de chat assíncrono baseado em microsserviços e estruturado em containers com a utilização do Docker. Nele é possível a troca de mensagens entre usuários em chats privados.

## Docker

Todo o aplicativo foi conteinerizado, sendo possível com os devidos ajustes rodar como teste através de comandos do Docker, e do Docker-compose. Para subir a aplicação em containers basta executar o comando que se segue no diretório raíz do projeto onde se encontra o arquivo *[docker-compose](https://github.com/alexandre11aa/model-chat_v2/tree/main/docker-compose.yml)*.

```Shell
$ sudo docker-compose up --build
```

## Backend

O Backend foi desenvolvido em Python, utilizando tecnologias como Django, Django Rest Framework, SocketIO, dentre outras que podem ser vistas no arquivo *[requirements](https://github.com/alexandre11aa/model-chat_v2/tree/main/backend/model-chat/requirements.txt)*. Para rodar um teste do aplicativo, recomenda-se adicionar à lista **CORS_ALLOWED_ORIGINS** presente no arquivo *[settings](https://github.com/alexandre11aa/model-chat_v2/tree/main/backend/model-chat/core/settings.py)* o IP utilizado no Frontend na porta 3000. Para descobrir qual IP inserir basta verificar o IPAddress do container com o comando que se segue.

```Shell
$ sudo docker inspect frontend | grep "IPAddress"
```

## Frontend

O Frontend foi desenvolvido em Typescript, utilizando tecnologias como Next.js, React.js, Tailwind, Shadcn, dentre outras que podem ser vistas no arquivo *[package](https://github.com/alexandre11aa/model-chat_v2/tree/main/frontend/model-chat/package.json)*. Para rodar um teste do aplicativo, recomenda-se alterar o **NEXT_PUBLIC_API_BASE_URL** no arquivo *[.env](https://github.com/alexandre11aa/model-chat_v2/tree/main/frontend/dotenv_files/.env)* para o IP utilizado no Backend na porta 8000. Para descobrir qual IP inserir basta verificar o IPAddress do container com o comando que se segue.

```Shell
$ sudo docker inspect backend | grep "IPAddress"
```

Após as devidas alterações, basta reconstuir os containers com os comandos que se seguem no diretório raíz do projeto onde se encontra o arquivo *[docker-compose](https://github.com/alexandre11aa/model-chat_v2/tree/main/docker-compose.yml)*.

```Shell
$ sudo docker stop $(docker ps -q)
$ sudo docker-compose down
$ sudo docker-compose up --build
```