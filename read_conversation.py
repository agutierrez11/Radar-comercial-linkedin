import os
import sys
import zipfile
import csv
import io
import re

# Paths
zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
output_file = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\conversation_transcript.md"

def search_conversation(contact_query):
    if not os.path.exists(zip_path):
        print(f"Zip file not found at: {zip_path}")
        return
        
    print(f"Searching for conversation with: '{contact_query}'...")
    
    # Normalize query
    query_norm = contact_query.lower().strip()
    
    conversation_ids = set()
    matching_names = set()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            with zip_ref.open('messages.csv') as f:
                text_file = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(text_file)
                header = next(reader)
                
                # Column indices
                conv_id_idx = header.index('CONVERSATION ID')
                conv_title_idx = header.index('CONVERSATION TITLE')
                from_idx = header.index('FROM')
                to_idx = header.index('TO')
                
                all_messages = []
                
                # First pass: find conversation IDs matching contact name
                for row in reader:
                    if len(row) <= max(conv_id_idx, conv_title_idx, from_idx, to_idx):
                        continue
                    
                    conv_id = row[conv_id_idx]
                    conv_title = row[conv_title_idx]
                    sender = row[from_idx]
                    recipient = row[to_idx]
                    
                    # Store message for second pass
                    all_messages.append(row)
                    
                    # Check matches in Title, Sender, or Recipient
                    if (query_norm in conv_title.lower() or 
                        query_norm in sender.lower() or 
                        query_norm in recipient.lower()):
                        conversation_ids.add(conv_id)
                        
                        # Capture name that matched
                        if query_norm in sender.lower():
                            matching_names.add(sender)
                        if query_norm in recipient.lower():
                            matching_names.add(recipient)
                        if conv_title and query_norm in conv_title.lower():
                            matching_names.add(conv_title)
                
                if not conversation_ids:
                    print(f"No conversation found matching '{contact_query}'.")
                    with open(output_file, "w", encoding="utf-8") as out:
                        out.write(f"# Búsqueda de Conversación: {contact_query}\n\nNo se encontró ninguna conversación que coincida.")
                    return
                
                print(f"Found matching conversations for names: {matching_names} (IDs: {conversation_ids})")
                
                # Second pass: extract and sort messages for those conversation IDs
                filtered_messages = []
                date_idx = header.index('DATE')
                content_idx = header.index('CONTENT')
                
                for row in all_messages:
                    conv_id = row[conv_id_idx]
                    if conv_id in conversation_ids:
                        filtered_messages.append(row)
                
                # Sort by date
                # Date format is usually: '2024-07-15 18:13:47 UTC' or similar, string sort is fine if ISO, 
                # but let's parse or sort string since it starts with YYYY-MM-DD
                filtered_messages.sort(key=lambda x: x[date_idx])
                
                # Write to markdown file
                with open(output_file, "w", encoding="utf-8") as out:
                    out.write(f"# 💬 Conversación con {', '.join(matching_names)}\n\n")
                    out.write(f"*Búsqueda realizada para:* `{contact_query}`\n")
                    out.write(f"*Total de mensajes:* `{len(filtered_messages)}`\n\n---\n\n")
                    
                    for msg in filtered_messages:
                        sender = msg[from_idx]
                        date = msg[date_idx]
                        content = msg[content_idx]
                        
                        # Clean content formatting (newlines, etc.)
                        content_clean = content.replace("<br>", "\n").replace("<br/>", "\n")
                        
                        # Format bubble
                        if "antonio gutierrez" in sender.lower() or "tono" in sender.lower():
                            out.write(f"### 👤 **Yo** (Antonio Gutiérrez)\n")
                        else:
                            out.write(f"### 👥 **{sender}**\n")
                            
                        out.write(f"*{date}*\n\n")
                        out.write(f"> {content_clean}\n\n")
                        out.write("---\n\n")
                
                print(f"Conversation extracted successfully to: {output_file}")
                
    except Exception as e:
        print(f"Error extracting conversation: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search_conversation(query)
    else:
        print("Usage: python read_conversation.py <contact_name>")
