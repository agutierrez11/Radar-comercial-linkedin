import os
import json
import urllib.request
import urllib.parse

def load_env():
    """Reads local .env file without external dependencies."""
    env = {}
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

# Load config from .env
env_vars = load_env()
BOT_TOKEN = env_vars.get("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = int(env_vars.get("TELEGRAM_CHAT_ID", 0)) if env_vars.get("TELEGRAM_CHAT_ID") else None
output_file = os.path.join(os.path.dirname(__file__), "IDEAS_TELEGRAM.md")

def fetch_telegram_ideas():
    if not BOT_TOKEN or not ALLOWED_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in .env file.")
        return
        
    print("Checking Telegram for new ideas...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    offset_file = os.path.join(os.path.dirname(__file__), ".telegram_offset")
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
    from datetime import datetime
    fetch_telegram_ideas()
