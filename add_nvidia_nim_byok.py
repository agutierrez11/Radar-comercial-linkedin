"""
add_nvidia_nim_byok.py
Adds NVIDIA NIM API Key input field to BYOK Modal in staging.html and index.html,
and saves/restores rc_nvidia_api_key in localStorage.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DIR = os.path.dirname(os.path.abspath(__file__))

def patch_file(file_name):
    file_path = os.path.join(DIR, file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    nvidia_input_html = """
              <!-- NVIDIA NIM API KEY -->
              <div style="margin-bottom:12px;">
                <label style="display:block; font-size:10px; font-weight:600; margin-bottom:3px; color:var(--green); font-family:'JetBrains Mono',monospace;">🟢 NVIDIA NIM API Key (Nemotron 70B / Llama 3.3)</label>
                <input type="password" id="nvidia-api-key" placeholder="nvapi-..." style="width:100%; font-size:11px; padding:6px 10px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">
              </div>
"""

    if 'id="nvidia-api-key"' not in html:
        html = html.replace('<div style="margin-bottom:12px;">\n                <label style="display:block; font-size:10px;', nvidia_input_html + '\n              <div style="margin-bottom:12px;">\n                <label style="display:block; font-size:10px;', 1)

    # Patch saving/restoring rc_nvidia_api_key
    save_restore_js = """
  // Load NVIDIA Key
  const savedNvidia = localStorage.getItem('rc_nvidia_api_key') || '';
  const nvidiaInput = document.getElementById('nvidia-api-key');
  if (nvidiaInput && savedNvidia) nvidiaInput.value = savedNvidia;
"""

    if "rc_nvidia_api_key" not in html:
        html = html.replace("document.getElementById('ai-config-modal').style.display = 'flex';", "document.getElementById('ai-config-modal').style.display = 'flex';\n" + save_restore_js)

    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html)
    print(f"NVIDIA_BYOK_PATCHED: {file_name}")

patch_file("staging.html")
patch_file("index.html")
