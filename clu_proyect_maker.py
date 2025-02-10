import json

# Cargar datos de productos
with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
    
with open('azure-clu/conversational-template.json', 'r', encoding='utf-8') as file:
    clu_template = json.load(file)

with open("azure-clu/keywords.txt") as f:
    keywords = [line.strip().lower() for line in f]

executed_mostrar_lista_de_productos = False

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
                        "precio de venta", "precio de mercado", "precio de venta al público"
                        "precio de catálogo", "precio de referencia", "precio de tarifa"
                        "precio de lista", "precio de liquidación", "precio de salida",
                        "precio de saldo"
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
                "values": {
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                }
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
                "values": {
                    # leer cada product["type"] y hacer una lista de todos
                    # los product["title"] que coincidan en el tipo
                }
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
                        "especificacion", "atributos", "propiedades", "funciones", "madera"
                    ],
                }
            }
        ]
    },
    {
        "intent": "mostrar_lista_de_productos",
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
                "type": "lista",
                "values": {
                    "lista": [
                        "muéstrame los productos", "dime qué productos", "qué productos tienes",
                        "enséñame los productos", "quiero ver los productos", "lista de productos",
                        "productos disponibles", "qué productos hay", "qué productos están disponibles",
                        "quiero ver la lista de productos", "puedes mostrarme los productos",
                        "puedes decirme qué productos tienes", "qué productos puedes ofrecerme",
                        "qué productos están en stock", "qué productos están en existencia"
                    ]
                }
            }
        ]
    }
]

def generate_synonyms(product):
    if product["type"]:
        product_type = product["type"][0]
        for i in intents_data:
            if product_type not in i["entities"][0]["values"]:
                i["entities"][0]["values"][product_type] = []
                i["entities"][0]["values"][product_type].append(product_type )
                i["entities"][0]["values"][product_type].append(product["title"])
            else:
                i["entities"][0]["values"][product_type].append(product["title"])
        

