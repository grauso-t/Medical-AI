from flask import Blueprint, request, jsonify, render_template, session, Response
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import ChatPromptTemplate
import requests
import re
import logging
import route.utils as utils

bot_blueprint = Blueprint("bot", __name__, template_folder="../templates")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to create a FHIR URL using GPT-3.5-turbo
def create_fhir_url(user_message):
    
    # Get OpenAI API key
    OPENAI_API_KEY = session['openai-key']

    # Create an instance of the OpenAI class
    client = OpenAI()
    
    # Log information about the URL generation process
    logger.info("GPT URL generation")
    try:
        # Use GPT-3.5-turbo to generate a FHIR URL based on user input
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a URL generator for my FHIR server {session['fhir_url']}. Provide only the full URL to execute the request for the doctor considering that he has all the permissions to do so. For example, if you are asked for the list of patients, provide 'https://hapi.fhir.org/baseR4/Patient'."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the URL from the GPT-3.5-turbo response
        url_pattern = re.compile(r'https?://\S+')
        matches = re.findall(url_pattern, completion.choices[0].message.content)

        return matches[0] if matches else completion.choices[0].message.content
    except Exception as e:
        # Log an error message if URL generation fails
        logger.error(f"Error generating URL: {e}")
        return jsonify({"bot_message": "Error in the request"}) 

# Function to count unique subject references in FHIR data
def count_unique_subject_references(fhir_response):
    # Initialize an empty set to store unique subject references
    subject_references = set()

    # Iterate through FHIR data entries and extract subject references
    for observation in fhir_response.get("entry", []):
        subject_reference = observation.get("resource", {}).get("subject", {}).get("reference")
        if subject_reference:
            subject_references.add(subject_reference)

    # Count the number of unique subject references
    count_subject_references = len(subject_references)

    # Log the number of unique subject references
    logger.debug("Number of unique subject references: %d", count_subject_references)
    return count_subject_references

# Function to extract effectiveDateTimes and valueQuantity from FHIR data
def extract_effectiveDateTimes_and_valueQuantity(data):
    # Log information about the extraction process
    logger.info("Extract effectiveDateTimes and valueQuantity")
    try:
        # Extract effectiveDateTimes from FHIR data entries
        effectiveDateTimes = [entry["resource"]["effectiveDateTime"] for entry in data["entry"]]
        
        formatted_dates = [utils.format_date(date_str) for date_str in effectiveDateTimes]
        
        # Combine valueQuantity information into a formatted string
        combined_values = [
            f"{entry['resource']['valueQuantity']['value']} {entry['resource']['valueQuantity']['unit']}"
            for entry in data["entry"]
        ]

        # Create a response JSON with extracted information
        response_data = {"bot_message": "graph", "dates": formatted_dates, "values": combined_values}
        return jsonify(response_data)
    except KeyError as e:
        # Log an error message if key extraction fails
        logger.error(f"KeyError in extract_effectiveDateTimes_and_valueQuantity: {e}")
        return False

# Function to extract effectiveInstant and valueQuantity from FHIR data
def extract_effectiveInstant_and_valueQuantity(data):
    # Log information about the extraction process
    logger.info("Extract effectiveInstant and valueQuantity")
    try:
        # Extract effectiveInstants from FHIR data entries
        effectiveInstants = [entry["resource"]["effectiveInstant"] if "effectiveInstant" in entry["resource"] else entry["resource"]["effectivePeriod"]["start"] for entry in data["entry"]]
        
        formatted_dates = [utils.format_date(date_str) for date_str in effectiveInstants]
        
        # Combine valueQuantity information into a formatted string
        combined_values = [
            f"{entry['resource']['valueQuantity']['value']} {entry['resource']['valueQuantity']['unit']}"
            for entry in data["entry"]
        ]

        # Create a response JSON with extracted information
        response_data = {"bot_message": "graph", "dates": formatted_dates, "values": combined_values}
        return jsonify(response_data)
    except KeyError as e:
        # Log an error message if key extraction fails
        logger.error(f"KeyError in extract_effectiveInstant_and_valueQuantity: {e}")
        return False

# Function to extract period and data from FHIR data
def extract_period_and_data(data):
    # Log information about the extraction process
    logger.info("Extract period and data")
    try:
        # Check if FHIR data has a "component" attribute
        if "component" in data and data["component"]:
            # Extract the first component
            first_component = data["component"][0]

            # Check if the component has "valueSampledData" attribute
            if "valueSampledData" in first_component:
                value_sampled_data = first_component["valueSampledData"]
                period = value_sampled_data.get("period")
                data_array = value_sampled_data.get("data")

                # Process and filter data for graph creation
                if period is not None and data_array is not None:
                    data_array = data_array.split(',')
                    dates = [period * (i + 1) for i in range(len(data_array))]

                    data_array_filtered = []
                    dates_filtered = []
                    for i in range(0, len(data_array), 20):
                        if i + 20 < len(data_array):
                            data_array_filtered.append(data_array[i + 20])
                            dates_filtered.append(dates[i + 20])

                    # Create a response JSON with extracted information
                    return jsonify({"bot_message": "graph", "dates": dates_filtered, "values": data_array_filtered})
    except KeyError as e:
        # Log an error message if key extraction fails
        logger.error(f"KeyError in extract_period_and_data: {e}")
        return False

