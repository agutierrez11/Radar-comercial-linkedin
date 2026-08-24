import re

banner_html = """
<!-- 🔔 BOT RECORDATORIO DE ACTUALIZACIÓN MENSUAL DE BÓVEDA (30/60/90 DÍAS) -->
<div id="monthly-ingestion-reminder-banner" style="display:flex; align-items:center; justify-content:space-between; gap:16px; padding:10px 24px; background:linear-gradient(90deg, rgba(79,70,229,0.18), rgba(124,58,237,0.18)); border-bottom:1px solid rgba(99,102,241,0.35); font-family:'Outfit',sans-serif; backdrop-filter:blur(10px); z-index:990; font-size:12px; color:var(--text);">
  <div style="display:flex; align-items:center; gap:12px; flex:1;">
    <div style="font-size:20px; background:rgba(99,102,241,0.25); border:1px solid rgba(99,102,241,0.5); border-radius:8px; width:36px; height:36px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
      🔔
    </div>
    <div>
      <div style="display:flex; align-items:center; gap:8px;">
        <strong style="color:#ffffff; font-size:13px; font-weight:800;">Radar Comercial — Recordatorio de Minería Recurrente (30/60/90 Días)</strong>
        <span style="background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.4); color:#10b981; padding:1px 8px; border-radius:12px; font-size:10px; font-weight:700;">+30 Días de Actividad</span>
      </div>
      <div style="color:var(--text-muted); margin-top:2px; font-size:11px;">
        ¡Tu red sigue creciendo! Han pasado más de 30 días desde tu última sincronización. Si has agregado nuevos contactos o recibido invitaciones en el último mes, solicita tu ZIP en LinkedIn para incluirlos a tu Bóveda.
      </div>
    </div>
  </div>

  <div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
    <a href="https://www.linkedin.com/mypreferences/d/download-my-data" target="_blank" rel="noopener" class="mini-btn primary" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:8px; background:linear-gradient(135deg, #6366f1, #4f46e5); color:#fff; text-decoration:none; display:inline-flex; align-items:center; gap:6px; box-shadow:0 4px 12px rgba(99,102,241,0.3);">
      🚀 Solicitar ZIP en LinkedIn
    </a>
    <button onclick="openMonthlyIngestionModal()" class="mini-btn" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:8px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:var(--text); cursor:pointer;">
      📋 Guía Paso a Paso
    </button>
    <button onclick="dismissMonthlyReminder()" style="background:transparent; border:none; color:var(--muted); font-size:16px; cursor:pointer; padding:4px;" title="Cerrar recordatorio por 30 días">✕</button>
  </div>
</div>

<!-- MODAL GUÍA SOLICITUD LINKEDIN ZIP -->
<div id="monthly-ingestion-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); backdrop-filter:blur(8px); z-index:99999; align-items:center; justify-content:center; padding:20px; font-family:'Outfit',sans-serif;">
  <div style="background:#0f172a; border:1px solid rgba(99,102,241,0.4); border-radius:20px; max-width:540px; width:100%; padding:28px; box-shadow:0 25px 60px rgba(0,0,0,0.7); position:relative;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:14px;">
      <div style="display:flex; align-items:center; gap:10px;">
        <span style="font-size:24px;">📡</span>
        <div>
          <h3 style="font-size:17px; font-weight:800; color:#fff; margin:0;">Bot de Minería Recurrente Bóveda</h3>
          <div style="font-size:11px; color:#818cf8;">Actualización periódica de relaciones (30/60/90 días)</div>
        </div>
      </div>
      <button onclick="closeMonthlyIngestionModal()" style="background:transparent; border:none; color:#94a3b8; font-size:22px; cursor:pointer;">✕</button>
    </div>

    <div style="font-size:13px; color:#cbd5e1; line-height:1.6; margin-bottom:20px;">
      LinkedIn te permite descargar gratis una copia completa de tus conexiones y conversaciones en cualquier momento. Al sincronizar cada 30 días:
      <ul style="margin:10px 0 0 18px; padding:0; color:#94a3b8; font-size:12px;">
        <li style="margin-bottom:4px;"><strong style="color:#fff;">Integras a tus 100-300 contactos recién aceptados</strong> en tu pipeline warm.</li>
        <li style="margin-bottom:4px;"><strong style="color:#fff;">Mantenes al día tus scores de calidez de relación</strong> sin arriesgar tu cuenta.</li>
        <li style="margin-bottom:4px;"><strong style="color:#fff;">Zero-Knowledge:</strong> Tus datos nunca salen de tu cliente ni de tu bóveda local.</li>
      </ul>
    </div>

    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px; margin-bottom:24px;">
      <div style="font-size:11px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:10px; font-family:'JetBrains Mono',monospace;">Paso a Paso Rápido (2 minutos):</div>
      <div style="display:flex; flex-direction:column; gap:10px; font-size:12px; color:#e2e8f0;">
        <div style="display:flex; gap:10px; align-items:flex-start;">
          <span style="background:#4f46e5; color:#fff; font-weight:800; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:11px; flex-shrink:0;">1</span>
          <div>Haz clic en <strong>"Solicitar mi ZIP en LinkedIn"</strong> (te llevará a Configuración de Datos).</div>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
          <span style="background:#4f46e5; color:#fff; font-weight:800; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:11px; flex-shrink:0;">2</span>
          <div>Selecciona las casillas <strong>"Conexiones"</strong> y <strong>"Mensajes"</strong> y presiona <em>Solicitar archivo</em>.</div>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
          <span style="background:#4f46e5; color:#fff; font-weight:800; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:11px; flex-shrink:0;">3</span>
          <div>En 10 minutos descarga tu ZIP y arrástralo en el panel de <strong>Cargar Datos</strong> de Radar Comercial.</div>
        </div>
      </div>
    </div>

    <div style="display:flex; gap:12px; justify-content:flex-end;">
      <button onclick="markVaultUpdatedToday()" style="padding:10px 16px; font-weight:700; font-size:12px; border-radius:10px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#fff; cursor:pointer;">
        ✅ Marcar Bóveda Actualizada Hoy
      </button>
      <a href="https://www.linkedin.com/mypreferences/d/download-my-data" target="_blank" rel="noopener" onclick="closeMonthlyIngestionModal();" style="padding:10px 18px; font-weight:700; font-size:12px; border-radius:10px; background:linear-gradient(135deg, #6366f1, #4f46e5); color:#fff; text-decoration:none; display:inline-flex; align-items:center; gap:6px; box-shadow:0 4px 14px rgba(99,102,241,0.4);">
        🚀 Solicitar ZIP en LinkedIn
      </a>
    </div>
  </div>
</div>

<script>
function openMonthlyIngestionModal() {
  const m = document.getElementById('monthly-ingestion-modal');
  if (m) m.style.display = 'flex';
}
function closeMonthlyIngestionModal() {
  const m = document.getElementById('monthly-ingestion-modal');
  if (m) m.style.display = 'none';
}
function dismissMonthlyReminder() {
  const b = document.getElementById('monthly-ingestion-reminder-banner');
  if (b) b.style.display = 'none';
  localStorage.setItem('rc_last_reminder_dismiss', Date.now().toString());
  if (typeof showToast === 'function') showToast('ℹ️ Recordatorio pausado por 30 días.', 'ℹ️');
}
function markVaultUpdatedToday() {
  localStorage.setItem('rc_last_csv_ingestion', Date.now().toString());
  dismissMonthlyReminder();
  closeMonthlyIngestionModal();
  if (typeof showToast === 'function') showToast('✅ Bóveda marcada como actualizada hoy.', '✅');
}

document.addEventListener('DOMContentLoaded', function() {
  const lastDismiss = localStorage.getItem('rc_last_reminder_dismiss');
  const lastIngest = localStorage.getItem('rc_last_csv_ingestion');
  const now = Date.now();
  const thirtyDays = 30 * 24 * 60 * 60 * 1000;

  // Show banner by default if 30 days passed since dismiss or ingest
  const banner = document.getElementById('monthly-ingestion-reminder-banner');
  if (banner) {
    if (lastDismiss && (now - parseInt(lastDismiss)) < thirtyDays) {
      banner.style.display = 'none';
    } else {
      banner.style.display = 'flex';
    }
  }
});
</script>
"""

def add_reminder(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'monthly-ingestion-reminder-banner' in content:
        print(f"Banner already present in {filepath}")
        return

    # Insert banner right after </header>
    target = "</header>"
    if target in content:
        content = content.replace(target, target + "\n" + banner_html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Monthly ingestion reminder bot added to {filepath}")

add_reminder(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
add_reminder(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
