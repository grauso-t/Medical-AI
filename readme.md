# Medical-AI

Un assistente virtuale che si interfaccia con un server FHIR per tradurre risposte in formato JSON in una rappresentazione testuale comprensibile.


## Architettura di Sistema

![System Architecture](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/architettura.jpg)

Dopo aver effettuato l’accesso al sistema ed inviato una richiesta all’assistente virtuale, questa verrà inoltrata al server.

Il modello GPT-3.5-Turbo elaborerà la richiesta trasformandola in un formato compatibile con un server FHIR. Una volta ricevuta la risposta in JSON, questa verrà elaborata localmente tramite il modello Mistral 7B oppure verrà generato un grafico tramite la libreria Chart.js.

Infine, la risposta verrà inviata al client per la visualizzazione da parte dell’utente.


## Demo

Dopo l’accesso, verrà mostrata la dashboard. Per accedere all’assistente virtuale, utilizzare il pulsante situato in basso.

![Dashboard](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/dashboard.png)

È possibile porre domande in linguaggio naturale, ad esempio: la lista dei pazienti, le informazioni personali di un paziente specifico, la lista degli appuntamenti, ecc.

![Virtual Assistant](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/virtual-assistant.png)

Qui sotto sono riportati alcuni esempi di risposte fornite dall’assistente virtuale.

![Example](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/example.png)

<p align="center">
  <img src="https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/graph.png" alt="Graph" width="500"/>
</p>


## Deployment

Per utilizzare l’applicazione, è sufficiente scaricare le dipendenze elencate nel file `requirements.txt`.

Successivamente, scaricare il modello preferito — idealmente un modello da 7B — in formato "gguf". Una volta scaricato, spostarlo nella cartella `models` e rinominarlo in `model.gguf`. Infine, avviare il server e aggiornare l’URL del server FHIR e la chiave OpenAI nelle impostazioni utente.

Username: `admin`  
Password: `qwerty`  


## Pubblicazioni Scientifiche

Questa repository è stata la base di due pubblicazioni scientifiche:

- **A Multi-Agent Architecture for Privacy-Preserving Natural Language Interaction with FHIR-Based Electronic Health Records**  
  DOI: [https://doi.org/10.23919/SoftCOM62040.2024.10721684](https://doi.org/10.23919/SoftCOM62040.2024.10721684)

- **Privacy-Preserving Healthcare Data Interactions: A Multi-Agent Approach Using LLMs**  
  DOI: [https://doi.org/10.24138/jcomss-2024-0119](https://doi.org/10.24138/jcomss-2024-0119)
