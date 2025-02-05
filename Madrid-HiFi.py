import requests
from bs4 import BeautifulSoup
import json

# URL de la página que deseas analizar
print("======================================================================")
print("                 Bienvenido a Madrid HiFi Web Scraper")
print("======================================================================")
query = input("Introduce la marca de la que deseas obtener información: ")
url = 'https://www.madridhifi.com/m/' + query + '/'
base_url = 'https://www.madridhifi.com'
# Lista de palabras clave para identificar el tipo de producto
keywords = [
    'guitarra', 'bajo', 'pedal guitarra', 'cuerdas', 'ukelele',
    'pedal bajo', 'funda', 'funda guitarra electrica', 
    'funda guitarra acustica', 'funda bajo', 'signature',
    'amplificador', 'cable', 'correa', 'pua', 'pedal'
    'pastilla', 'pedalera', 'saxofon', 'trompeta',
    'bateria', 'bateria electronica', 'cajon',
    'piano', 'teclado', 'microfono', 'altavoz',
    'auriculares', 'mezclador', 'interface audio',
    'sintetizador', 'pedal efectos', 'banqueta piano',
]

# Realizar la solicitud a la página
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar todos los productos en la página
    product_cards = soup.find_all('div', class_='product_card')
    
    products = []
    
    for card in product_cards:
        try:
            # Obtener el título del producto
            title = card.find('div', class_='product_title').get_text(strip=True)
            
            # Obtener el precio actual
            price = card.find('div', class_='actual_price').get_text(strip=True)
            price = price.replace('€', '').strip()
            if ',' not in price:
                price += ',00'
            
            
            # Obtener el precio anterior (si está disponible)
            old_price = card.find('div', class_='product_old_price')
            old_price = old_price.get_text(strip=True).replace('€', '').strip() if old_price else 'No disponible'
            if ',' not in old_price:
                old_price += ',00'
            
            # Calcular el precio de reducción
            price_reduction = "None"
            if old_price != 'No disponible':
                old_price_num = float(old_price.replace(',', '').strip())
                price_num = float(price.replace(',', '').strip())
                if old_price_num > price_num:
                    price_reduction = round(((old_price_num - price_num) / old_price_num) * 100, 2)
            
            # Obtener la disponibilidad y separarla
            availability = card.find('div', class_='product_availibility')
            availability_text = availability.get_text(strip=True) if availability else 'No disponible'
            
            # Separar la disponibilidad en dos partes: "En stock" y la fecha de entrega
            availability_parts = availability_text.split('Recíbelo entre') if 'Recíbelo entre' in availability_text else [availability_text, '']
            in_stock = availability_parts[0].strip()
            delivery_date = availability_parts[1].strip() if len(availability_parts) > 1 else ''
            
            # url Producto
            product_url = card.find('a')['href'] if card.find('a') else None
                # Corregir el enlace del producto para que sea completo
            if product_url and not product_url.startswith('http'):
                product_url = base_url + product_url
            # Identificar el tipo de producto
            product_type = []
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    product_type.append(keyword)
            
            price += ' €'    
            old_price += ' €'    
            
            # consultar product_url para obtener más información y sacar la descripción
            product_response = requests.get(product_url)
            if product_response.status_code == 200:
                # Parsear el HTML
                soup = BeautifulSoup(product_response.text, 'html.parser')
                
                # Encontrar la lista con las características del producto
                texto_completo_div = soup.find('div', id='textoCompleto')
                features_list = texto_completo_div.find('ul')
                
                # Extraer y analizar cada elemento de la lista
                features = [item.text for item in features_list.find_all('li')]
            else:
                description = 'No disponible'
            
            # Almacenar la información en un diccionario
            product_info = {
                "title": title,
                "current_price": price,
                "old_price": old_price,
                "price_reduction": price_reduction,
                "availability": in_stock,
                "delivery_date": delivery_date,
                "url": product_url,
                "type": product_type,
                "features": features
            }
            
            # Añadir el diccionario a la lista de productos
            products.append(product_info)
            print(f"Producto {title} añadido a la lista")
            
        except Exception as e:
            print(f"Error procesando el producto: {e}")
            continue
        
    # Guardar la lista de productos en un archivo JSON
    with open('data/' + query + '.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print("Información de productos guardada en " + query + ".json")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
