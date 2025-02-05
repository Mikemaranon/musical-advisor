import json
import random

with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
    
# Variables para almacenar los datos generados
type_list = []

intents_data = []

synonyms_data = []
s_synonyms = []


# Función para generar ejemplos de entrenamiento
def generate_intent_examples(product):
    for t in product["type"]:
        if "Recomendacion-" + t not in intents_data:
            intents_data.append({
                "intent": "Recomendacion-" + t,
                "examples": [
                    f"Recomiéndame una {t}",
                    f"¿Cuál es el mejor {t}?",
                    f"¿Qué {t} tiene un buen precio?",
                    f"¿Me puedes recomendar una {t} de buena calidad?",
                    f"¿Qué {t} tiene más funciones?"
                ],  
                "entities": [
                    {
                        "type": t,
                        "values": [t, product["title"]]
                    }
                ]
            })
        else:
            for id in intents_data:
                if id["intent"] == "Recomendacion-" + t:
                    id["entities"].get(0)["values"].append({
                        product["title"]
                    })
                    break

# Función para generar sinónimos
def generate_synonyms(product):
    product_type = product.get("type", [""])[0]
    features = product.get("features", [])
    
    return {
        "synonym_groups": [
            {"synonyms": [product_type, "instrumento musical"]},
            {"synonyms": [f"{feature.split(':')[0]}", f"{feature.split(':')[0]} feature"]} for feature in features
        ]
    }

def getAllTypes(products):
    for t in product["type"]:
        if(t not in type_list):
            type_list.append(t)

getAllTypes(products)

# Generar los ejemplos de entrenamiento, sinónimos y respuestas para cada producto
for product in products:

    # generar intents
    generate_intent_examples(product)
    
    # Agregar sinónimos
    synonyms_data.append(generate_synonyms(product))

# Guardar los ficheros generados

# Fichero de entrenamiento (JSON)
with open('training_data.json', 'w', encoding='utf-8') as f:
    json.dump(intents_data, f, ensure_ascii=False, indent=4)

# Fichero de sinónimos (JSON)
with open('synonyms_data.json', 'w', encoding='utf-8') as f:
    json.dump(synonyms_data, f, ensure_ascii=False, indent=4)

print("Archivos generados correctamente.")

