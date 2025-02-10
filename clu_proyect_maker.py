import json

# Cargar datos de productos
with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
    
with open('azure-clu/conversational-template.json', 'r', encoding='utf-8') as file:
    clu_template = json.load(file)

intents_data = [
    {
        "intent": "saber_precio",
        "examples": [
            
        ],
        "entities": [
            {
                "type": "producto",
                "values": {
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                }
            },
            {
                "type": "precio",
                "values": {
                    "precio": [
                        "precio", "costo", "valor", "tarifa", "valoración", "cuesta",
                        "coste", "importe", "cotización", "tasación", "valoracion",
                        "precio de venta", "precio de compra", "precio de mercado",
                        "precio de oferta", "precio de catálogo", "precio de referencia",
                        "precio de lista", "precio de liquidación", "precio de salida",
                        "precio de saldo", "precio de tarifa", "precio de venta al público"
                    ],
                    "rebaja": [
                        "rebaja", "descuento", "oferta", "promoción", "descuento especial",
                        "descuento por temporada", "descuento por oferta", "descuento por salida",
                        "descuento por saldo", "descuento por liquidación", "descuento por lista",
                        "descuento por promoción", "descuento por venta", "descuento por catálogo",
                        "descuento por referencia", "descuento por tarifa", "descuento por precio"
                    ],
                }
            }
        ]
    },
    {
        "intent": "saber_disponibilidad",
        "examples": [
            
        ],
        "entities": [
            {
                "type": "producto",
                "values": [
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                ]
            },
            {
                "type": "disponibilidad",
                "values": {
                    "disponibilidad": [
                        "disponibilidad", "existencia", "stock", "cantidad", "unidades",
                        "disponible", "en stock", "en existencia", "en inventario",
                        "en almacén", "en depósito", "en bodega", "en tienda",
                        "en local", "en punto de venta", "en comercio", "en establecimiento",
                        "en mercado", "en línea", "en internet", "en la web"        
                    ],
                }
            }
        ]
    },
    {
        "intent": "saber_redireccion",
        "examples": [
            
        ],
        "entities": [
            {
                "type": "producto",
                "values": [
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                ]
            },
            {
                "type": "enlace",
                "values": {
                    "enlace": [
                        "enlace", "link", "url", "dirección", "vínculo", "hipervínculo", "redirección",
                        "hipervinculo", "dirección web", "dirección url", "dirección de internet"
                    ],
                }
            }
        ]
    },
    {
        "intent": "saber_caracteristicas",
        "examples": [
            
        ],
        "entities": [
            {
                "type": "producto",
                "values": {
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                }
            },
            {
                "type": "caracteristicas",
                "values": {
                    "caracteristicas": [
                        "características", "especificaciones", "detalles", "atributos",
                        "propiedades", "funciones", "característica", "especificación",
                        "detalle", "atributo", "propiedad", "función", "caracteristica",
                        "especificacion", "atributos", "propiedades", "funciones", "madera",
                        "caoba", "arce", "Color Negro", "Acabado Natural", "Cuerpo de Acacia", 
                        "Acacia", "24 trastes", "golpeador", "aliso", "ocume", "Escala de 648", 
                        "2 pastillas", "Incluye estuche", "Cejilla de hueso", "Signature"
                    ],
                }
            }
        ]
    }
]

def generate_synonyms(product):
    product_type = product["type"][0]
    for i in intents_data:
        if product_type not in i["entities"][0]["values"]:
            i["entities"][0]["values"].append(product_type)
            i["entities"][0]["values"][product["title"]].append(product["type"])
            i["entities"][0]["values"][product["title"]].append(product["title"])
        else:
            i["entities"][0]["values"][product["title"]].append(product["title"])
        

