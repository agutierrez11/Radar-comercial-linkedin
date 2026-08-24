"""
apply_welcome_gateway.py
Updates #login-modal in staging.html and index.html to the HarvestAPI-style
SaaS B2B Welcome Access Gateway with professional copy, Google OAuth placeholder,
clean credentials form, and secondary demo access section.
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DIR = os.path.dirname(os.path.abspath(__file__))

def update_welcome_gateway(file_name):
    file_path = os.path.join(DIR, file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. New Professional HarvestAPI-style Welcome Gateway Modal HTML
    new_modal_html = """<!-- ── PROFESSIONAL SAAS WELCOME ACCESS GATEWAY MODAL ── -->
<div class="modal-overlay" id="login-modal">
  <div class="modal" style="max-width:460px; padding:28px 24px; border-radius:16px; background:var(--surface); border:1px solid var(--border); box-shadow:0 20px 40px rgba(0,0,0,0.5); font-family:'Outfit',sans-serif;">
    
    <!-- BRANDING HEADER -->
    <div style="text-align:center; margin-bottom:20px;">
      <div style="display:inline-flex; align-items:center; gap:8px; font-weight:800; font-size:18px; color:var(--text); margin-bottom:4px;">
        <div style="background:var(--accent); color:#fff; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:16px;">📡</div>
        <span>RADAR <span style="color:var(--accent);">COMERCIAL</span></span>
      </div>
      <div style="font-size:11px; font-family:'JetBrains Mono',monospace; color:var(--text-muted); text-transform:uppercase; letter-spacing:.06em;">
        Relationship Intelligence & Warm Pipeline Mining
      </div>
    </div>

    <!-- TITLE & SUBTITLE -->
    <div style="text-align:center; margin-bottom:20px;">
      <h2 style="font-size:20px; font-weight:800; color:var(--text); margin-bottom:6px;">Accede a tu bóveda</h2>
      <p style="font-size:12px; color:var(--text-muted); line-height:1.5; margin:0;">
        Tu espacio privado para explorar tu red, tus conversaciones y tus oportunidades comerciales.
      </p>
    </div>

    <!-- GOOGLE OAUTH PLACEHOLDER -->
    <button class="mini-btn" onclick="showToast('🔑 Continuar con Google estará disponible próximamente en Supabase Auth.', '💡')" style="width:100%; padding:10px; font-size:13px; font-weight:700; border-radius:10px; border:1px solid var(--border); background:var(--bg); color:var(--text); cursor:pointer; display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:16px; transition:all 0.2s;">
      <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
      <span>Continuar con Google <span style="font-size:10px; opacity:0.6; font-weight:400;">(Próximamente)</span></span>
    </button>

    <!-- SEPARATOR -->
    <div style="display:flex; align-items:center; margin:16px 0; color:var(--text-muted); font-size:11px;">
      <div style="flex:1; height:1px; background:var(--border);"></div>
      <span style="padding:0 10px; font-weight:600; text-transform:lowercase;">o</span>
      <div style="flex:1; height:1px; background:var(--border);"></div>
    </div>

    <!-- FORMULARIO PRINCIPAL DE ACCESO -->
    <div style="margin-bottom:20px;">
      <div style="margin-bottom:12px;">
        <label style="font-size:11px; font-weight:600; color:var(--text); display:block; margin-bottom:6px;">Correo electrónico o ID de usuario</label>
        <input type="text" id="login-username-input" class="filter-input" placeholder="ej. antonio@radarcomercial.com" value="antonio" style="width:100%; font-size:13px; padding:10px 12px; border-radius:8px; background:var(--bg); border:1px solid var(--border); color:var(--text); outline:none;" onkeyup="if(event.key==='Enter') submitCustomLogin()">
      </div>
      <div style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <label style="font-size:11px; font-weight:600; color:var(--text);">Contraseña</label>
          <a href="#" onclick="showToast('🔑 Contacta al administrador para restablecer tu contraseña.', '💡'); return false;" style="font-size:11px; color:var(--accent); text-decoration:none; font-weight:600;">¿Olvidaste tu contraseña?</a>
        </div>
        <input type="password" id="login-password-input" class="filter-input" value="12345" style="width:100%; font-size:13px; padding:10px 12px; border-radius:8px; background:var(--bg); border:1px solid var(--border); color:var(--text); outline:none;" onkeyup="if(event.key==='Enter') submitCustomLogin()">
      </div>
      <button class="mini-btn primary" onclick="submitCustomLogin()" style="width:100%; padding:11px; font-size:14px; font-weight:700; border-radius:10px; background:linear-gradient(135deg, var(--accent), #4338ca); color:white; border:none; cursor:pointer; box-shadow:0 4px 12px rgba(79,70,229,0.3);">
        Entrar a mi bóveda
      </button>
    </div>

    <!-- SECCIÓN SECUNDARIA: ACCESOS DE DEMO / SELECCIÓN RÁPIDA -->
    <div style="border-top:1px solid var(--border); padding-top:16px;">
      <div style="font-size:11px; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:.05em; margin-bottom:10px; text-align:center;">
        ¿Explorando una demostración?
      </div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        <button class="mini-btn" onclick="quickLogin('antonio', '12345')" style="padding:9px 12px; justify-content:flex-start; font-size:12px; font-weight:600; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--text); display:flex; align-items:center; gap:8px;">
          👤 <span>Antonio · Bóveda personal</span>
          <span style="margin-left:auto; font-size:10px; color:var(--green); font-weight:700; background:rgba(16,185,129,0.1); padding:2px 6px; border-radius:4px;">2,953 contactos</span>
        </button>
        <button class="mini-btn" onclick="quickLogin('giovanna', '12345')" style="padding:9px 12px; justify-content:flex-start; font-size:12px; font-weight:600; border-radius:8px; border:1px solid var(--purple); color:var(--purple); background:rgba(124,58,237,0.06); display:flex; align-items:center; gap:8px;">
          👤 <span>Giovanna · Bóveda de prueba</span>
          <span style="margin-left:auto; font-size:10px; opacity:0.8; font-weight:500;">Bóveda privada</span>
        </button>
        <button class="mini-btn" onclick="quickLogin('ronan', '12345')" style="padding:9px 12px; justify-content:flex-start; font-size:12px; font-weight:600; border-radius:8px; border:1px solid var(--amber); color:var(--amber); background:rgba(245,158,11,0.06); display:flex; align-items:center; gap:8px;">
          🧪 <span>Ronan · Sandbox colaborativo</span>
          <span style="margin-left:auto; font-size:10px; opacity:0.8; font-weight:500;">500 demo BI</span>
        </button>
      </div>
    </div>

  </div>
</div>"""

    # Replace old login-modal HTML
    modal_regex = re.compile(r'<!-- ── AUTH LOGIN MODAL ── -->.*?<!-- AI & ENRICHMENT', re.DOTALL)
    if not modal_regex.search(html):
        modal_regex = re.compile(r'<div class="modal-overlay" id="login-modal">.*?<div class="modal-overlay" id="ai-config-modal">', re.DOTALL)

    html = modal_regex.sub(new_modal_html + "\n\n<!-- AI & ENRICHMENT", html)

    # 2. Add automatic popup trigger on page startup if not authenticated
    startup_trigger = """
    // Welcome Gateway Auto-Popup on Startup
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(function() {
        if (typeof openLoginModal === 'function') {
          openLoginModal();
        }
      }, 300);
    });
    """
    if "Welcome Gateway Auto-Popup on Startup" not in html:
        html = html.replace("</script>\n</body>", startup_trigger + "\n</script>\n</body>")

    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html)
    print(f"WELCOME_GATEWAY_UPDATED: {file_name}")

update_welcome_gateway("staging.html")
update_welcome_gateway("index.html")
