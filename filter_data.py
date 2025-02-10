import json

# open json hifi-data/data.json
with open('hifi-data/data.json', 'r', encoding='utf-8') as file:
    products = json.load(file)

# print the type field of each product
for product in products:
    print(f"Title: {product['title']}, Type: {product['type']}")


# select every register with more than 1 element in type
filtered_data = [x for x in products if len(x['type']) > 1]
print(filtered_data)