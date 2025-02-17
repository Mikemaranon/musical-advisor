import json
import os

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

    i = 0
    
    for document in document_list:
        entities = {
            "regionOffset": 0,
            "regionLength": len(document_list[document]),
            "labels": [
                # here we will add the labeled entities for each document
            ]
        }
        for entity in key_values[i]:
            if entity in document_list[document]:
                entities["labels"].append({"category": entity, "offset": document_list[document].index(entity), "length": len(entity)})
                # error
        document_entry = {
            "location": document,
            "language": "es",
            "entities": entities,
            "dataset": "Train"
        }
        dataset["documents"].append(document_entry)
        i += 1

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