import zipfile
import csv
import io
import sys

# Configure stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open('Connections.csv') as f:
            text_file = io.TextIOWrapper(f, encoding='utf-8')
            reader = csv.reader(text_file)
            header = next(reader)
            print("Header:", header)
            for i in range(5):
                print(next(reader))
except Exception as e:
    print(f"Error reading Connections.csv: {e}")

