import requests
from datetime import datetime

def create_observation(session):
    fhir_url_observation = session['fhir_url'] + "Observation?_count=5"

    try:
        response = requests.get(fhir_url_observation)
        if response.status_code == 200:
            json_data = response.json()
            observations = []

            for entry in json_data['entry']:
                observation = entry.get('resource', {})
                obs_id = observation.get('id', 'Not defined')
                last_updated = format_date(observation.get('meta', {}).get('lastUpdated', 'Not defined'))
                reference = observation.get('subject', {}).get('reference', 'Not defined')

                observation_info = {}

                if 'component' in observation:
                    observation_code = observation['component'][0]['code'].get('text', 'Not defined')

                    observation_info = {
                        "Observation ID": obs_id,
                        "Last Updated": last_updated,
                        "Reference": reference,
                        "Observation Code (LOINC)": observation_code
                    }
                else:
                    observation_code = observation.get('code', {}).get('text', 'Not defined')

                    observation_info = {
                        "Observation ID": obs_id,
                        "Last Updated": last_updated,
                        "Reference": reference,
                        "Observation": observation_code
                    }

                observations.append(observation_info)
                print(observation_info)

            return observations
    except requests.exceptions.RequestException as e:
        print("Si è verificato un errore durante la richiesta GET:", e)
        
    return False

def create_patient(session):
    fhir_url_patient = session['fhir_url'] + "Patient?_count=5"

    try:
        response = requests.get(fhir_url_patient)
        if response.status_code == 200:
            json_data = response.json()
            patients = []

            for entry in json_data['entry']:
                patient = entry.get('resource', {})
                ptn_id = patient.get('id', 'Not defined')
                birthDate = patient.get('birthDate', 'Not defined')
                gender = patient.get('gender', 'Not defined')

                name_info = patient.get("name", [{}])[0]
                name = " ".join(name_info.get("given", []))
                surname = name_info.get("family", "")

                if name.strip() == "" and surname.strip() == "":
                    full_name = "Not found"
                else:
                    full_name = name + " " + surname

                patient_info = {
                    "Patient ID": ptn_id,
                    "Name": full_name,
                    "Birth Date": birthDate,
                    "Gender": gender
                }
                patients.append(patient_info)

                print(patient_info)

            return patients
    except requests.exceptions.RequestException as e:
        print("Si è verificato un errore durante la richiesta GET:", e)
        
    return False

def format_date(input_string):
    try:
        datetime_obj = datetime.strptime(input_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        # Se la stringa non è nel formato originale, prova il formato alternativo
        datetime_obj = datetime.strptime(input_string, "%Y-%m-%dT%H:%M:%S%z")
        
    formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M")
    return formatted_date