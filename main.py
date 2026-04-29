#inanzitutto, cosa stiamo facendo? quali sono gli obiettivi di questo codice? in che modo il sito web che verrà creato verrà usato dall'utente? 
# quale tipo di utente lo usa? in quale contesto?
"""
L'obiettivo: 
Stiamo costruendo il "cervello" (il Backend) di un'applicazione. 
Questo codice crea un servizio che riceve richieste, elabora dati e risponde.
Chi lo usa e come?
L'utente: In questo caso non è un utente comune, ma un altro sviluppatore o un'altra parte di software (il "Frontend", come un'App o un sito) 
che ha bisogno di salvare o leggere dati di persone.

Contesto: Immagina un sistema di gestione dipendenti o un'anagrafica semplice. 
Invece di usare un database complesso, usiamo un file CSV come "archivio" economico e portatile.

"""

#1. questa è una "importazione selettiva" giusto? quale è il gergo tecnico di questa operazione?
"""
Importazione Selettiva: Il gergo tecnico è "Specific Import" (o semplicemente from-import). 
Si usa per caricare solo le classi/funzioni che servono, evitando di sprecare memoria caricando l'intera libreria.
"""
#2. cosa mi serve importare selettivamente FastAPI, HTTPException cosa fanno questi due "elementi" della libreria esattamente?
"""
FastAPI: È la classe che crea il server web. È il "motore" che ascolta le chiamate HTTP.
HTTPException: È uno strumento per generare errori standard del web (es: il famoso "404 Not Found"). Serve per dire all'utente: "Ehi, qualcosa è andato storto!".
"""
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
#cosa è csv e os? cosa fanno queste due librerie?
"""
csv: È una libreria standard di Python. Serve a leggere e scrivere file ".csv" (composti da righe e virgole) senza dover gestire manualmente le virgole e gli a capo.
os: Sta per Operating System. Serve a interagire con il tuo computer (es: controllare se un file esiste fisicamente sul disco).
"""
import csv
import os




# Creazione dell'istanza principale dell'applicazione FastAPI
# 1. in questa parte sto assegnando alla variabile app la funzione FastApi() ? mi serve per richiamarla più velocemente?
"""
Qui stai creando un oggetto (un'istanza). 
Non è solo per richiamarla velocemente, ma per configurare il server. 
"""
# 2. immagino che questa funzione non venga definita prima in quanto è importata da una libreria e quindi è già stata definita nella libreria, giusto?
"""
FastAPI() è il costruttore della classe definito nella libreria che hai importato.
"""
app = FastAPI()

# Nome del file fisico dove verranno salvati i dati
# 1. qui sto assegnando ad una variabile CSV_FILE un valore stringa: "data.csv"
"""
Questa è una costante. La dichiariamo all'inizio
"""
# 2. per quale motivo sto facendo questa assegnazione?
"""
così, se un domani decidessi di chiamare il file archivio_utenti.csv, dovrai cambiarlo solo in questa riga e non in tutte le funzioni del codice.
"""
CSV_FILE = "data.csv"






# =====================
# MODELLO DATI (SCHEMA)
# =====================
# Definiamo come deve essere fatto un "Item". 
# 1. creo una classe Item in cui passo come parametro BaseModel, cosa fa il parametro BaseModel?
"""
È una classe speciale di Pydantic. 
Quando la "erediti" (mettendola tra parentesi), dici a Python: 
"Questa classe non è solo un contenitore, ma deve controllare i dati".
"""
# 2. verrà usata da FastAPI per validare i dati inviati dall'utente?: a)cioè per verificare che i dati siano del tipo corretto int,str? b)quali dati invierà l'utente?
"""
Sì, verifica che se l'utente invia "id": "ciao", il sistema risponda automaticamente con un errore perché si aspettava un intero (int).
Dati inviati: L'utente invierà un oggetto JSON (un formato testuale simile a un dizionario Python) tramite il corpo della richiesta web.
"""
class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str












# =====================
# creo 2 funzioni, una che legge e una che scrive
# =====================

