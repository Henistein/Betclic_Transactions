import sys
from bs4 import BeautifulSoup

depositos_file = sys.argv[1]
levantamentos_file = sys.argv[2]

with open(depositos_file, 'r') as f:
    depositos_content = f.read()

with open(levantamentos_file, 'r') as f:
    levantamentos_content = f.read()

soup = BeautifulSoup(depositos_content, 'html.parser')

# List to store the transactions
depositos_ammount = []
depositos_text = []
# Find all the divs with the class "myAccount_boxTitleContent"
box_ammount_contents = soup.find_all('div', class_='myAccount_boxTitleContent')
box_titled_contents = soup.find_all('div', class_='myAccount_boxTitleEnd')

for box in box_ammount_contents:
    # Extract the amount from the span with class "myAccount_amount"
    amount_span = box.find('span', class_='myAccount_amount')
    amount = amount_span.text.strip() if amount_span else None
    depositos_ammount.append(amount)

for box in box_titled_contents:
    # Extract the amount from the span with class "myAccount_amount"
    titled_span = box.find('span', class_='tag_label')
    titled_text = titled_span.text
    depositos_text.append(titled_text)

depositos = list(zip(depositos_ammount, depositos_text))

soup = BeautifulSoup(levantamentos_content, 'html.parser')

# List to store the transactions
levantamentos_ammount = []
levantamentos_text = []
# Find all the divs with the class "myAccount_boxTitleContent"
box_ammount_contents = soup.find_all('div', class_='myAccount_boxTitleContent')
box_titled_contents = soup.find_all('div', class_='myAccount_boxTitleEnd')

for box in box_ammount_contents:
    # Extract the amount from the span with class "myAccount_amount"
    amount_span = box.find('span', class_='myAccount_amount')
    amount = amount_span.text.strip() if amount_span else None
    levantamentos_ammount.append(amount)

for box in box_titled_contents:
    # Extract the amount from the span with class "myAccount_amount"
    titled_span = box.find('span', class_='tag_label')
    titled_text = titled_span.text
    levantamentos_text.append(titled_text)

levantamentos = list(zip(levantamentos_ammount, levantamentos_text))

import re
soma_depositos = []
for i in range(len(depositos)):
    dep = depositos[i]
    if dep[1] == 'Confirmado':
        numeric_amount = float(re.search(r'[\d,]+', dep[0]).group().replace(',', '.'))
        soma_depositos.append(numeric_amount)

soma_levantamentos = []
for i in range(len(levantamentos)):
    dep = levantamentos[i]
    if dep[1] == 'Confirmado':
        numeric_amount = float(re.search(r'[\d,]+', dep[0]).group().replace(',', '.'))
        soma_levantamentos.append(numeric_amount)


print(sum(soma_depositos) - sum(soma_levantamentos))