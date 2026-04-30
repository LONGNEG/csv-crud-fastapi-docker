"""
L'obiettivo: 
Stiamo costruire il Backend di un'applicazione. 
Creare un servizio che riceve richieste, elabora dati e risponde.
"""

#librerie
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import csv
import os

#creazione dell'oggetto app della classe FastAPI (che crea il server) definita nella libreria fastapi
app = FastAPI()

#dichiaro la costante a cui assegno il nome del file dell'archivio
CSV_FILE = "data.csv"

#creo classe che controlla i dati che siano giusti
class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str


# creo 2 funzioni, una che legge e una che scrive sul CSV, svolgendo quindi le operazioni CRUD
#funzione che legge
def read_csv():
    if not os.path.exists(CSV_FILE):
        return [] 

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


#funzione che scrive
def write_csv(rows):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "nome", "cognome", "codice_fiscale"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(rows) 





#ENDPOINTs

#primo endpoint con corrispettivo url
@app.post("/items/")
def create_item(item: Item):
    #cosa fa? esegue il codice dentro read_csv e salva il risultato in rows.
    rows = read_csv()

    # Controllo di sicurezza: verifichiamo che l'ID non sia già presente
    for r in rows:
        if int(r["id"]) == item.id:
            raise HTTPException(status_code=400, detail="ID già esistente")

    rows.append(item.dict())

    # allora chiamo la funzione write_csv per sovrascrivere i nuovi dati
    write_csv(rows)
    return item



#a questo endpoint è associata la restituzione delle righe
@app.get("/items/")
def get_items():
    return read_csv()



#a questo endpoint è associata l'operazione di conta
@app.get("/items/count")
def count_items():
    #legge le righe
    rows = read_csv()
    #e le conta
    return {"count": len(rows)}



#a questo endpoint è associata la ricerca di un valore tramite il suo id (che è variabile)
@app.get("/items/{item_id}")
def get_item(item_id: int):
    rows = read_csv()

    #se l'id è giusto me lo restituisce
    for r in rows:
        if int(r["id"]) == item_id:
            return r

    #se il ciclo finisce senza trovare nulla, lanciamo un errore 404
    raise HTTPException(status_code=404, detail="Elemento non trovato")



#a questo endpoint è associata l'update dei valori
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    rows = read_csv()

    #è impostato a false
    updated = False

    #se alla fine del ciclo diventa true allora lo sostituiamo
    for i, r in enumerate(rows):
        if int(r["id"]) == item_id:
            rows[i] = item.dict()
            updated = True
            break
    
    #altrimenti non esisteva e lanciamo l'errore
    if not updated:
        raise HTTPException(status_code=404, detail="Impossibile aggiornare: ID non trovato")

    write_csv(rows)
    return item



#a questo endpoint è associata l'eliminazione
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    rows = read_csv()
    #creiamo una nuova lista escludendo l'elemento con l'ID specificato
    new_rows = [r for r in rows if int(r["id"]) != item_id]

    #se la lunghezza non è cambiata, l'ID non esisteva
    if len(rows) == len(new_rows):
        raise HTTPException(status_code=404, detail="Impossibile eliminare: ID non trovato")

    write_csv(new_rows)
    return {"message": "Elemento eliminato con successo"}