# creo una funzione read_csv() che legge i dati dal file CSV e li trasforma in una lista di dizionari Python (a cosa ci serve fare dei dizionari?)
"""
Nel CSV i dati sono stringhe separate da virgole. Il dizionario ci permette di accedere ai dati tramite nome: r["nome"] è molto più chiaro di r[1]
"""
def read_csv():
    # Se il file non esiste ancora, restituisce una lista vuota
    # chiariscimi questa scrittura: os.path.exists(CSV_FILE), 
    # 1. significa che passo a parametro CSV_FILE in un metodo path della libreria os? 
    # 2. perchè gli passo dentro CSV_FILE?
    """
    Passi il nome del file ("data.csv") al metodo exists che fa parte del sottomodulo path della libreria os.
    Serve a evitare che il programma crashi cercando di leggere un file che non hai ancora creato.
    """
    if not os.path.exists(CSV_FILE):
        return [] 

    # se invece il file esiste: with open (...) as ...: mi serve per l'apertura di un file con quella formattazione testuale e lo assegna alla variabile file.
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        # crea/dichaira variabile reader e le assegna il metodo DictReader della libreria csv passandogli dentro "file" (quindi è ricorsiva?)
        # usa la prima riga del CSV come chiavi del dizionario
        """
        Qui file è il file aperto, e reader è un oggetto creato in quel momento (inizializzato lì). Non è ricorsiva, è solo una variabile locale.
        """
        reader = csv.DictReader(file)
        # e gli restituisce la lista a cui passa dentro il parametro reader, da dove è uscito fuori questo parametro reader? 
        # mi ricordo che in altri linguaggi di programmazione tutto deve essere dichiarato/definito/inizializzato quindi reader da dove è stato preso?
        """
        DictReader restituisce un oggetto speciale (iteratore). Trasformandolo in list, otteniamo una lista di dizionari vera e propria, pronta all'uso.
        """
        return list(reader)





# creo una seconda funzione write_csv a cui passo dentro rows (da dove esce fuori questo parametro? lo sto dichiarando per la prima volta qui? cosa farà?)
"""
Questo parametro lo dichiari qui. Rappresenta "la lista di dati che vuoi salvare". Quando chiamerai la funzione, le passerai la lista aggiornata.
"""
# prende una lista di dizionari e sovrascrive il file CSV con i nuovi dati
def write_csv(rows):
    #apre il file CSV_FILE con quella formattazione e lo assegna alla variabile file
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        #crea una variabile di nome fieldnames e gli assegna una lista di stringhe 
        fieldnames = ["id", "nome", "cognome", "codice_fiscale"]
        #crea/dichiara una variabile di tipo writer assegnandole il metodo DictWriter della libreria csv passandogli dentro file e fieldnames=fieldnames (cos'è? perchè?)
        """
        È un argomento con nome. Dici a DictWriter: "Usa la lista che ho chiamato fieldnames come intestazione delle colonne".
        """
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        #della variabile writer creata prima usa il metodo writeheader che serve a scrivere la riga dei titoli (header) 
        writer.writeheader() 
        #della variabile writer creata prima usa il metodo writerows che scrive tutti i record
        writer.writerows(rows) 



"""
L'utente chiama l'URL.

FastAPI riceve i dati e li valida con Item.

Le tue funzioni read e write traducono quei dati tra il linguaggio Python (liste/dizionari) e il linguaggio del disco (file CSV).
"""









# =====================
# ENDPOINT API (ROTTE)
# =====================
"""
metodo di un dizionario = endpoint = indirizzo urls che api mette a disposizione
"""
""" quando qualcuno chiama l'indirizzo /items/ usando il metodo POST esegui la funzione create_item"""
#la chiocciola è il decoratore;
#dell'istanza app di FastAPI uso il metodo post a cui passo dentro la stringa "/items/" che mi indica il path nel quale vanno risposte le richieste post, giusto?
@app.post("/items/")
#creo la funzione create_item in cui dentro passo item, che mi aspetto sia di tipo Item (json e lo converte in item python)
def create_item(item: Item):
    #assegno alla variabile rows la funzione read_csv() 
    """
    rows = read_csv() esegue il codice dentro read_csv e salva il risultato in rows.
    """
    rows = read_csv()

    # Controllo di sicurezza: verifichiamo che l'ID non sia già presente
    #creo un ciclo for che cicla in rows
    for r in rows:
        #all'interno del ciclo creo una condizione per cui, se l'intero id nel dizionario r è uguale ad item.id allora manda un segnale di errore exception 
        if int(r["id"]) == item.id:
            raise HTTPException(status_code=400, detail="ID già esistente")

    #? all'oggetto di tipo lista rows aggiungiamo un singolo elemento alla fine con il metodo append, l'elemento è il dizionario dell'item, giusto? (perchè è barrato dict?)
    rows.append(item.dict())

    # allora chiamo la funzione write_csv per sovrascrivere i nuovi dati, giusto? quali dati?
    # passi la lista rows nella funzione write_csv e sovrascrive tutto il file data.csv.
    write_csv(rows)
    #restituisco l'oggetto item, giusto?
    return item

