import json

# Cargar datos de productos
with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
    
with open('azure-clu/conversational-template.json', 'r', encoding='utf-8') as file:
    clu_template = json.load(file)

intents_data = []

def generate_intent_examples(product):
    for t in product["type"]:
        intent_name = "Recomendacion-" + t
        existing_intent = next((id for id in intents_data if id["intent"] == intent_name), None)

        if existing_intent:
            # Evitar agregar duplicados en los valores
            if product["title"] not in existing_intent["entities"][0]["values"]:
                existing_intent["entities"][0]["values"].append(product["title"])
                product_title_question = [
                    f"¿Qué opinas de la {product['title']}?",
                    f"¿Vale la pena comprar la {product['title']}?",
                    f"¿Es la {product['title']} buena para principiantes?",
                    f"¿Qué características tiene la {product['title']}?",
                    f"¿Dónde puedo conseguir la {product['title']}?",
                    f"¿La {product['title']} tiene buen precio?",
                    f"¿Qué tal su rendimiento la {product['title']}?",
                    f"¿La {product['title']} es recomendable para su uso?",
                    f"¿Es duradera la {product['title']}?",
                    f"¿La {product['title']} tiene buenas críticas?"
                ]
                for question in product_title_question:
                    existing_intent["examples"].append(question)
        else:
            # Crear nuevo intent
            intents_data.append({
                "intent": intent_name,
                "examples": [
                    f"Recomiéndame una {t}",
                    f"¿Cuál es el mejor {t}?",
                    f"¿Qué {t} tiene un buen precio?",
                    f"¿Me puedes recomendar una {t} de buena calidad?",
                    f"¿Qué {t} tiene más funciones?",
                    f"¿Qué opinas de la {product['title']}?",
                    f"¿Vale la pena comprar la {product['title']}?",
                    f"¿Es la {product['title']} buena para principiantes?",
                    f"¿Qué características tiene la {product['title']}?",
                    f"¿Dónde puedo conseguir la {product['title']}?",
                    f"¿La {product['title']} tiene buen precio?",
                    f"¿Qué tal su rendimiento la {product['title']}?",
                    f"¿La {product['title']} es recomendable para su uso?",
                    f"¿Es duradera la {product['title']}?",
                    f"¿La {product['title']} tiene buenas críticas?"
                ],
                "entities": [
                    {
                        "type": t,
                        "values": [t, product["title"]]
                    }
                ]
            })

def create_conversational_file(intents_data):

    # Agregar intents
    for intent in intents_data:
        clu_template["assets"]["intents"].append({"category": intent["intent"]})

        # Agregar entidades correctamente
        for entity in intent["entities"]:
            entity_category = entity["type"]
            existing_entity = next((e for e in clu_template["assets"]["entities"] if e["category"] == entity_category), None)

            if not existing_entity:
                # Crear una nueva entidad si no existe
                new_entity = {
                    "category": entity_category,
                    "compositionSetting": "separateComponents",
                    "list": {"sublists": []}
                }
                clu_template["assets"]["entities"].append(new_entity)
                existing_entity = new_entity

            # Agregar cada modelo como un sublist separado
            for value in entity["values"]:
                existing_sublist = next((s for s in existing_entity["list"]["sublists"] if s["listKey"] == value), None)

                if not existing_sublist:
                    existing_entity["list"]["sublists"].append({
                        "listKey": value,
                        "synonyms": [
                            {
                                "language": "es",
                                "values": [value]
                            }
                        ]
                    })

        # Agregar ejemplos de entrenamiento (utterances)
        for example in intent["examples"]:
            # Determinar la posición de la entidad en el texto
            entity_positions = []
            for entity in intent["entities"]:
                for value in entity["values"]:
                    start_index = example.lower().find(value.lower())
                    if start_index != -1:
                        entity_positions.append({
                            "category": entity["type"],
                            "offset": start_index,
                            "length": len(value)
                        })

            clu_template["assets"]["utterances"].append({
                "text": example,
                "intent": intent["intent"],
                "language": "es",
                "dataset": "train",
                "entities": entity_positions
            })

    return clu_template

# Generar intents
for product in products:
    generate_intent_examples(product)

# Guardar archivo JSON de intents
with open('azure-clu/structured-entities.json', 'w', encoding='utf-8') as f:
    json.dump(intents_data, f, ensure_ascii=False, indent=4)
    
# Crear JSON de CLU solo una vez después del bucle
clu_project = create_conversational_file(intents_data)

# Guardar archivo CLU
with open('azure-clu/clu_project.json', 'w', encoding='utf-8') as f:
    json.dump(clu_project, f, ensure_ascii=False, indent=4)

print("Archivos generados correctamente.")
