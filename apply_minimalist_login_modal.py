import re

def patch_login_modal(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace #login-modal HTML with Minimalist Editorial UI design (Gym Cold style layout, NO neon/glassmorphism)
    old_modal_regex = r'<div id="login-modal"[\s\S]*?<!-- END LOGIN MODAL -->'
    
    new_modal_html = """<div id="login-modal" style="position:fixed; inset:0; z-index:9999999; background:rgba(15, 23, 42, 0.95); backdrop-filter:blur(8px); display:flex; align-items:center; justify-content:center; padding:20px;">
  <div style="width:100%; max-width:420px; background:#0F172A; border:1px solid #334155; border-radius:12px; padding:32px; box-shadow:0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5); font-family:'Outfit', system-ui, sans-serif; color:#F8FAFC;">
    
    <!-- HEADER -->
    <div style="text-align:center; margin-bottom:28px;">
      <div style="display:inline-flex; align-items:center; gap:8px; padding:4px 12px; background:#1E1B4B; border:1px solid #3730A3; border-radius:9999px; margin-bottom:12px;">
        <span style="font-size:12px; font-weight:700; color:#A5B4FC; letter-spacing:0.05em; text-transform:uppercase;">MINERÍA DE RELACIONES B2B</span>
      </div>
      <h2 style="font-size:24px; font-weight:800; color:#F8FAFC; margin:0 0 6px 0; letter-spacing:-0.02em;">Radar Comercial</h2>
      <p style="font-size:13px; color:#94A3B8; margin:0; line-height:1.5;">Ingresa con tus credenciales de bóveda o usuario asignado.</p>
    </div>

    <!-- ERROR ALERT (HIDDEN BY DEFAULT) -->
    <div id="login-error-alert" style="display:none; background:#451A1A; border:1px solid #991B1B; color:#FCA5A5; padding:10px 14px; border-radius:8px; font-size:13px; font-weight:600; margin-bottom:20px; text-align:center;">
      ❌ Credenciales incorrectas. Verifique usuario o contraseña.
    </div>

    <!-- FORM -->
    <form id="login-form-card" onsubmit="event.preventDefault(); submitCustomLogin();" style="display:flex; flex-direction:column; gap:18px;">
      
      <div>
        <label for="login-username-input" style="display:block; font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:6px;">USUARIO O EMAIL</label>
        <input id="login-username-input" type="text" placeholder="Ej. giovanna o antonio@radar.com" required style="width:100%; height:44px; background:#1E293B; border:1px solid #334155; border-radius:8px; padding:0 14px; font-size:14px; color:#F8FAFC; outline:none; transition:border-color 0.2s;" onfocus="this.style.borderColor='#6366F1'" onblur="this.style.borderColor='#334155'">
      </div>

      <div>
        <label for="login-password-input" style="display:block; font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; color:#94A3B8; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:6px;">CONTRASEÑA / PIN</label>
        <input id="login-password-input" type="password" placeholder="••••••••" required style="width:100%; height:44px; background:#1E293B; border:1px solid #334155; border-radius:8px; padding:0 14px; font-size:14px; color:#F8FAFC; outline:none; transition:border-color 0.2s;" onfocus="this.style.borderColor='#6366F1'" onblur="this.style.borderColor='#334155'">
      </div>

      <button id="login-submit-btn" type="submit" style="width:100%; height:46px; background:#4F46E5; border:none; border-radius:8px; font-size:14px; font-weight:700; color:#FFFFFF; cursor:pointer; transition:all 0.15s ease; margin-top:6px;" onmouseover="this.style.background='#4338CA'" onmouseout="this.style.background='#4F46E5'">
        Entrar a la Bóveda
      </button>

    </form>

    <!-- QUICK ACCESS PRESETS FOR DEMO -->
    <div style="margin-top:24px; padding-top:20px; border-top:1px solid #1E293B;">
      <div style="font-family:'JetBrains Mono', monospace; font-size:10px; font-weight:700; color:#64748B; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px; text-align:center;">
        DEMO ACCESO RÁPIDO
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center;">
        <button type="button" onclick="fillQuickLogin('antonio', '12345')" style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:6px 10px; font-size:11px; font-weight:600; color:#CBD5E1; cursor:pointer; transition:all 0.15s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          👤 Antonio (Master)
        </button>
        <button type="button" onclick="fillQuickLogin('giovanna', 'gio2026')" style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:6px 10px; font-size:11px; font-weight:600; color:#CBD5E1; cursor:pointer; transition:all 0.15s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          🔒 Giovanna (Bóveda Privada)
        </button>
        <button type="button" onclick="fillQuickLogin('ronan', 'ronan123')" style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:6px 10px; font-size:11px; font-weight:600; color:#CBD5E1; cursor:pointer; transition:all 0.15s;" onmouseover="this.style.borderColor='#6366F1'" onmouseout="this.style.borderColor='#334155'">
          🧪 Ronan (Sandbox)
        </button>
      </div>
    </div>

  </div>
</div>
<!-- END LOGIN MODAL -->"""

    content = re.sub(old_modal_regex, new_modal_html, content, count=1)

    # 2. Update JS helper functions for fillQuickLogin and submitCustomLogin (NO PROMPT POPUPS AT ALL)
    old_submit_regex = r'function submitCustomLogin\(targetUser\) \{[\s\S]*?window\.submitCustomLogin = submitCustomLogin;'
    
    new_js_code = """function fillQuickLogin(username, password) {
  const userInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  const alertDiv = document.getElementById('login-error-alert');
  if (alertDiv) alertDiv.style.display = 'none';
  if (userInput) userInput.value = username;
  if (pwdInput) pwdInput.value = password;
  submitCustomLogin();
}
window.fillQuickLogin = fillQuickLogin;

function quickLogin(username, pwd) {
  fillQuickLogin(username, pwd || '12345');
}
window.quickLogin = quickLogin;

function submitCustomLogin() {
  const userInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  const alertDiv = document.getElementById('login-error-alert');
  if (alertDiv) alertDiv.style.display = 'none';

  const userVal = (userInput ? userInput.value : '').trim().toLowerCase();
  const pwdVal = (pwdInput ? pwdInput.value : '').trim();

  if (!userVal) {
    if (alertDiv) {
      alertDiv.textContent = '⚠️ Ingresa tu usuario o email.';
      alertDiv.style.display = 'block';
    }
    return;
  }

  // --- ANTONIO MASTER ADMIN ---
  if (userVal === 'antonio' || userVal === 'antonio@radar.com' || userVal === 'master') {
    if (pwdVal !== '12345' && pwdVal !== 'admin') {
      if (alertDiv) {
        alertDiv.textContent = '❌ PIN o Contraseña incorrecta para Antonio Master.';
        alertDiv.style.display = 'block';
      }
      if (typeof showToast === 'function') showToast('❌ PIN o Contraseña incorrecta.', '🔒');
      return;
    }

    window.currentAuthUser = { id: 'antonio', name: '👤 Antonio (Master)', isMaster: true };
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';

    closeLoginModal();
    if (typeof showToast === 'function') showToast('⏳ Cargando Bóveda Master Antonio (2,953 contactos)...', '⏳');

    restoreLocalVault().then(restored => {
      if (!restored) {
        if (typeof window.fetchMasterSupabaseData === 'function') {
          window.fetchMasterSupabaseData().then(contacts => {
            if (contacts && contacts.length > 0) {
              S.contacts = contacts;
            } else {
              loadDemoData(false);
            }
            updateStatus();
            if (typeof renderDashboard === 'function') renderDashboard();
            if (typeof renderNetworkTable === 'function') renderNetworkTable();
            if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
          });
        } else {
          loadDemoData(false);
          updateStatus();
          if (typeof renderDashboard === 'function') renderDashboard();
          if (typeof renderNetworkTable === 'function') renderNetworkTable();
          if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
        }
      } else {
        updateStatus();
        if (typeof renderDashboard === 'function') renderDashboard();
        if (typeof renderNetworkTable === 'function') renderNetworkTable();
        if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada desde almacenamiento local.', '🔑');
      }
    });
  } 
  // --- GIOVANNA ISOLATED VAULT ---
  else if (userVal === 'giovanna' || userVal === 'giovanna@radar.com' || userVal === 'roanna') {
    if (pwdVal !== 'gio2026' && pwdVal !== '12345' && pwdVal !== 'giovanna') {
      if (alertDiv) {
        alertDiv.textContent = '❌ Contraseña incorrecta para Bóveda Giovanna.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    const isGio = userVal.includes('giovanna');
    const nameStr = isGio ? 'Giovanna' : 'Roanna';
    window.currentAuthUser = { id: userVal, name: `🔒 Bóveda ${nameStr} (Privada)`, isMaster: false };

    S.contacts = [];
    S.positions = [];
    S.messages = [];
    S.crmState = { discarded: [], whitelisted: [], deals: [] };
    S.loadedParts = { connections: false, messages: false, positions: false, profile: false };
    S.isDemoLoaded = false;

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `🔒 Bóveda ${nameStr} (Privada)`;

    updateStatus();
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    if (typeof navigate === 'function') navigate('upload');
    if (typeof showToast === 'function') showToast(`🔒 Bóveda Aislada de ${nameStr} (0 contactos). Lista para cargar tu ZIP.`, '🔒');
  } 
  // --- RONAN SANDBOX ---
  else if (userVal === 'ronan' || userVal === 'ronan@radar.com') {
    if (pwdVal !== 'ronan123' && pwdVal !== '12345' && pwdVal !== 'ronan') {
      if (alertDiv) {
        alertDiv.textContent = '❌ Contraseña incorrecta para Sandbox Ronan.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    window.currentAuthUser = { id: 'ronan', name: '🧪 Sandbox Ronan', isMaster: false, isSandbox: true };

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';

    if (typeof switchRonanAbMode === 'function') switchRonanAbMode('B');
  } 
  // --- OTHER INDIVIDUAL USERS ---
  else {
    if (!pwdVal) {
      if (alertDiv) {
        alertDiv.textContent = '⚠️ Ingresa una contraseña para tu bóveda.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    window.currentAuthUser = { id: userVal, name: `👤 Bóveda ${userVal}`, isMaster: false };

    S.contacts = [];
    S.positions = [];
    S.messages = [];

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `👤 Bóveda ${userVal}`;

    updateStatus();
    if (typeof navigate === 'function') navigate('upload');
    if (typeof showToast === 'function') showToast(`🔒 Bóveda de ${userVal} lista (0 contactos).`, '🔑');
  }
}
window.submitCustomLogin = submitCustomLogin;"""

    content = re.sub(old_submit_regex, new_js_code, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Minimalist login modal applied to {filepath}")

patch_login_modal(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_login_modal(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
