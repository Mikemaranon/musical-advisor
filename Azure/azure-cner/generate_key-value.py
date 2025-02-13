import requests
import json
import os
from dotenv import load_dotenv
import time
import re

# Cargar variables de entorno desde el archivo .env
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT")

# API_KEY = os.getenv("GPT-35_API_KEY")
# ENDPOINT = os.getenv("GPT-35_ENDPOINT")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "model": "deepseek-r1",
    "messages": [{"role": "user", "content": "Hola, prueba de conexión"}]
}

try:
    response = requests.post(f"{ENDPOINT}/v1/chat/completions", json=payload, headers=HEADERS, timeout=10)
    print("Código de respuesta:", response.status_code)
    print("Respuesta:", response.text)
except requests.exceptions.Timeout:
    print("Warning: La solicitud tarda demasiado en responder.")
except requests.exceptions.RequestException as e:
    print("Error en la solicitud:", e)

times = {}

system_message = {
    "role": "system",
    "content": (
        "Eres un asistente experto en generación de documentos comerciales a partir de datos desestructurados. "
        "Debes generar un único párrafo que describa todas las claves del JSON de entrada, "
        "incluyendo sus valores sin editar. Debe de haber un hilo narrativo a lo largo del texto, \n"
        "no puede ser meramente descriptivo."
        "El contenido debe ser atractivo para el usuario final, con una intención comercial clara."
    )
}

def save_times(times, filename="Azure/azure-cner/src/times.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(times, f, indent=4, ensure_ascii=False)

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

# Generar texto con DeepSeek R1
def generar_texto(prompt, index):
    payload = {
        "model": "deepseek-r1",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    start_time = time.time()  # Inicia el temporizador
    response = requests.post(f"{ENDPOINT}/v1/chat/completions", json=payload, headers=HEADERS)
    end_time = time.time()  # Detiene el temporizador
    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido
    
    times[f"product_{index}"] = elapsed_time  # Almacena el tiempo en el diccionario
    
    print(f"Tiempo de respuesta de DeepSeek: {elapsed_time:.2f} segundos")
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error en la solicitud: {response.text}")

# Crear documentos de texto a partir del JSON
def generar_documento(json_data, ruta_salida, index):
    prompt = f"Genera un documento basado en esta información:\n{json.dumps(json_data, indent=2)}"
    texto_generado = generar_texto(prompt, index)
    
    # borrar la etiqueta <think> y </think> del texto generado junto con su contenido
    texto_generado = re.sub(r'<think>.*?</think>', '', texto_generado, flags=re.DOTALL)
    # borrar los signos de markdown
    texto_generado = texto_generado.replace("```markdown", "").replace("```", "")
    
    # Cambiar el nombre del archivo a "texto_" + index
    file_name = f"texto_{index}.txt"
    file_path = os.path.join(ruta_salida, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(texto_generado)

    print(f"Documento generado: {file_path}")

def process_dataset(dataset_file, keywords_file, output_directory):
    # Procesa el dataset y guarda cada producto como un JSON individual. 
    keywords = load_keywords(keywords_file)
    dataset = load_dataset(dataset_file)
    
    for i, product in enumerate(dataset):
        
        filtered_data = {}
        
        # Filtra solo la clave 'features' si está presente en el producto
        if 'features' in product:
            
            generar_documento(product, "Azure/azure-cner/src/texts", i + 1)

            filtered_data['name'] = product['title']
            filtered_data['precio'] = product['current_price']
            filtered_data['url'] = product['url']
            filtered_data['type'] = product['type'][0]
            
            for p in keywords:
                if product['type'][0] == p:
                    for feature in product['features']:
                        for keyword in keywords[p]:
                            if keyword in feature:
                                filtered_data[keyword] = feature
                                break
                                
            if filtered_data:
                filename = f"product_{i+1}.json"
                save_json(filtered_data, output_directory, filename)
                print(f"Guardado: {filename}")
            else:
                print(f"No se encontraron coincidencias en 'features' para el producto {i+1}")
        
        # Añadir una espera de 10 segundos entre cada solicitud
        time.sleep(60)
        
save_times(times)

# Ejemplo de uso
process_dataset("hifi-data/data.json", "Azure/azure-cner/src/keywords.json", "Azure/azure-cner/src/key-values")
