import requests
from bs4 import BeautifulSoup
import json

# URL de la página que deseas analizar
print("======================================================================")
print("                 Bienvenido a Thomann Web Scraper")
print("======================================================================")
query = input("Introduce la marca de la que deseas obtener información: ")
url = 'https://www.thomann.de/es/search_dir.html?sw=' + query
base_url = 'https://www.thomann.de'
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
    product_cards = soup.find_all('div', class_='fx-product-list-entry')
    
    products = []

    with open(url, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    for product in product_cards:
        try:
            # Obtener el título del producto
            title_tag = product.find("div", class_="product__title")
            title = title_tag.text.strip() if title_tag else "none"
            
            # Obtener el precio actual
            price = product.find('span', class_='fx-typography-price-primary').get_text(strip=True)
            price = price.replace('€', '').strip()
            if ',' not in price:
                price += ',00'
            
            # Extraer el precio antiguo (tachado)
            old_price = soup.select_one(".fx-typography-price-secondary--strike").text.strip()
            old_price = old_price.replace('€', '').strip()
            if ',' not in old_price:
                old_price += ',00'
            
            availability = product.find("span", class_="fx-availability")
            availability = availability.text.strip() if availability else "none"
            
            url = product.find("a", class_="product__content no-underline")
            url = url["href"] if url else "none"
            
            # No hay información directa sobre la reducción de precio y la fecha de entrega
            price_reduction = "none"
            delivery_date = "none"
            
            # Clasificación del producto (debe implementarse una lógica personalizada)
            type_tags = []  # Aquí se puede agregar una lógica basada en el título o descripción
            
            # Características (No disponibles en este HTML)
            features = []
            
            product_info = {
                "title": title,
                "current_price": price,
                "old_price": old_price,
                "price_reduction": price_reduction,
                "availability": availability,
                "delivery_date": delivery_date,
                "url": url,
                "type": type_tags,
                "features": features
            }
            
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
