import os
import json
import urllib.request
import urllib.parse

# Config
BOT_TOKEN = "8490697588:AAHeC-QumamVg4X9RIyoaHijyeNJTmdo0xY"
ALLOWED_CHAT_ID = 1373770013
output_file = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\IDEAS_TELEGRAM.md"

def fetch_telegram_ideas():
    print("Checking Telegram for new ideas...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    # Load offset if we processed updates before
    offset_file = r"C:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\.telegram_offset"
    offset = None
    if os.path.exists(offset_file):
        with open(offset_file, "r") as f:
            try:
                offset = int(f.read().strip())
            except:
                pass
                
    params = {}
    if offset:
        params["offset"] = offset
        
    query_string = urllib.parse.urlencode(params)
    if query_string:
        full_url = f"{url}?{query_string}"
    else:
        full_url = url
        
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if not data.get("ok"):
                print("Telegram API returned error:", data)
                return
                
            updates = data.get("result", [])
            if not updates:
                print("No new messages on Telegram.")
                return
                
            new_ideas_count = 0
            max_update_id = 0
            
            # Ensure file exists
            if not os.path.exists(output_file):
                with open(output_file, "w", encoding="utf-8") as out:
                    out.write("# 📓 Ideas Recibidas desde Telegram\n\nEste archivo recopila las notas de voz y texto que envías a tu bot de Telegram en la noche.\n\n")
            
            with open(output_file, "a", encoding="utf-8") as out:
                for update in updates:
                    update_id = update["update_id"]
                    max_update_id = max(max_update_id, update_id)
                    
                    message = update.get("message", {})
                    chat = message.get("chat", {})
                    chat_id = chat.get("id")
                    
                    # Only accept messages from Antonio
                    if chat_id == ALLOWED_CHAT_ID:
                        text = message.get("text")
                        date_timestamp = message.get("date")
                        date_str = ""
                        if date_timestamp:
                            date_str = datetime.fromtimestamp(date_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            date_str = "Fecha desconocida"
                            
                        if text:
                            print(f"New idea received: {text[:30]}...")
                            out.write(f"### 📝 Nota del {date_str}\n")
                            out.write(f"> {text}\n\n")
                            out.write("---\n\n")
                            new_ideas_count += 1
            
            # Confirm receipt of updates to Telegram by advancing offset
            if max_update_id > 0:
                with open(offset_file, "w") as f:
                    f.write(str(max_update_id + 1))
                    
            if new_ideas_count > 0:
                print(f"Successfully saved {new_ideas_count} new ideas to {output_file}")
            else:
                print("No new ideas from your specific chat ID.")
                
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")

if __name__ == "__main__":
    # Import datetime inside main context
    from datetime import datetime
    fetch_telegram_ideas()
