import re

with open('video1_clean.txt', 'r', encoding='utf-8') as f:
    v1_text = f.read()

with open('video2_clean.txt', 'r', encoding='utf-8') as f:
    v2_text = f.read()

print("=== ANALYSIS OF VIDEO 1: Cómo convertir tu LinkedIn en una página web profesional con IA ===")
print("Snippet beginning:", v1_text[:800])
print("\nSnippet middle:", v1_text[len(v1_text)//2:len(v1_text)//2 + 800])
print("\nSnippet end:", v1_text[-800:])

print("\n" + "="*80 + "\n")

print("=== ANALYSIS OF VIDEO 2: El Método Definitivo para Captar Clientes con LinkedIn + IA Online ===")
print("Snippet beginning:", v2_text[:800])
print("\nSnippet middle:", v2_text[len(v2_text)//2:len(v2_text)//2 + 800])
print("\nSnippet end:", v2_text[-800:])
