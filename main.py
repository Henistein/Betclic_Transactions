import sys
import re
from bs4 import BeautifulSoup
from enum import Enum

class PaymentType(Enum):
  DEPOSIT = "deposit"
  WITHDRAW = "withdrawal" 

data_file = sys.argv[1]

with open(data_file, 'r') as f:
  data = f.read()

def extract_transactions(soup: BeautifulSoup, type: PaymentType) -> list:
  tab = soup.find(f'bc-payment-history-{type.value}', class_='w_100 is-active ng-star-inserted')
  box_ammount_contents = tab.find_all('div', class_='myAccount_boxTitleContent')
  box_titled_contents = tab.find_all('div', class_='myAccount_boxTitleEnd')

  ammounts, titles = [], []

  for box in box_ammount_contents:
    # Extract the amount from the span with class "myAccount_amount"
    amount_span = box.find('span', class_='myAccount_amount')
    ammounts.append(amount_span.text.strip())

  for box in box_titled_contents:
    # Extract the title from the span with class "tab_label"
    titled_span = box.find('span', class_='tag_label')
    titles.append(titled_span.text)

  return list(zip(ammounts, titles))

def calculate_sum(lst):
  ret = []
  for i in range(len(lst)):
    if lst[i][1] == 'Confirmado':
      numeric_amount = float(re.search(r'[\d,]+', lst[i][0]).group().replace(',', '.'))
      ret.append(numeric_amount)
  return ret

if __name__ == '__main__':
  soup = BeautifulSoup(data, 'html.parser')

  deposits = extract_transactions(soup, PaymentType.DEPOSIT)
  withdrawls = extract_transactions(soup, PaymentType.WITHDRAW)

  dep_sum = calculate_sum(deposits)
  wit_sum = calculate_sum(withdrawls)

  profit = -(sum(dep_sum) - sum(wit_sum))

  print(f'Profit: {round(profit, 2)}€')