def generate_intent_examples(product):
    global executed_mostrar_lista_de_productos
    
    for t in product["type"]:
        for i in intents_data:
            if i["intent"] == "saber_precio":
                input = [
                    {
                        "text": "¿Cuánto cuesta el " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 18,
                                "length": len(product['title'])
                            },
                            {
                                "category": "precio",
                                "offset": 8,
                                "length": 6
                            }
                        ]
                    },
                    {
                        "text": "¿Cuál es el precio del " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 23,
                                "length": len(product['title'])
                            },
                            {
                                "category": "precio",
                                "offset": 12,
                                "length": 6
                            }
                        ]
                    },
                    {
                        "text": "¿cuales son los " + product["type"] + " mas caros?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 16,
                                "length": len(product['title'])
                            },
                            {
                                "category": "precio",
                                "offset": 21 + len(product['title']),
                                "length": 5
                            }
                        ]
                    },
                    {
                        "text": "¿cuales son los " + product["type"] + " mas baratos?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 16,
                                "length": len(product['title'])
                            },
                            {
                                "category": "precio",
                                "offset": 21 + len(product['title']),
                                "length": 5
                            }
                        ]
                    }
                ]
                i["examples"].append(input[0])
                
            elif i["intent"] == "saber_disponibilidad":
                input = [
                    {
                        "text": "¿Cuándo estaría disponible el " + product['title']+ "?",                         
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 30,
                                "length": len(product['title'])
                            },
                            {
                                "category": "disponibilidad",
                                "offset": 16,
                                "length": 10
                            }
                        ]
                    },
                    {
                        "text": "¿En que fecha puedo tener el " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 29,
                                "length": len(product['title'])
                            },
                            {
                                "category": "disponibilidad",
                                "offset": 8,
                                "length": 5
                            }
                        ]
                    }
                ]
                i["examples"].append(input[0])
                
            elif i["intent"] == "saber_redireccion":
                input = [
                    {
                        "text": "dame el enlace de " + product['title'],
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 18,
                                "length": len(product['title'])
                            },
                            {
                                "category": "enlace",
                                "offset": 8,
                                "length": 6
                            }
                        ]
                        
                    },
                    {
                        "text": "¿donde puedo comprar el producto " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 33,
                                "length": len(product['title'])
                            },
                            {
                                "category": "enlace",
                                "offset": 13,
                                "length": 7
                            }
                        ]
                    }
                ]
                i["examples"].append(input[0])
                i["examples"].append(input[1])
                
            elif i["intent"] == "saber_caracteristicas":
                input = [
                    {
                        "text": "dame las caracteristicas de " + product['title'],
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 28,
                                "length": len(product['title'])
                            },
                            {
                                "category": "caracteristicas",
                                "offset": 9,
                                "length": 15
                            }
                        ]
                    },
                    {
                        "text": "¿cuales son las caracteristicas del " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 36,
                                "length": len(product['title'])
                            },
                            {
                                "category": "caracteristicas",
                                "offset": 16,
                                "length": 15
                            }
                        ]
                    }
                ]
                
                wood_input = [
                    {
                        "text": "¿que tipo de madera tiene el " + product['title'] + "?",
                        "entities": [
                            {
                                "category": "producto",
                                "offset": 29,
                                "length": len(product['title'])
                            },
                            {
                                "category": "caracteristicas",
                                "offset": 13,
                                "length": 6
                            }
                        ]
                    }
                ]
                
                i["examples"].append(input[0])
                i["examples"].append(input[1])
                if(product["type"] == "guitarra" or product["type"] == "bajo" or product["type"] == "ukelele"):
                    i["examples"].append(wood_input[0])
                
            elif i["intent"] == "mostrar_lista_de_productos":
                if not executed_mostrar_lista_de_productos:
                    for kw in keywords:
                        input = [
                            {
                                "text": "¿Que productos tienen " + kw,
                                "entities": [
                                    {
                                        "category": "producto",
                                        "offset": 5,
                                        "length": 9
                                    },
                                    {
                                        "category": "lista",
                                        "offset": 22,
                                        "length": len(kw)
                                    }
                                ]
                            }
                        ]
                        i["examples"].append(input[0])
                    executed_mostrar_lista_de_productos = True
                else:
                    print("Intent ya ejecutado.")
            else:
                print("Intent no encontrado.")
                break
        

def create_conversational_file(intents_data):

    # Agregar intents
    for intent in intents_data:
        clu_template["assets"]["intents"].append({"category": intent["intent"]})

        for entity in intent["entities"]:
            entity_category = entity["type"]
            sublist = []
            for key, values in entity["values"].items():
                elements = []
                for value in values:
                    elements.append(value)
                sublist.append({
                    "listKey": key,
                    "synonyms": [
                        {
                            "language": "es",
                            "values": elements
                        }
                    ]
                })
            
            # Verificar si la categoría ya existe antes de añadirla
            if not any(e["category"] == entity_category for e in clu_template["assets"]["entities"]):
                clu_template["assets"]["entities"].append({
                    "category": entity_category,
                    "compositionSetting": "separateComponents",
                    "list": {"sublists": sublist}
                })
        
        for example in intent["examples"]:
            clu_template["assets"]["utterances"].append({
                "text": example["text"],
                "intent": intent["intent"],
                "language": "es",
                "dataset": "train",
                "entities": example["entities"]
            })

    return clu_template

# Generar intents
for product in products:
    generate_synonyms(product)
    generate_intent_examples(product)

# Guardar archivo JSON de intents
try: 
    with open('azure-clu/structured-entities.json', 'w', encoding='utf-8') as f:
        json.dump(intents_data, f, ensure_ascii=False, indent=4)
    print("archivo JSON guardado correctamente.")
except Exception as e:
    print("Error al guardar archivo JSON de intents:", e)
    
# Crear JSON de CLU solo una vez después del bucle
clu_project = create_conversational_file(intents_data)

# Guardar archivo CLU
with open('azure-clu/clu_project.json', 'w', encoding='utf-8') as f:
    json.dump(clu_project, f, ensure_ascii=False, indent=4)

print("Archivos generados correctamente.")
