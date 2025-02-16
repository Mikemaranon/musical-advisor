import json
import os

key_values = []
document_list = []
dataset = {
    "assets": {
        "projectKind": "CustomEntityRecognition", 
        "entities": [],
        "documents": []
    }
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
                document_list.append(file.read())
                
def add_entities_to_dataset():
    for product in key_values:
        for entity in product:
            if entity not in dataset["assets"]["entities"]:
                dataset["assets"]["entities"].append(entity)
    
def extract_entities_from_text():

    for document, key_val in document_list, key_values:
        entities = {
            "regionOffset": 0,
            "regionLength": document.length,
            "labels": [
                # here we will add the labeled entities for each document
            ]
        }
        for entity in key_val:
            if entity in document:
                entities["labels"].append({"category": entity, "offset": document.index(entity), "length": len(entity)})
        
        document_entry = {
            "location": document_list.index(document),
            "language": "es",
            "entities": entities,
            "dataset": "Train"
        }
        dataset["assets"]["documents"].append(document_entry)

# Load the key values and documents
load_key_values("Azure/azure-cner/src/key-values")
load_documents("Azure/azure-cner/src/texts")

# Add the entities to the dataset
add_entities_to_dataset()
extract_entities_from_text()

# Save the dataset to a new JSON file
with open("Azure/azure-cner/cner_project.json", "w", encoding="utf-8") as output_file:
    json.dump(dataset, output_file, indent=4, ensure_ascii=False)