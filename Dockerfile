# Usa uma imagem oficial do Python, versão leve (slim)
FROM python:3.10-slim

# Define que a saída do Python não fique presa no buffer (ajuda nos logs do Docker)
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia todo o resto do seu código para dentro do contêiner
COPY . /app/