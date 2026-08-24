import re

def update_login_modal(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacement HTML for #login-modal matching Minimalist Editorial UI protocol (Warm Off-White/Slate 900, zero gradients, crisp borders)
    old_modal_pattern = r'<div class="modal-overlay open" id="login-modal"[\s\S]*?</div>\s*</div>\s*</div>'
    
    new_modal_html = """<div class="modal-overlay open" id="login-modal" style="display:flex !important; opacity:1 !important; pointer-events:auto !important; z-index:99999 !important; background:rgba(15, 23, 42, 0.96); padding:20px; align-items:center; justify-content:center;">
  <div class="modal" style="max-width:440px; width:100%; padding:32px 28px; border-radius:12px; background:#0F172A; border:1px solid #334155; box-shadow:0 10px 30px rgba(0,0,0,0.5); font-family:'Outfit', sans-serif; color:#F8FAFC;">
    
    <!-- BRANDING HEADER -->
    <div style="text-align:center; margin-bottom:24px;">
      <div style="display:inline-flex; align-items:center; gap:8px; padding:4px 12px; background:#1E293B; border:1px solid #334155; border-radius:9999px; margin-bottom:12px;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; color:#A5B4FC; letter-spacing:0.06em; text-transform:uppercase;">MINERÍA DE RELACIONES B2B</span>
      </div>
      <h2 style="font-size:22px; font-weight:800; color:#F8FAFC; margin:0 0 6px 0; letter-spacing:-0.02em;">Radar Comercial</h2>
      <p style="font-size:13px; color:#94A3B8; margin:0; line-height:1.5;">Ingresa con tus credenciales asignadas.</p>
    </div>

    <!-- ERROR INLINE ALERT -->
    <div id="login-error-alert" style="display:none; background:#451A1A; border:1px solid #991B1B; color:#FCA5A5; padding:10px 14px; border-radius:8px; font-size:13px; font-weight:600; margin-bottom:18px; text-align:center;">
      ❌ Credenciales incorrectas. Verifique su usuario y contraseña.
    </div>

    <!-- FORMULARIO PRINCIPAL DE ACCESO -->
    <form id="login-form-card" onsubmit="event.preventDefault(); submitCustomLogin();" style="margin-bottom:24px; display:flex; flex-direction:column; gap:16px;">
      <div>
        <label for="login-username-input" style="font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; color:#94A3B8; display:block; margin-bottom:6px; letter-spacing:0.06em; text-transform:uppercase;">USUARIO O EMAIL</label>
        <input type="text" id="login-username-input" class="filter-input" placeholder="ej. giovanna o antonio@radar.com" required style="width:100%; height:44px; font-size:14px; padding:0 14px; border-radius:8px; background:#1E293B; border:1px solid #334155; color:#F8FAFC; outline:none; transition:border-color 0.2s;" onfocus="this.style.borderColor='#6366F1'" onblur="this.style.borderColor='#334155'">
      </div>
      
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <label for="login-password-input" style="font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.06em; text-transform:uppercase;">CONTRASEÑA / PIN</label>
        </div>
        <input type="password" id="login-password-input" class="filter-input" placeholder="••••••••" required style="width:100%; height:44px; font-size:14px; padding:0 14px; border-radius:8px; background:#1E293B; border:1px solid #334155; color:#F8FAFC; outline:none; transition:border-color 0.2s;" onfocus="this.style.borderColor='#6366F1'" onblur="this.style.borderColor='#334155'">
      </div>

      <button id="login-submit-btn" type="submit" style="width:100%; height:46px; font-size:14px; font-weight:700; border-radius:8px; background:#4F46E5; color:#FFFFFF; border:none; cursor:pointer; transition:background 0.2s ease; margin-top:4px;" onmouseover="this.style.background='#4338CA'" onmouseout="this.style.background='#4F46E5'">
        Entrar a mi bóveda
      </button>
    </form>

    <!-- SECCIÓN SECUNDARIA: ACCESOS DE DEMO / SELECCIÓN RÁPIDA -->
    <div style="border-top:1px solid #1E293B; padding-top:18px;">
      <div style="font-family:'JetBrains Mono', monospace; font-size:10px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:.08em; margin-bottom:12px; text-align:center;">
        DEMO ACCESO RÁPIDO
      </div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        <button type="button" class="mini-btn" onclick="fillQuickLogin('antonio', '12345')" style="padding:10px 14px; font-size:12px; font-weight:600; border-radius:8px; border:1px solid #334155; background:#1E293B; color:#CBD5E1; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:border-color 0.2s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          <span>👤 Antonio · Bóveda Master</span>
          <span style="font-size:11px; color:#818CF8; font-weight:700;">PIN: 12345</span>
        </button>
        <button type="button" class="mini-btn" onclick="fillQuickLogin('giovanna', 'gio2026')" style="padding:10px 14px; font-size:12px; font-weight:600; border-radius:8px; border:1px solid #334155; background:#1E293B; color:#CBD5E1; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:border-color 0.2s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          <span>🔒 Giovanna · Bóveda Privada</span>
          <span style="font-size:11px; color:#A7F3D0; font-weight:700;">0 contactos</span>
        </button>
        <button type="button" class="mini-btn" onclick="fillQuickLogin('ronan', 'ronan123')" style="padding:10px 14px; font-size:12px; font-weight:600; border-radius:8px; border:1px solid #334155; background:#1E293B; color:#CBD5E1; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:border-color 0.2s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          <span>🧪 Ronan · Sandbox</span>
          <span style="font-size:11px; color:#FDE68A; font-weight:700;">500 demo</span>
        </button>
      </div>
    </div>

  </div>
</div>"""

    content = re.sub(old_modal_pattern, new_modal_html, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Gym Cold card UI applied to {filepath}")

update_login_modal(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
update_login_modal(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
