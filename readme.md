
# 👨🏻‍⚕️ Medical-AI

A virtual assistant that interfaces with a FHIR server to translate JSON-formatted responses into an understandable textual representation.


## System Architecture

![System Architecture](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/architettura.jpg)

After logging into the system and sending a request to the virtual assistant, the request will be forwarded to the server.

The GPT-3.5-Turbo model will process the request, transforming it into a format compatible with a FHIR server. Once the JSON response is received, it will be processed locally using the Mistral 7B model or a graph will be generated through the Chart.js library.

Finally, the response will be sent to the client for user visualization.


## 📽️ Demo

After logging in, the dashboard will be displayed. To access the virtual assistant, use the button located at the bottom.

![Dashboard](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/dashboard.png)

You can ask the virtual assistant questions in natural language, such as: the list of patients, personal information about a specific patient, the list of appointments, etc.

![Virtual Assistant](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/virtual-assistant.png)

Below are some example responses from the virtual assistant.

![Example](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/example.png)

![Graph](https://raw.githubusercontent.com/grauso-t/medical-ai/main/Screenshot/graph.png)
## ⚙️ Deployment

To use the application, simply download the dependencies listed in the 'requirements.txt' file.

Then, download your preferred model — ideally a 7B model — in "gguf" format. Once downloaded, move it to the 'models' folder and rename it to 'model.gguf'. Finally, start the server and update the FHIR server URL and the OpenAI key in the user settings.

Username: admin
Password: qwerty
