import csv

companies = ['bac', 'credomatic', 'promerica', 'banco general', 'banistmo', 'agricola', 'pagadito', 'yappy', 'zinli', 'ficohsa', 'atlantida', 'cuscatlan', 'banco nacional de panama', 'caja de ahorros', 'kushki', 'dlocal', 'ebanx', 'payu', 'mercado pago', 'clip', 'clip ', 'konfio', 'kueski']
keywords = ['pago', 'payment', 'pay', 'fintech', 'wallet', 'tarjeta', 'card', 'banco', 'bank', 'remesa', 'adquirente', 'adquiriente', 'visa', 'mastercard', 'stripe']

with open('Connections.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    connections = list(reader)

print('Searching for CA related companies or payments keywords in companies/positions...')
found_people = []

for row in connections:
    comp = row.get('Company', '').lower()
    pos = row.get('Position', '').lower()
    
    # Check if company is in known CA companies
    is_ca_company = any(c in comp for c in companies)
    
    # If it's a generic Latam/global payment company (dlocal, ebanx, payu, mastercard, visa), 
    # we might just list them anyway as they cover the ecosystem
    is_payment = any(k in comp or k in pos for k in keywords)
    
    # Let's filter to those in known CA companies OR (those in payments and having some CA hint? No CA hint in csv)
    # Let's just output those in the CA specific list, plus those in major LatAm players
    if is_ca_company or ('dlocal' in comp or 'kushki' in comp or 'ebanx' in comp):
        found_people.append(row)

for p in found_people:
    print(f"- {p.get('First Name', '')} {p.get('Last Name', '')} : {p.get('Position', '')} @ {p.get('Company', '')}")
print(f"Total found: {len(found_people)}")
