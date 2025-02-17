import json
import os
import re

key_values = []
entity_list = []
document_list = {}

with open("Azure/azure-cner/cner-template.json", "r", encoding="utf-8") as file:
    project = json.load(file)

dataset = {
        "projectKind": "CustomEntityRecognition", 
        "entities": [],
        "documents": []
    }

def normalize_str(s):
    return re.sub(r'\W+', '', s).lower()

def load_key_values(file_path):
    for file_name in os.listdir(file_path):
        if file_name.endswith(".json"):
            with open(os.path.join(file_path, file_name), "r", encoding="utf-8") as file:
                key_values.append(json.load(file))

def load_documents(file_path):
    for file_name in os.listdir(file_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(file_path, file_name), "r", encoding="utf-8") as file:
                document_list[file_name] = file.read()
                
def add_entities_to_dataset():
    for product in key_values:
        for entity in product:
            if entity not in entity_list:
                entity_list.append(entity)
                dataset["entities"].append({"category": entity})
    
def extract_entities_from_text():
    for i, document in enumerate(document_list):
        entities = [{
            "regionOffset": 0,
            "regionLength": len(document_list[document]),
            "labels": []
        }]
        line_counter = 0
        
        for entity in key_values[i]:
            print(key_values[i][entity])
            if normalize_str(key_values[i][entity]) in normalize_str(document_list[document]):
                print(entity)
                try:
                    specific_index = document_list[document].find(key_values[i][entity])
                    if specific_index != -1:
                        # Extrae el contenido hasta el índice del string específico
                        content_until_specific_string = document_list[document][:specific_index]
                        # Cuenta los saltos de línea en el contenido extraído
                        line_counter = content_until_specific_string.count('\n')
                    
                    entities[0]["labels"].append({"category": entity, "offset": document_list[document].index(key_values[i][entity]) + line_counter, "length": len(key_values[i][entity])})
                    line_counter = 0  # Reinicia el contador después de un try exitoso
                    
                except: 
                    print("skipping this one... ", key_values[i][entity])
                line_counter += document_list[document].count('\n')
        document_entry = {
            "location": document,
            "language": "es",
            "entities": entities,
            "dataset": "Train"
        }
        dataset["documents"].append(document_entry)
    
# Load the key values and documents
load_key_values("Azure/azure-cner/src/key-values")
load_documents("Azure/azure-cner/src/texts")

# Add the entities to the dataset
add_entities_to_dataset()
extract_entities_from_text()

project["assets"] = dataset

# Save the dataset to a new JSON file
with open("Azure/azure-cner/cner_project.json", "w", encoding="utf-8") as output_file:
    json.dump(project, output_file, indent=4, ensure_ascii=False)