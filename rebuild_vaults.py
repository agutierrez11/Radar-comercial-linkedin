import os
import re
import shutil

# Paths
desktop_vault = r"C:\Users\Antonio\OneDrive\Escritorio\Boveda_Contactos_Linkedin"
obsidian_dir = r"C:\Users\Antonio\Bovedas_Obsidian"
vault_a_dir = os.path.join(obsidian_dir, "Boveda_Simple")
vault_b_dir = os.path.join(obsidian_dir, "Boveda_Estructurada")

# Make sure output directories exist
os.makedirs(vault_a_dir, exist_ok=True)
os.makedirs(vault_b_dir, exist_ok=True)

# 1. Parse Countries/Paises from 00_Hubs/01_Paises to build mapping of Contact Name -> Country
countries_dir = os.path.join(desktop_vault, "00_Hubs", "01_Paises")
contact_to_country = {}

print("Parsing country files...")
if os.path.exists(countries_dir):
    for filename in os.listdir(countries_dir):
        if filename.endswith(".md"):
            country_name = filename[:-3] # Remove .md
            filepath = os.path.join(countries_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # Find all lines starting with "- [["
                    lines = content.split("\n")
                    for line in lines:
                        if line.strip().startswith("- [["):
                            # Extract first link
                            match = re.search(r"-\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", line)
                            if match:
                                contact_name = match.group(1).strip()
                                contact_to_country[contact_name] = country_name
            except Exception as e:
                print(f"Error reading country file {filename}: {e}")

print(f"Mapped {len(contact_to_country)} contacts to their respective countries.")

# 2. Gather all contact md files in the original vault
contact_folders = [
    "01_Activos", "01_Red_Caliente", "02_Fosiles", "02_Reactivacion_Fosiles",
    "03_Ghosts_ClientesB2B", "03_Ghosts_Otros", "03_Ghosts_Talento",
    "03_Mina_Oro_Toku", "04_Mina_Oro_Netpay", "04_Ruido",
    "05_Talento_Empleadores", "06_Ruido_Ignorar"
]

contact_files_map = {} # Contact Name -> Full Path in original vault
for folder in contact_folders:
    folder_path = os.path.join(desktop_vault, folder)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                contact_name = filename[:-3]
                contact_files_map[contact_name] = os.path.join(folder_path, filename)

print(f"Found {len(contact_files_map)} actual contact files in original vault.")

# 3. Create VAULT A (Boveda_Simple)
# It should contain ONLY three folders: Pais, Sectores, Jerarquias
pais_a_dir = os.path.join(vault_a_dir, "Pais")
sectores_a_dir = os.path.join(vault_a_dir, "Sectores")
jerarquias_a_dir = os.path.join(vault_a_dir, "Jerarquias")

os.makedirs(pais_a_dir, exist_ok=True)
os.makedirs(sectores_a_dir, exist_ok=True)
os.makedirs(jerarquias_a_dir, exist_ok=True)

# Copy contact files into Pais/<Country>/
for contact_name, src_path in contact_files_map.items():
    country = contact_to_country.get(contact_name, "Otros Países")
    country_folder = os.path.join(pais_a_dir, country)
    os.makedirs(country_folder, exist_ok=True)
    dest_path = os.path.join(country_folder, f"{contact_name}.md")
    try:
        shutil.copy2(src_path, dest_path)
    except Exception as e:
        print(f"Error copying {contact_name}: {e}")

# Copy sector files to Sectores/
src_sectores_dir = os.path.join(desktop_vault, "00_Hubs", "02_Sectores")
if os.path.exists(src_sectores_dir):
    for filename in os.listdir(src_sectores_dir):
        if filename.endswith(".md"):
            try:
                shutil.copy2(os.path.join(src_sectores_dir, filename), os.path.join(sectores_a_dir, filename))
            except Exception as e:
                print(f"Error copying sector {filename}: {e}")

# Copy hierarchy files to Jerarquias/
src_jerarquias_dir = os.path.join(desktop_vault, "00_Hubs", "03_Jerarquias")
if os.path.exists(src_jerarquias_dir):
    for filename in os.listdir(src_jerarquias_dir):
        if filename.endswith(".md"):
            try:
                shutil.copy2(os.path.join(src_jerarquias_dir, filename), os.path.join(jerarquias_a_dir, filename))
            except Exception as e:
                print(f"Error copying hierarchy {filename}: {e}")

# Add a Master Note in Vault A root (00_Radar_Maestro.md)
radar_maestro_simple = """# 📡 Radar Maestro Simple

Esta es tu bóveda simple de contactos de LinkedIn organizada únicamente por tres dimensiones:

- **[[Pais/México|Países]]**: Organizados físicamente en carpetas por geografía.
- **[[Sectores/Fintech y Servicios Financieros|Sectores e Industrias]]**: Listados temáticos por sector.
- **[[Jerarquias/C-Level (CEO, CFO, Founder)|Jerarquías]]**: Listados por seniority (C-Levels, Gerentes, Directores).
"""
with open(os.path.join(vault_a_dir, "00_Radar_Maestro.md"), "w", encoding="utf-8") as f:
    f.write(radar_maestro_simple)

print("Vault A (Simple) created successfully.")

# 4. Create VAULT B (Boveda_Estructurada)
# Copy the structure of Vault B, but ignore dotfolders like .smart-env or .obsidian to avoid OneDrive lock errors
print("Creating Vault B (Estructurada)...")
for item in os.listdir(desktop_vault):
    # Ignore dotfiles/dotfolders (.obsidian, .smart-env) and empty folders
    if item.startswith(".") or item in ["Contactos", "Empresas", "Jerarquias"]:
        continue
    
    s = os.path.join(desktop_vault, item)
    d = os.path.join(vault_b_dir, item)
    try:
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".*"))
        else:
            shutil.copy2(s, d)
    except Exception as e:
        print(f"Error copying item {item} in Vault B: {e}")

# Double check and remove empty folders if they were copied
for folder in ["Contactos", "Empresas", "Jerarquias"]:
    fp = os.path.join(vault_b_dir, folder)
    if os.path.exists(fp):
        shutil.rmtree(fp)

# Clean up temporary post vault if it exists
post_vault = r"C:\Users\Antonio\Boveda_Post_Linkedin"
if os.path.exists(post_vault):
    try:
        shutil.rmtree(post_vault)
    except Exception:
        pass

print("All tasks completed successfully!")
