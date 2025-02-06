import json

# Cargar datos de productos
with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
    
with open('training-data/conversational-template.json', 'r', encoding='utf-8') as file:
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
        else:
            # Crear nuevo intent
            intents_data.append({
                "intent": intent_name,
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
                    "list": {"sublists": []},
                    "prebuilts": [],
                    "regex": {"expressions": []},
                    "requiredComponents": []
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
                                "language": "español",
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
                "language": "español",
                "dataset": "default",
                "entities": entity_positions
            })

    return clu_template

# Generar intents
for product in products:
    generate_intent_examples(product)

# Crear JSON de CLU solo una vez después del bucle
clu_project = create_conversational_file(intents_data)

# Guardar archivos
with open('training-data/structured-entities.json', 'w', encoding='utf-8') as f:
    json.dump(intents_data, f, ensure_ascii=False, indent=4)

with open('training-data/clu_project.json', 'w', encoding='utf-8') as f:
    json.dump(clu_project, f, ensure_ascii=False, indent=4)

print("Archivos generados correctamente.")
