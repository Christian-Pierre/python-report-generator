FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    fonts-liberation \
    libffi-dev

# Criar pasta da aplicação
WORKDIR /app

# Copiar dependências e instalar
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar a aplicação
COPY app/ ./app

# Rodar o app
CMD ["python", "app/main.py"]
