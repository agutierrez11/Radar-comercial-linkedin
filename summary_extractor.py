import re

def summarize_file(filename, title):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        
    print(f"=== DETAILED BREAKDOWN OF {title} ({len(text)} chars) ===")
    
    # Extract topics, tool names, prompt hints, workflow steps
    tools = set(re.findall(r'\b(Cloud|Claude|Anthropic|Frontend Design|Awards|awwwards|Cursor|Vercel|Make|Zapier|Apollo|LinkedIn|v0|Bolt|Windsurf|ChatGPT|OpenAI|GPT|n8n|Python|React)\b', text, re.I))
    print(f"Key Tools / Tech Mentioned: {', '.join(tools)}")
    
    # Extract sections or key sentences
    paragraphs = [p for p in text.split('. ') if len(p) > 50]
    print(f"Sample key points ({len(paragraphs)} total sentences):")
    for i in range(0, len(paragraphs), max(1, len(paragraphs)//10)):
        print(f"  - {paragraphs[i][:150]}...")
    print("\n" + "="*80 + "\n")

summarize_file('video1_clean.txt', 'Video 1: Convertir LinkedIn en Web con IA')
summarize_file('video2_clean.txt', 'Video 2: Método Definitivo para Captar Clientes con LinkedIn + IA')
