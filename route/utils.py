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
                observation = entry['resource']
                obs_id = observation['id']
                insertion_date = format_date(observation['meta']['lastUpdated'])
                
                if 'component' in observation:
                    observation_code = observation['component'][0]['code']['coding'][0]['system']
                    
                    observation_info = {
                        "Observation ID": obs_id,
                        "Insertion Date": insertion_date,
                        "Observation Code (LOINC)": observation_code
                    }
                    observations.append(observation_info)
                else:
                    observation_code = observation['code']['coding'][0]['code']
                
                    observation_info = {
                        "Observation ID": obs_id,
                        "Insertion Date": insertion_date,
                        "Observation Code (LOINC)": observation_code
                    }
                    observations.append(observation_info)
                
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
                patient = entry['resource']
                ptn_id = patient.get('id', 'Not defined')
                birthDate = patient.get('birthDate', 'Not defined')
                gender = patient.get('gender', 'Not defined')
                
                print(ptn_id)
                print(birthDate)
                
                patient_info = {
                    "Patient ID": ptn_id,
                    "Birth Date": birthDate,
                    "Gender": gender
                }
                patients.append(patient_info)
                
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