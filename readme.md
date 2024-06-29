
# 👨🏻‍⚕️ Medical-AI

Un assistente virtuale che si interfaccia con un server FHIR al fine di tradurre le risposte in formato JSON in una rappresentazione testuale comprensibile.


## Architettura del Sistema

![Architettura](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/architettura.jpg)

Dopo aver effettuato l'accesso al sistema e inviato una richiesta all'assistente virtuale, questa verrà inoltrata al server.

Il modello GPT-3.5-Turno elaborerà la richiesta, trasformandola in una richiesta compatibile con un server FHIR. Una volta ricevuta la risposta JSON, essa verrà elaborata localmente utilizzando il modello Mistral 7B oppure verrà generato un grafico tramite la libreria Chart.js.

Infine, la risposta sarà inviata al client per la visualizzazione da parte dell'utente.
## 📽️ Demo

Una volta effettuato l'accesso, verrà visualizzata la dashboard. Per accedere all'assistente virtuale, utilizzare il pulsante situato in basso.

![Dashboard](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/dashboard.png)

All'assistente virtuale è possibile formulare richieste in linguaggio naturale, come ad esempio: la lista dei pazienti, le informazioni personali di un determinato paziente, la lista degli appuntamenti, ecc.

![Virtual Assistant](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/virtual-assistant.png)

Di seguito sono presentate alcune possibili risposte da parte dell'assistente virtuale.

![Example](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/example.png)

![Graph](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/graph.png)
## ⚙️ Deployment

Per utilizzare l'applicazione, basta scaricare le dipendenze elencate nel file 'requirements.txt'.

Successivamente, procedi scaricando il modello preferito, ideale un modello da 7B, in formato "gguf". Una volta scaricato, spostalo nella cartella 'models' e rinominalo in 'model.gguf'. Infine, avvia il server e aggiorna l'URL del server FHIR e la chiave per OpenAI nella sezione utente.