#dell'oggetto di tipo dizionario app uso il metodo get che mi resituisce il valore che ha come chiave "/items/", giusto?
"""
valore associato alla chiave = response = Quello che il server rimanda indietro al client.
"""
@app.get("/items/")
#definisco una funzione di tipo get_items() 
def get_items():
    #questa funzione mi restituisce la funzione read_csv che mi legge tutti i valori, giusto?
    return read_csv()

#dell'oggetto di tipo dizionario "app" uso il metodo get che mi restituisce il valore che appartiene alla chiave "/items/count"
@app.get("/items/count")
#creo una funzione count_items()
def count_items():
    #all'interno della funzione creo una variabile rows a cui è assegnata la fuznione read_csv(), perchè?
    """Perché per sapere quante righe ci sono nel CSV, devi prima leggerlo! Non essendoci un database attivo, 
    dobbiamo ogni volta aprire il file, contare gli elementi nella lista e restituire il numero.
    rows = read_csv() esegue il codice dentro read_csv e salva il risultato in rows.
    """
    rows = read_csv()
    #questa funzione mi restituisce il numero totale di righe ovvero len(rows) della chiave "count", giusto?
    return {"count": len(rows)}

#dell'oggetto app usa il metodo get che ottiene il valore associato alla chiave /iterms/{item_id}, giusto? ma perchè è nelle parentesi graffe {item_id}?
"""
Quelle si chiamano Path Parameters (parametri di percorso). Significa che quella parte dell'URL è variabile.

Se l'utente scrive /items/10, FastAPI capisce che 10 è l'ID e lo passa automaticamente alla tua funzione come variabile item_id.
"""
@app.get("/items/{item_id}")
#creo la funzione get_item a cui passo all'interno item_id che si aspetta ":" sia un numero intero, giusto?
def get_item(item_id: int):
    """OPERAZIONE: READ (ONE) - Cerca un record specifico tramite l'ID."""
    #alla variabile rows associo la funzione read_csv
    rows = read_csv()

    #faccio un ciclo for all'interno della variabile rows che contiene la funzione read_csv quindi di lettura del file csv
    for r in rows:
        #se l'id del dizionario r, convertito in intero è uguale alla variabile item_id allora restituisci r, giusto? 
        if int(r["id"]) == item_id:
            return r

    # Se il ciclo finisce senza trovare nulla, lanciamo un errore 404
    raise HTTPException(status_code=404, detail="Elemento non trovato")

#dell'oggetto app uso il metodo .put per inserire la chiave /items/{items_id}, giusto? 
@app.put("/items/{item_id}")
#creo allora una funzione update_item con all'interno passo due parametri (cosa sono item_id e item? oggetti?) che ci si aspetta essere di tipo intero e Item
def update_item(item_id: int, item: Item):
    """Questa è una "bandierina" (flag). Di base diciamo: "Non ho ancora aggiornato nulla". 
    Se durante il ciclo for troviamo l'ID giusto, la cambiamo in True. 
    Se alla fine del ciclo è ancora False, sappiamo che l'ID non esisteva e lanciamo l'errore 404."""
    #associo alla variabile rows la funzione read_csv()
    rows = read_csv()
    #cosa fa updated = false?
    updated = False

    #per ogni i ed r che dichiato qui all'interno della funzione enumerate(rows) creo una condizione if, giusto?
    """
    enumerate è utilissimo: ti restituisce sia l'indice i (la posizione nella lista: 0, 1, 2...) sia il contenuto r (il dizionario). 
    Ci serve i perché per modificare la lista dobbiamo scrivere rows[i] = ... (vai alla posizione X e cambia il contenuto).
    Sì! Per ogni singola riga del CSV (r), controlliamo se il suo ID è quello che l'utente vuole modificare. 
    Se sì, usiamo la sua posizione (i) per sostituire i dati vecchi con quelli nuovi.
    """
    for i, r in enumerate(rows):
        #se 'id del dizionario r convertito in intero è uguale all'oggetto item_id
        if int(r["id"]) == item_id:
            # Sostituiamo il vecchio dizionario con quello nuovo inviato dall'utente
            rows[i] = item.dict()
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=404, detail="Impossibile aggiornare: ID non trovato")

    write_csv(rows)
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """OPERAZIONE: DELETE - Rimuove un record dal CSV."""
    rows = read_csv()
    # Creiamo una nuova lista escludendo l'elemento con l'ID specificato
    new_rows = [r for r in rows if int(r["id"]) != item_id]

    # Se la lunghezza non è cambiata, l'ID non esisteva
    if len(rows) == len(new_rows):
        raise HTTPException(status_code=404, detail="Impossibile eliminare: ID non trovato")

    write_csv(new_rows)
    return {"message": "Elemento eliminato con successo"}