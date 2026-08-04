import csv
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

city_country_map = {
    'CDMX': 'México', 'Mexico City': 'México', 'Ciudad de México': 'México', 'Monterrey': 'México', 'Guadalajara': 'México', 'Puebla': 'México', 'Queretaro': 'México', 'Querétaro': 'México', 'Merida': 'México', 'Mérida': 'México', 'Tijuana': 'México', 'Leon': 'México', 'Cancun': 'México', 'Toluca': 'México', 'Saltillo': 'México', 'Hermosillo': 'México', 'Aguascalientes': 'México',
    'Bogota': 'Colombia', 'Bogotá': 'Colombia', 'Medellin': 'Colombia', 'Medellín': 'Colombia', 'Cali': 'Colombia', 'Barranquilla': 'Colombia', 'Cartagena': 'Colombia',
    'Lima': 'Perú', 'Arequipa': 'Perú',
    'Santiago': 'Chile', 'Santiago Metropolitan': 'Chile', 'Región Metropolitana': 'Chile', 'Valparaiso': 'Chile',
    'Buenos Aires': 'Argentina', 'Cordoba': 'Argentina', 'Rosario': 'Argentina', 'Mendoza': 'Argentina',
    'Madrid': 'España', 'Barcelona': 'España', 'Valencia': 'España', 'Sevilla': 'España', 'Zaragoza': 'España', 'Malaga': 'España',
    'Sao Paulo': 'Brasil', 'São Paulo': 'Brasil', 'Rio de Janeiro': 'Brasil', 'Belo Horizonte': 'Brasil', 'Curitiba': 'Brasil',
    'Miami': 'Estados Unidos', 'New York': 'Estados Unidos', 'San Francisco': 'Estados Unidos', 'Los Angeles': 'Estados Unidos', 'Chicago': 'Estados Unidos', 'Texas': 'Estados Unidos', 'Greater Seattle Area': 'Estados Unidos', 'Washington': 'Estados Unidos', 'Boston': 'Estados Unidos', 'San Diego': 'Estados Unidos', 'Dallas': 'Estados Unidos', 'Houston': 'Estados Unidos', 'Austin': 'Estados Unidos',
    'San Jose': 'Costa Rica', 'San José': 'Costa Rica',
    'Panama': 'Panamá', 'Panamá': 'Panamá', 'Ciudad de Panamá': 'Panamá',
    'San Salvador': 'El Salvador',
    'Guatemala': 'Guatemala', 'Ciudad de Guatemala': 'Guatemala',
    'Quito': 'Ecuador', 'Guayaquil': 'Ecuador',
    'Caracas': 'Venezuela', 'Maracaibo': 'Venezuela',
    'Montevideo': 'Uruguay',
    'Asuncion': 'Paraguay', 'Asunción': 'Paraguay',
    'La Paz': 'Bolivia', 'Santa Cruz': 'Bolivia',
    'Santo Domingo': 'República Dominicana',
    'San Juan': 'Puerto Rico',
    'London': 'Reino Unido', 'Paris': 'Francia', 'Berlin': 'Alemania', 'Rome': 'Italia', 'Toronto': 'Canadá', 'Montreal': 'Canadá', 'Vancouver': 'Canadá'
}

def guess_country(text):
    text_lower = text.lower()
    for city, country in city_country_map.items():
        if city.lower() in text_lower:
            return country
    return "Desconocido"

def main():
    rows = []
    with open('radar_database_final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
            
    fixed_count = 0
    for row in rows:
        if row['Location'] == 'Desconocido':
            # Intentar deducir de Company, Position o Google Snippet
            text_to_search = f"{row['Company']} {row['Position']} {row['Google Snippet']}"
            country = guess_country(text_to_search)
            if country != "Desconocido":
                row['Location'] = country
                fixed_count += 1
                
    with open('radar_database_final.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Reparados: {fixed_count} perfiles.")
    
if __name__ == "__main__":
    main()
