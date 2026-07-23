import zipfile
import os

path1 = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
path2 = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip (1).zip"

print(f"Size of Zip 1: {os.path.getsize(path1)} bytes")
print(f"Size of Zip 2: {os.path.getsize(path2)} bytes")

with zipfile.ZipFile(path1) as z1, zipfile.ZipFile(path2) as z2:
    shares1 = z1.getinfo("Shares_577732310.csv")
    shares2 = z2.getinfo("Shares_577732310.csv")
    print(f"Shares CSV 1 Size: {shares1.file_size} bytes")
    print(f"Shares CSV 2 Size: {shares2.file_size} bytes")
    
    # Are the namelists identical?
    list1 = sorted(z1.namelist())
    list2 = sorted(z2.namelist())
    if list1 == list2:
        print("File lists in both ZIPs are identical.")
    else:
        print("File lists in both ZIPs differ!")
        print("Only in Zip 1:", set(list1) - set(list2))
        print("Only in Zip 2:", set(list2) - set(list1))
