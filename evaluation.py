from typing import Optional, List, Dict
from pydantic import BaseModel, Field

def calculate_equality(generated, reference):
    if type(generated) != type(reference):
        raise ValueError("Instances must be of the same type")

    dict1 = generated.dict()
    dict2 = reference.dict()

    total_attributes = len(dict2)
    if total_attributes == 0:
        return 100.0

    matching_attributes = 0
    for key in dict1.keys():
        if key in dict2 and dict1[key] == dict2[key]:
            matching_attributes += 1
   
    percentage = (matching_attributes / total_attributes) * 100.0
    return percentage

class Patient(BaseModel):
    resourceType: str = Field("Patient", description="Tipo di risorsa, fisso a 'Patient' per paziente FHIR")
    id: Optional[str] = Field(None, description="Identificatore univoco del paziente")
    active: Optional[bool] = Field(None, description="Stato attivo del paziente (True o False)")
    name: Optional[List[str]] = Field(None, description="Lista dei nomi del paziente")
    gender: Optional[str] = Field(None, description="Sesso del paziente (male, female, other, unknown)")
    birthDate: Optional[str] = Field(None, description="Data di nascita del paziente nel formato 'YYYY-MM-DD'")
    deceasedBoolean: Optional[bool] = Field(None, description="Indica se il paziente è deceduto (True o False)")
    deceasedDateTime: Optional[str] = Field(None, description="Data/ora del decesso del paziente nel formato ISO 8601")
    address: Optional[List[str]] = Field(None, description="Array degli indirizzi del paziente")
    telecom: Optional[List[str]] = Field(None, description="Array dei contatti del paziente (telefono, email, ecc.)")
    maritalStatus: Optional[str] = Field(None, description="Stato civile del paziente (single, married, divorced, widowed, etc.)")

class AllergyIntolerance(BaseModel):
    resourceType: str = Field("AllergyIntolerance", description="Tipo di risorsa, fisso a 'AllergyIntolerance' per allergie/intolleranze")
    id: Optional[str] = Field(None, description="Identificatore univoco della risorsa allergia/intolleranza")
    patient: Optional[str] = Field(None, description="Riferimento al paziente associato")
    substance: Optional[str] = Field(None, description="Sostanza a cui il paziente è allergico o intollerante")
    status: Optional[str] = Field(None, description="Stato della condizione (active, inactive, resolved)")
    recordedDate: Optional[str] = Field(None, description="Data di registrazione della condizione nel formato ISO 8601")
    note: Optional[str] = Field(None, description="Note aggiuntive sulla condizione")

class Appointment(BaseModel):
    resourceType: str = Field("Appointment", description="Tipo di risorsa, fisso a 'Appointment' per gli appuntamenti")
    id: Optional[str] = Field(None, description="Identificatore univoco dell'appuntamento")
    status: Optional[str] = Field(None, description="Stato dell'appuntamento (pending, booked, arrived, fulfilled, cancelled)")
    description: Optional[str] = Field(None, description="Descrizione dell'appuntamento")
    start: Optional[str] = Field(None, description="Data e ora di inizio dell'appuntamento nel formato ISO 8601")
    end: Optional[str] = Field(None, description="Data e ora di fine dell'appuntamento nel formato ISO 8601")
    participant: Optional[List[str]] = Field(None, description="Elenco dei partecipanti all'appuntamento (es. medico, paziente)")
    location: Optional[str] = Field(None, description="Luogo dell'appuntamento")

class Observation(BaseModel):
    resourceType: str = Field("Observation", description="Tipo di risorsa, fisso a 'Observation' per le osservazioni")
    id: Optional[str] = Field(None, description="Identificatore univoco dell'osservazione")
    subject: Optional[str] = Field(None, description="Riferimento al soggetto dell'osservazione (es. ID del paziente)")
    status: Optional[str] = Field(None, description="Stato dell'osservazione (final, amended, corrected, etc.)")
    code: Optional[str] = Field(None, description="Codice dell'osservazione (es. tipo di misurazione)")
    valueQuantity: Optional[str] = Field(None, description="Valore quantitativo dell'osservazione")
    valueString: Optional[str] = Field(None, description="Valore testuale dell'osservazione")
    effectiveDateTime: Optional[str] = Field(None, description="Data/ora effettiva dell'osservazione nel formato ISO 8601")
    performer: Optional[str] = Field(None, description="Entità che ha eseguito l'osservazione (es. nome del medico)")

generated = Patient(
    id="12345",
    name=["John", "Doe"],
    gender="male",
    birthDate="1980-05-15",
    address=["123 Main St", "Atlanta", "USA"],
    telecom=["123-456-7890", "john.doe@example.com"],
    maritalStatus="married"
)

reference = Patient(
    id="12345",
    active=True,
    name=["John", "Doe"],
    gender="male",
    birthDate="1980-05-15",
    deceasedBoolean=False,
    address=["123 Main St", "Atlanta", "USA"],
    telecom=["123-456-7890", "john.doe@example.com"],
    maritalStatus="married"
)

# Calcolo della percentuale di uguaglianza
equality_percentage = calculate_equality(generated, reference)
print(f"Percentage of equality: {equality_percentage:.2f}%")
