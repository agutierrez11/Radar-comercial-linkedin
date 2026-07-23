import zipfile

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

with zipfile.ZipFile(zip_path, 'r') as z:
    for name in sorted(z.namelist()):
        info = z.getinfo(name)
        print(f"{name} ({info.file_size} bytes)")
