import requests
import json
import csv

url = "https://observatorioagroalimentar.gov.pt/wp-admin/admin-ajax.php"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://observatorioagroalimentar.gov.pt',
    'Referer': 'https://observatorioagroalimentar.gov.pt/setor/batata/',
    'X-Requested-With': 'XMLHttpRequest',
    # Add your other headers here if necessary...
}

payload = {
    'action': 'get_produto_graph',
    'fase': '2',
    'product': '1027',
    'start_year': '2019',
    'start_period': '1',
    'end_year': '2025',
    'end_period': '4',
    'compare[]': '120'
}

response = requests.post(url, headers=headers, data=payload)
response_json = response.json()

# Parse the JSON strings inside the JSON response
labels = json.loads(response_json["labels_grafico"])
products = json.loads(response_json["produtos_graph_info"])

# Find the product with id 1027
product_data = None
for prod in products:
    if prod["id"] == 1027:
        product_data = prod["dados"]
        break

if product_data is None:
    raise ValueError("Product with id 1027 not found")

# Write to CSV
with open("potato_prices.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Period", "Price (€ / kg)"])
    for label, price in zip(labels, product_data):
        writer.writerow([label, price])
