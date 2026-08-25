import re, json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract contacts array or test criteria logic against contacts
print("Analyzing criteria counts...")
# Let's inspect where 447 could come from
