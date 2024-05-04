# Documentazione Tecnica del Sito di Esposizione d'Arte

## Introduzione
Il sito web si propone come una piattaforma espositiva per opere d'arte, consentendo la visualizzazione di opere sia di artisti storici che contemporanei, inclusi gli utenti registrati che desiderano esporre le loro creazioni. Le funzionalità principali includono la visualizzazione delle opere e la possibilità per gli utenti di caricare e gestire le proprie opere d'arte.

## Tecnologie Utilizzate
- **Python**: Linguaggio di programmazione principale usato per lo sviluppo del backend.
- **Flask Web Framework**: Framework web leggero utilizzato per gestire le richieste HTTP, il routing e la presentazione delle pagine web.
- **SQLAlchemy**: ORM (Object-Relational Mapping) che facilita l'interazione tra il codice Python e il database MySQL, permettendo una gestione più efficiente e sicura dei dati.
- **MySQL**: Sistema di gestione del database relazionale utilizzato per memorizzare tutte le informazioni relative agli utenti, agli artisti e alle opere d'arte.
- **TailwindCSS**: Framework CSS utilizzato per lo styling del sito, permettendo una design responsive e personalizzabile.

## Architettura del Sistema
L'architettura del sistema è progettata per separare chiaramente le responsabilità e organizzare il codice in modo modulare e manutenibile. Di seguito vengono descritti i componenti principali dell'architettura:

### Struttura dei File
Il sistema è organizzato nei seguenti file Python principali:
- `__init__.py`: Configura e inizializza l'applicazione Flask, comprese le impostazioni di base e l'integrazione con altri moduli.
- `run.py`: File eseguibile che avvia l'applicazione Flask, gestendo il server di sviluppo e le configurazioni di produzione.
- `models.py`: Contiene le definizioni dei modelli SQLAlchemy per il database, rappresentando le strutture di dati come `artists`, `users`, `artworks`, e così via.
- `routes.py`: Gestisce il routing delle richieste, definendo le funzioni che rispondono alle diverse richieste HTTP inviate al server.

### Templates
Tutti i template web sono organizzati nella cartella `templates`. Un template di base, `base.html`, è utilizzato per mantenere un layout coerente in tutto il sito, inclusi l'header e il footer comuni a tutte le pagine. Gli altri template derivano da questo file di base, garantendo un'interfaccia utente uniforme e riducendo la duplicazione del codice HTML.

### Risorse Statiche
Le immagini delle opere d'arte e altri file statici sono conservati nella cartella `static`. Questa organizzazione facilita la gestione e l'ottimizzazione delle risorse multimediali che il sito web deve caricare e visualizzare, migliorando l'esperienza utente generale.

### Moduli Utente
Il sistema è suddiviso in moduli per facilitare la gestione e l'espansione delle funzionalità:
- **Modulo Utente**: Gestisce autenticazione, registrazione, e profili degli utenti.
- **Modulo Artista**: Responsabile della gestione delle informazioni degli artisti e delle loro opere.
- **Modulo Opere d'Arte**: Permette agli utenti di esplorare, cercare e visualizzare opere d'arte.
- **Interfaccia Utente**: Realizzata con Flask e TailwindCSS, offre un'interfaccia pulita e facile da usare.

Questi componenti lavorano insieme per fornire una piattaforma robusta e flessibile per la visualizzazione e la gestione delle opere d'arte online.

## Struttura del Database
```sql
CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_year INTEGER NOT NULL,
    death_year INTEGER NOT NULL,
    genre VARCHAR(255),
    nationality VARCHAR(255) NOT NULL,
    bio TEXT,
    wikipedia_link VARCHAR(255) NOT NULL,
    number_paintings INTEGER DEFAULT 0
);

CREATE TABLE users (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    bio TEXT DEFAULT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE artworks (
    painting_name VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    PRIMARY KEY (artist_id, painting_name),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE users_as_artist (
    id_user INTEGER PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    nationality VARCHAR(255) NOT NULL,
    bio TEXT DEFAULT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE artworks_user (
    painting_name VARCHAR(255) NOT NULL,
    artist_user_id INTEGER NOT NULL,
    PRIMARY KEY (artist_user_id, painting_name),
    FOREIGN KEY (artist_user_id) REFERENCES users_as_artist(id_user)
);
```

## Sviluppo del Software
### Tutto lo sviluppo del progetto è stato eseguito utilizzando git ed effettuando commit ad ogni sessione di scrittura effettuata.
All'inizio dello sviluppo ho definito degli issues che andavano a descrivere i requisiti dell'applicazione finale e annotare dei promemoria per le idee e le problematiche in cui incorrevo o prevedevo di incorrere. Ora ho tradotto i requisiti dell'applicazione in user stories (in modo da renderli chiari).

### User Stories

#### 1. Creazione dell'account
- **Who**: Utente visitatore
- **What**: Creare un account sul sito
- **How**: Compilando un modulo di registrazione con username, password ed email.

#### 2. Visualizzazione delle opere storiche
- **Who**: Utente registrato
- **What**: Visualizzare opere storiche nell'homepage
- **How**: Accedendo alla homepage dove sono esposte le opere storiche in modo prominente.

#### 3. Visualizzazione dei dettagli degli artisti storici
- **Who**: Utente registrato
- **What**: Visualizzare dettagli specifici sugli artisti storici
- **How**: Cliccando sul nome dell'artista storico dall'homepage o da altre sezioni correlate per aprire una pagina dettagliata.

#### 4. Esplorazione delle opere degli altri utenti
- **Who**: Utente registrato
- **What**: Visualizzare opere caricate da altri utenti
- **How**: Navigando nella 'User Artwork Page' che elenca tutte le opere caricate dagli utenti.

#### 5. Visualizzazione dei dettagli degli user-artist
- **Who**: Utente registrato
- **What**: Ottenere informazioni dettagliate sugli user-artist
- **How**: Cliccando sul nome dell'utente-artist nella 'User Artwork Page' per visualizzare la loro bio, opere, e altre informazioni rilevanti.

#### 6. Trasformazione del proprio account in "User Artist"
- **Who**: Utente registrato
- **What**: Diventare un user-artist per poter caricare proprie opere
- **How**: Compilando un ulteriore modulo nel proprio profilo per aggiungere dettagli come nome d'arte, bio, genere e nazionalità.

#### 7. Aggiunta di opere da parte dell'user artist
- **Who**: User artist
- **What**: Aggiungere nuovi quadri al proprio portfolio sul sito
- **How**: Utilizzando un form specifico nella propria area utente per caricare immagini delle opere, insieme a titolo, descrizione, e altre informazioni pertinenti.

Deploy
Il deploy è stato realizzato su PythonAnywhere, una piattaforma cloud che supporta applicazioni Python/Flask, offrendo un ambiente di hosting facile da configurare e gestire.

Conclusioni
Il sito è progettato per essere estensibile e adattabile, con la possibilità di aggiungere nuove funzionalità come i like alle opere, integrazioni social per condividere opere su piattaforme esterne, e miglioramenti dell'interfaccia utente per dispositivi mobili (e in generale per renderla più aderente alle foto delle opere d'arte).
