import json
import os

def load_keywords(keywords_file):
    # Carga las claves válidas desde keywords.json.
    with open(keywords_file, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
    return keywords

def load_dataset(dataset_file):
    # Carga el dataset desde un archivo JSON. 
    with open(dataset_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, directory, filename):
    # Guarda un JSON en el directorio especificado. 
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def process_dataset(dataset_file, keywords_file, output_directory):
    # Procesa el dataset y guarda cada producto como un JSON individual. 
    keywords = load_keywords(keywords_file)
    dataset = load_dataset(dataset_file)
    
    print(keywords)
    pause = input("Presiona Enter para continuar: ")
    
    for i, product in enumerate(dataset):
        
        filtered_data = {}
        
        # Filtra solo la clave 'features' si está presente en el producto
        if 'features' in product:

            filtered_data['name'] = product['title']
            filtered_data['precio'] = product['current_price']
            filtered_data['url'] = product['url']
            filtered_data['type'] = product['type'][0]
            
            for p in keywords:
                if product['type'][0] == p:
                    print(f"Coincidencia de tipo encontrada: {product['type'][0]}")
                    for feature in product['features']:
                        for keyword in keywords[p]:
                            print(keyword)
                            #pause = input("Presiona Enter para continuar: ")
                            if keyword in feature:
                                filtered_data[keyword] = feature
                                print(f"Coincidencia encontrada: {feature}")
                                break
                else:
                    filtered_data = []
                                
            if filtered_data:
                filename = f"product_{i+1}.json"
                save_json(filtered_data, output_directory, filename)
                print(f"Guardado: {filename}")
            else:
                print(f"No se encontraron coincidencias en 'features' para el producto {i+1}")
        
        inp = input("Presiona Enter para continuar, 'exit' para salir: ")
        if inp == 'exit':
            break

# Ejemplo de uso
process_dataset("hifi-data/data.json", "Azure/azure-cner/src/keywords.json", "Azure/azure-cner/src/key-values")
