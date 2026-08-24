with open('exhaustive_qa_audit.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("8890", "8888")

with open('exhaustive_qa_audit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Port updated to 8888")
