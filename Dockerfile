#usa un'immagine base con Python
FROM python:3.11-slim

#imposta la cartella di lavoro nel container
WORKDIR /app

#copia il file requirements
COPY requirements.txt .

#installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

#copia tutto il progetto dentro il container
COPY . .

#espone la porta 8000
EXPOSE 8000

#comando per avviare FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]