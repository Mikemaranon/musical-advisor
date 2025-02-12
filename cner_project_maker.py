import json
import os

# extract azure-cner/src/keywords.json
with open("Azure/azure-cner/src/keywords.json", "r", encoding="utf-8") as keywords_file:
    keywords = json.load(keywords_file)

dataset = {
    "assets": {
        "projectKind": "CustomEntityRecognition", 
        "entities": [],
        "documents": []
    }
}
    
def extract_entities_from_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    entities = []
    for keyword in keywords:
        if keyword in text:
            entities.append({"category": keyword, "offset": text.index(keyword), "length": len(keyword)})

    return json.dumps(entities)

def generate_json_from_files(directory):

    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            extracted_entities = extract_entities_from_text(file_path)
            
            document_entry = {
                "location": file_name,
                "language": "es",
                "entities": json.loads(extracted_entities),
                "dataset": "Train"
            }
            dataset["assets"]["documents"].append(document_entry)
    
    return dataset

# Generate the dataset
dataset = generate_json_from_files("azure-cner/src/txt_outputs")

# Save the dataset to a new JSON file
with open("Azure/azure-cner/cner_project.json", "w", encoding="utf-8") as output_file:
    json.dump(dataset, output_file, indent=4, ensure_ascii=False)