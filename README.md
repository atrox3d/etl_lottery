## README

### Italiano
---


Questo progetto contiene codice per l'analisi dei dati della Lotteria Italia.

una versione online che utilizza sqlite come db è raggiungibile a:
https://atrox3dlottery.streamlit.app/


**Struttura del progetto:**

*   `index.py`: Script principale per l'esecuzione dell'applicazione Streamlit.

        streamlit run index.py

    *   `dashboard/`: Contiene moduli per la creazione della dashboard, inclusi helper e gestione dei dati con pandas.
    *   `pagination/`: Gestisce la paginazione dei dati.

*   `main.py`: carica e trasforma i dati da tabella html alla tabella 'lotteria' nel database 'testing'

        python main.py
        
    *   `etl/`: Contiene script per l'estrazione, trasformazione e caricamento dei dati (ETL).


*   `dbhelpers/`: Contiene moduli per la gestione del database, inclusa la configurazione e la creazione di query.
*   `tests/`: Contiene test unitari per i moduli `dbhelpers`.
*   `docker-compose.yml`: crea due servizi:
    *   mysql
    *   phpmydamin

---

**Come eseguire il progetto:**

1.  Assicurati di avere Docker e Docker Compose installati.
2.  Clona il repository.
3.  Creare ed attivare virtual environment:

        python -m venv .venv
        source .venv/bin/activate

4.  Installare le dipendenze:

        pip install -r requirements.txt
5.  Esegui `docker compose up` nella directory principale del progetto.
6.  Esegui `python main.py`per creare la tabella 'lotteria' nel database 'testing'.
7.  Esegui `streamlit run index.py` per avviare l'applicazione Streamlit.
8.  L'applicazione sarà disponibile all'indirizzo `http://localhost:8501`.

---

**Test:**

Per eseguire i test unitari, usa il comando `pytest` nella directory principale del progetto.


---

### English
---

This project contains code for analyzing data from the Italian Lottery (Lotteria Italia).

an online version which uses sqlite as db is reachable at:
https://atrox3dlottery.streamlit.app/

**Project Structure:**

*   `index.py`: Main script to run the Streamlit application.

        streamlit run index.py

    *   `dashboard/`: Contains modules for creating the dashboard, including helpers and data management with pandas.
    *   `pagination/`: Handles data pagination.

*   `main.py`: loads and and transforms data from html table to table 'lotteria' into 'testing' db

        python main.py
        
    *   `etl/`: Contains scripts for Extract, Transform, Load (ETL) operations.


*   `dbhelpers/`: Contains modules for database management, including configuration and query building.
*   `tests/`: Contains unit tests for the `dbhelpers` modules.
*   `docker-compose.yml`: Configuration file for Docker Compose.


---

**How to run the project:**

1.  Make sure you have Docker and Docker Compose installed.
2.  Clone the repository.
3.  Creare ed attivare virtual environment:

        python -m venv .venv
        source .venv/bin/activate

4.  Installare le dipendenze:

        pip install -r requirements.txt

5.  Run `docker compose up --build` in the project's root directory.
6.  Run `python main.py` to create the table 'lotteria' into the 'testing' db.
7.  Run `streamlit run index.py` to start Streamlit application.
4.  The application will be available at `http://localhost:8501`.

---

**Tests:**

To run the unit tests, use the command `pytest` in the project's root directory.