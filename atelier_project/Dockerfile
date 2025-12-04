FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Librerie di sistema per WeasyPrint o altre dipendenze
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libgobject-2.0-0 \
    libxml2 \
    libxslt1.1 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamo requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il resto del progetto
COPY . .

# Creiamo la cartella staticfiles (volume)
RUN mkdir -p /app/staticfiles

# Non facciamo collectstatic durante il build: lo faremo a runtime

CMD ["gunicorn", "atelier_project.wsgi:application", "--bind", "0.0.0.0:8000"]