import json
import csv
from collections import defaultdict

with open('hifi-data/ibanez.json', 'r', encoding='utf-8') as file:
    products = json.load(file)

global_questions = []

def generate_keyword_questions(data):
    keywords = []
    with open("azure-qna/keywords.txt") as f:
        keywords = [line.strip().lower() for line in f]

    # Generar preguntas y respuestas para cada palabra clave
    for keyword in keywords:
        filtered_items = [item for item in data if any(keyword in feature.lower() for feature in item["features"])]
        
        question = f"¿Qué instrumentos tienen {keyword}?"
        answer = "Los instrumentos que tienen {0} son:: ".format(keyword) + ";; ".join([f"[{item['title']}]({item['url']})" for item in filtered_items])
        
        global_questions.append({question: answer})
    
    return global_questions

def generate_discount_questions(data):
    # Agrupar productos por tipo
    products_by_type = defaultdict(list)
    for item in data:
        for product_type in item.get("type", []):  # Un producto puede tener varios tipos
            products_by_type[product_type].append(item)

    # Generar preguntas y respuestas
    questions = []
    for product_type, products in products_by_type.items():
        # Ordenar los productos del tipo actual por "price_reduction"
        top_products = sorted(products, key=lambda x: x.get("price_reduction", 0), reverse=True)[:5]

        # Crear la pregunta
        question = f"¿Cuáles son l@s {product_type} más rebajados?"
        answer = f"L@s {product_type} con mayor descuento son:: " + ";; ".join([
            f"[{item['title']}]({item['url']}) - {item['price_reduction']}% de descuento - {item['current_price']}€"
            for item in top_products
        ])

        global_questions.append({question: answer})

def analyze_prices(data):

    # Agrupar productos por tipo
    products_by_type = defaultdict(list)
    for item in data:
        for product_type in item.get("type", []):
            products_by_type[product_type].append(item)

    # Generar preguntas y respuestas
    questions = []
    for product_type, products in products_by_type.items():
        # Ordenar los productos dentro de cada tipo
        top_expensive = sorted(products, key=lambda x: float(x.get("current_price", "0").replace("€", "").replace(",", "").strip()), reverse=True)[:5]
        top_cheap = sorted(products, key=lambda x: float(x.get("current_price", "0").replace("€", "").replace(",", "").strip()))[:5]

        # Pregunta de los más caros
        question_expensive = f"¿Cuáles son los {product_type} más caros?"
        answer_expensive = f"Los {product_type} más caros son:: " + ";; ".join(
            [f"[{item['title']}]({item['url']}) - {item['current_price']}" for item in top_expensive]
        )
        global_questions.append({question_expensive: answer_expensive})

        # Pregunta de los más baratos
        question_cheap = f"¿Cuáles son los {product_type} más baratos?"
        answer_cheap = f"Los {product_type} más baratos son:: " + ";; ".join(
            [f"[{item['title']}]({item['url']}) - {item['current_price']}" for item in top_cheap]
        )
        global_questions.append({question_cheap: answer_cheap})

    return questions

def generate_delivery_date_questions(data):
    # Generar preguntas sobre la fecha de entrega para cada producto
    for item in data:
        if 'delivery_date' in item:
            question = f"¿Cuándo estará disponible para entrega el producto {item['title']}?"
            answer = f"El producto {item['title']} estará disponible para entrega el {item['delivery_date']}"
            global_questions.append({question: answer})

def generate_purchase_link_questions(data):
    # Generar preguntas con el enlace directo de compra para cada producto
    for item in data:
        if 'url' in item:
            question = f"¿Dónde puedo comprar el producto {item['title']}?"
            answer = f"Puedes comprar el producto {item['title']} [aquí]({item['url']})"
            global_questions.append({question: answer})

def generate_wood_type_questions(data):
    wood_keywords = [                                       # Lista de maderas comunes
        "pícea", "sapeli", "nyatoh", "nogal", 
        "arce", "caoba", "palosanto", "ébano", 
        "tilo", "aliso", "fresno", "basswood", 
        "ovangkol", "koa"
    ]  

    for item in data:
        wood_types = [wood for wood in wood_keywords if any(wood in feature.lower() for feature in item.get("features", []))]

        if wood_types:
            question = f"¿Qué tipos de madera tiene el producto {item['title']}?"
            answer = f"El producto {item['title']} está fabricado con:: {';; '.join(wood_types)}"
            global_questions.append({question: answer})

def save_questions_to_json(questions, filename="azure-qna/questions.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    
    print(f"Se han guardado las preguntas en {filename}")
    
def generate_text_file_from_questions(questions, filename="azure-qna/azure-questions.txt"):
    question_number = 1
    with open(filename, "w", encoding="utf-8") as f:
        for item in questions:
            for question, answer in item.items():
                f.write(f"{question_number}: {question}\n{answer}\n\n")
                question_number += 1
    print(f"Se ha creado el archivo {filename} con el formato adecuado.")

generate_keyword_questions(products)        # genera preguntas de palabras clave
generate_discount_questions(products)       # genera preguntas de descuentos por tipo de producto
analyze_prices(products)                    # genera preguntas de precios por tipo de producto
generate_delivery_date_questions(products)  # genera preguntas de fechas de entrega
generate_purchase_link_questions(products)  # genera preguntas de enlaces de compra
generate_wood_type_questions(products)      # genera preguntas de tipos de madera

generate_text_file_from_questions(global_questions)

global_questions.append(                    # añade el número total de preguntas
    {
        "numero de preguntas": len(global_questions)
    }
)  

save_questions_to_json(global_questions)

# Definir el nombre del archivo de salida TSV
tsv_filename = "azure-qna/questions_for_azure.tsv"

# Abrir el archivo TSV para escritura
with open(tsv_filename, 'w', newline='', encoding='utf-8') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    
    # Escribir la cabecera del archivo TSV
    tsv_writer.writerow(["Question", "Answer", "Source", "Metadata", "SuggestedQuestions", "IsContextOnly", "Prompts", "QnaId", "SourceDisplayName"])

    # Inicializar un contador para QnaId
    qna_id = 1

    # Recorrer todas las preguntas generadas
    for question_dict in global_questions:
        for question, answer in question_dict.items():
            if question != "numero de preguntas":  # Excluimos el contador total de preguntas
                # Escribir cada fila en el archivo TSV
                tsv_writer.writerow([
                    question,
                    answer,
                    "azure-questions.txt",  # Puedes cambiar esto por un nombre más adecuado si lo deseas
                    "",  # Metadata vacío
                    "[]",  # SuggestedQuestions vacío
                    "False",  # IsContextOnly siempre es False
                    "[]",  # Prompts vacío
                    qna_id,
                    "ask-hifi"  # Fuente o nombre que desees, en este caso se ha dejado como ejemplo
                ])
                qna_id += 1  # Incrementar el QnaId para la siguiente pregunta

print(f"El archivo TSV ha sido creado como {tsv_filename}")