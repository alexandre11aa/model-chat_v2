FROM python:3.11

# Variáveis de ambiente para controle de comportamento do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia os arquivos necessários para o contêiner
COPY backend/model-chat /model-chat
COPY backend/scripts /scripts

# Define o diretório de trabalho
WORKDIR /model-chat

# Instala dependências e configura permissões
RUN apt-get update && apt-get install -y netcat-openbsd default-mysql-client

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /model-chat/requirements.txt && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chmod -R 775 /data/web/static && \
  chmod -R 775 /data/web/media && \
  chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

# Exponha a porta 8000 para a aplicação Django
EXPOSE 8000

CMD [ "commands.sh" ]