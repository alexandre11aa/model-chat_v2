FROM python:3.11

# Variáveis de ambiente para controle de comportamento do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia os arquivos necessários para o contêiner
COPY model_chat /model_chat
COPY scripts /scripts

# Define o diretório de trabalho
WORKDIR /model_chat

# Instala dependências e configura permissões
RUN apt-get update && apt-get install -y netcat-openbsd

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /model_chat/requirements.txt && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts


ENV PATH="/scripts:/venv/bin:$PATH"

# Exponha a porta 8000 para a aplicação Django
EXPOSE 8000

CMD [ "commands.sh" ]