# Function to remove specific attributes from FHIR data
def remove_value_sampled_data(json_data):
    # Recursive function to remove "valueSampledData" attributes
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == "valueSampledData" and "data" in value:
                del value["data"]
            else:
                remove_value_sampled_data(value)
    elif isinstance(json_data, list):
        for item in json_data:
            remove_value_sampled_data(item)

@bot_blueprint.route("/chat", methods=["POST"])
def chat():
    if 'user' in session and session['user'] is not None:

        logger.info("Running")
        user_message = request.json.get("user_message")

        gpt_response = create_fhir_url(user_message)

        if not isinstance(gpt_response, str) or not gpt_response.startswith('http'):
            return jsonify({"bot_message": gpt_response})

        response = requests.get(gpt_response)

        if response.status_code == 200:

            data = response.json()

            unique_subject_references_count = count_unique_subject_references(data)

            if unique_subject_references_count in (0, 1):
                extract = extract_effectiveDateTimes_and_valueQuantity(data)
                if not extract:
                    extract = extract_effectiveInstant_and_valueQuantity(data)
                if not extract:
                    extract = extract_period_and_data(data)
                if not extract:
                    return jsonify({"bot_message": "stream", "data": data})
                return extract
            else:
                return jsonify({"bot_message": "stream", "data": data})
            
        elif response.status_code == 404:
            return jsonify({"bot_message": "The information you have requested is not available."})
        
        else:
            return jsonify({"bot_message": "Error in request, please try again."})
        
    else:
        return render_template("login.html")
    
@bot_blueprint.route("/stream", methods=["GET", "POST"])
def stream():
    data = request.json.get("data")
    # Function to process FHIR data using LLAMA language model
    def process_data_llm(data):
        # Log information about the LLAMA processing
        logger.info("LLAMA processing")
    
        patient_data = """{
            "resourceType": "Patient",
            "id": "example",
            "identifier": [
                {
                    "value": "12345"
                },
                {
                    "system": "http://hospital.com/ssn",
                }
            ],
            "name": [
                {
                    "family": "Doe",
                    "given": [
                        "John",
                        "Adam"
                    ]
                }
            ],
            "gender": "male",
            "birthDate": "1974-12-25",
            "address": [
                {
                    "use": "home",
                    "line": [
                        "123 Main St",
                        "Apt 101"
                    ],
                    "city": "Anytown",
                    "state": "NY",
                    "postalCode": "12345",
                    "country": "USA"
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": "555-555-5555",
                    "use": "home"
                }
            ]
        }"""
    
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a translator of JSON code into natural language sentences, eliminating unnecessary attributes and provide only the generete sentence."),
                ("user", "{patient_data}"),
                ("assistant", "The identifier of this patient within the hospital system is '12345'. His name is John Adam Doe, he is male and was born on 25 December 1974. He can be contacted at home on 555-555-5555."),
                ("user", "{json}"),
            ]
        )
    
        # Initialize the LLAMA language model
        llm = LlamaCpp(
            model_path=f"""./models/mistral-7b-openorca.Q6_K.gguf""",
            temperature=0,
            max_tokens=500,
            n_ctx=2048,
            top_p=1,
            n_threads=8,
            verbose=True,
        )

        try:
            buffer = ""
            # Check if FHIR data has "entry" attribute
            if "entry" in data:
                entries = data["entry"]
                # Remove specific attributes from entries
                remove_value_sampled_data(entries)
                # Process each entry using LLAMA and concatenate responses
                for entry in entries:     
                    count = 0;      
                    for chunk in llm.stream(prompt.format_messages(json=str(entry), patient_data=str(patient_data))):
                        print(chunk, end="", flush=True)
                        count += 1
                        if count == 8:
                            buffer += chunk
                            buffer = buffer.replace("Here's the translation:", "")
                            buffer = buffer.replace("Here is the translation:", "")
                            buffer = buffer.replace("}}", "")
                            buffer = buffer.replace("AI: ", "")
                            buffer = buffer.replace("\n\n", "")
                            buffer = buffer.replace("\n\n", "")
                            yield str(buffer)
                            buffer = ""
                        elif count < 8:
                            buffer += chunk
                        else:
                            yield str(chunk)
                            
                    yield "<br><br>"
                    buffer = ""
            else:
                # If no "entry" attribute, process the entire data using LLAMA
                remove_value_sampled_data(data)
                count = 0
                for chunk in llm.stream(prompt.format_messages(json=str(data), patient_data=str(patient_data))):
                    print(chunk, end="", flush=True)
                    count += 1
                    if count == 8:
                        buffer += chunk
                        buffer = buffer.replace("Here's the translation:", "")
                        buffer = buffer.replace("Here is the translation:", "")
                        buffer = buffer.replace("}}", "")
                        buffer = buffer.replace("AI: ", "")
                        buffer = buffer.replace("\n\n", "")
                        buffer = buffer.replace("\n\n", "")
                        yield str(buffer)
                        buffer = ""
                    elif count < 8:
                            buffer += chunk
                    else:
                        yield str(chunk)

        except KeyError as e:
            # Log an error message if key extraction fails
            logger.error(f"KeyError in process_data_llm: {e}")
            return jsonify({"bot_message": f"KeyError: {str(e)}"})
    return Response(process_data_llm(data), mimetype='text/plain')