def generate_intent_examples(product):
    for t in product["type"]:
        for i in intents_data:
            if i["intent"] == "saber_precio":
                input = [
                    {
                        "¿Cuánto cuesta el " + {product['title']}+ "?": {
                            "entities": [
                                {
                                    "category": "producto",
                                    "offset": 18,
                                    "length": {len(product['title'])}
                                },
                                {
                                    "category": "precio",
                                    "offset": 8,
                                    "length": 6
                                }
                            ]
                        }
                    }
                ]
                i["examples"].append(input[0])
            elif i["intent"] == "saber_disponibilidad":
                input = [
                    {
                        "¿Cuándo estaría disponible el " + product['title']+ "?": {
                            "entities": [
                                {
                                    "category": "producto",
                                    "offset": 31,
                                    "length": len(product['title'])
                                },
                                {
                                    "category": "disponibilidad",
                                    "offset": 18,
                                    "length": 10
                                }
                            ]
                        }
                    }
                ]
                i["examples"].append(input[0])
            elif i["intent"] == "saber_redireccion":
                input = [
                    {
                        "dame el enlace de " + product['title']: {
                            "entities": [
                                {
                                    "category": "producto",
                                    "offset": 18,
                                    "length": len(product['title'])
                                },
                                {
                                    "category": "enlace",
                                    "offset": 10,
                                    "length": 6
                                }
                            ]
                        }
                    }
                ]
                i["examples"].append(input[0])
            elif i["intent"] == "saber_caracteristicas":
                input = [
                    {
                        "dame las caracteristicas de " + product['title']: {
                            "entities": [
                                {
                                    "category": "producto",
                                    "offset": 31,
                                    "length": len(product['title'])
                                },
                                {
                                    "category": "precio",
                                    "offset": 10,
                                    "length": 14
                                }
                            ]
                        }
                    }
                ]
                i["examples"].append(input[0])
            else:
                print("Intent no encontrado.")
                break
        

#def create_conversational_file(intents_data):
#
#    # Agregar intents
#    for intent in intents_data:
#        clu_template["assets"]["intents"].append({"category": intent["intent"]})
#
#        # Agregar entidades correctamente
#        for entity in intent["entities"]:
#            entity_category = entity["type"]
#            existing_entity = next((e for e in clu_template["assets"]["entities"] if e["category"] == entity_category), None)
#
#            if not existing_entity:
#                # Crear una nueva entidad si no existe
#                new_entity = {
#                    "category": entity_category,
#                    "compositionSetting": "separateComponents",
#                    "list": {"sublists": []}
#                }
#                clu_template["assets"]["entities"].append(new_entity)
#                existing_entity = new_entity
#
#            # Agregar cada modelo como un sublist separado
#            for value in entity["values"]:
#                existing_sublist = next((s for s in existing_entity["list"]["sublists"] if s["listKey"] == value), None)
#
#                if not existing_sublist:
#                    existing_entity["list"]["sublists"].append({
#                        "listKey": value,
#                        "synonyms": [
#                            {
#                                "language": "es",
#                                "values": [value]
#                            }
#                        ]
#                    })
#
#        # Agregar ejemplos de entrenamiento (utterances)
#        for example in intent["examples"]:
#            # Determinar la posición de la entidad en el texto
#            entity_positions = []
#            for entity in intent["entities"]:
#                for value in entity["values"]:
#                    start_index = example.lower().find(value.lower())
#                    if start_index != -1:
#                        entity_positions.append({
#                            "category": entity["type"],
#                            "offset": start_index,
#                            "length": len(value)
#                        })
#
#            clu_template["assets"]["utterances"].append({
#                "text": example,
#                "intent": intent["intent"],
#                "language": "es",
#                "dataset": "train",
#                "entities": entity_positions
#            })
#
#    return clu_template

# Generar intents
for product in products:
    generate_synonyms(product)

# Guardar archivo JSON de intents
with open('azure-clu/structured-entities.json', 'w', encoding='utf-8') as f:
    json.dump(intents_data, f, ensure_ascii=False, indent=4)
    
# Crear JSON de CLU solo una vez después del bucle
# clu_project = create_conversational_file(intents_data)

# Guardar archivo CLU
# with open('azure-clu/clu_project.json', 'w', encoding='utf-8') as f:
#     json.dump(clu_project, f, ensure_ascii=False, indent=4)

print("Archivos generados correctamente.")
