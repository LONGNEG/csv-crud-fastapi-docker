# Usa un'immagine base con Python
FROM python:3.11-slim

# Imposta la cartella di lavoro nel container
WORKDIR /app

# Copia il file requirements
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il progetto dentro il container
COPY . .

# Espone la porta 8000
EXPOSE 8000

# Comando per avviare FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]