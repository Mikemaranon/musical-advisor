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

    for product in product_cards:
        try:
            # Obtener el título del producto
            title_brand = product.find("span", class_="title__manufacturer")
            title_brand = title_brand.text.strip() if title_brand else ""
            title_tag = product.find("span", class_="title__name")
            title_tag = title_tag.text.strip() if title_tag else "none"
            title = title_brand + " " + title_tag

            print(title)
            
            # Obtener el precio actual
            price_st = product.find('span', class_='fx-typography-price-primary fx-price-group__primary product__price-primary').get_text(strip=True)
            price = price_st.replace('€', '').strip()
            if ',' not in price and price != "":
                price += ',00'
            
            print(price)
            
            # Extraer el precio antiguo (tachado)
            try: 
                old_price = soup.find('span', class_="fx-typography-price-secondary fx-typography-price-secondary--strike fx-price-group__strike product__price-strike").text.strip()
                old_price = old_price.replace('€', '').strip()
                if ',' not in old_price:
                    old_price += ',00'
            except:
                old_price = "No disponible"
            
            print(old_price)
            
            # Obtener la disponibilidad del producto
            availability = product.find("span", class_="fx-availability")
            availability = availability.text.strip() if availability else "none"
            
            print(availability)
            
            # Obtener el enlace al producto
            product_url = product.find("a", class_="product__content no-underline")
            product_url = product_url["href"] if product_url else "none"
            
            print(product_url)
            
            # No hay información directa sobre la reducción de precio y la fecha de entrega
            price_reduction = "none"
            delivery_date = "unknown"
            
            # Clasificación del producto
            product_type = []
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    product_type.append(keyword)
            
            price += ' €'    
            old_price += ' €' 
            
            print("hasta aquí todo bien")
            
            # Características del producto
            features = []            
            product_response = requests.get(product_url)
            if product_response.status_code == 200:
                # Parsear el HTML
                soup = BeautifulSoup(product_response.text, 'html.parser')
                
                # Encontrar la lista con las características del producto
                texto_completo_div = soup.find('div', class_='text-original js-prod-text-original ')
                features_list = texto_completo_div.find('ul')
                
                # Extraer y analizar cada elemento de la lista
                features = [item.text for item in features_list.find_all('li')]
            else:
                description = 'No disponible'
            
            product_info = {
                "title": title,
                "current_price": price,
                "old_price": old_price,
                "price_reduction": price_reduction,
                "availability": availability,
                "delivery_date": delivery_date,
                "url": product_url,
                "type": product_type,
                "features": features
            }
            
            products.append(product_info)
            print(f"Producto {title} añadido a la lista")
            
        except Exception as e:
            print(f"Error procesando el producto: {e}")
            continue
    # Guardar la lista de productos en un archivo JSON
    with open('thomann-data/' + query + '.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print("Información de productos guardada en " + query + ".json")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
