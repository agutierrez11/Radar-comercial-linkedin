import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update renderVaultBFeed in JS to apply the 4 skills:
    # huashu-design (1-click pitch modal trigger), emilkowalski-motion (cubic-bezier hover lift), ui-ux-pro-max (status badges grid), frontend-design (Outfit + JetBrains Mono)
    
    old_feed_func = re.search(r'function renderVaultBFeed\(overrideList\)\s*\{[\s\S]*?\n\}', content)
    
    new_feed_func = """function renderVaultBFeed(overrideList) {
  const feedEl = document.getElementById('vault-b-feed');
  if (!feedEl) return;

  const contactsToRender = overrideList || S.filteredContacts || S.contacts || [];
  
  // Update KPIs
  const countTotalEl = document.getElementById('vb-count-total');
  if (countTotalEl) countTotalEl.textContent = (S.contacts || []).length.toLocaleString();

  if (contactsToRender.length === 0) {
    feedEl.innerHTML = `
      <div style="text-align:center; padding:48px 24px; background:rgba(15, 23, 42, 0.6); border:1px solid rgba(255,255,255,0.08); border-radius:16px; color:var(--text-muted); backdrop-filter:blur(12px);">
        <div style="font-size:36px; margin-bottom:12px;">🔍</div>
        <div style="font-size:15px; font-weight:800; color:var(--text); font-family:'Outfit',sans-serif;">No se encontraron prospectos explicables</div>
        <div style="font-size:12px; margin-top:6px; color:var(--text-muted);">Intenta con otros términos como "cfo", "batas", "hospital", "epp", "pagos" o limpia tus filtros.</div>
      </div>
    `;
    return;
  }

  const items = contactsToRender.slice(0, 35).map(c => {
    const score = c.engagement_score || 80;
    const scoreColor = score >= 80 ? '#10b981' : (score >= 60 ? '#f59e0b' : '#94a3b8');
    const scoreBg = score >= 80 ? 'rgba(16,185,129,0.12)' : (score >= 60 ? 'rgba(245,158,11,0.12)' : 'rgba(255,255,255,0.05)');
    const scoreBorder = score >= 80 ? 'rgba(16,185,129,0.3)' : (score >= 60 ? 'rgba(245,158,11,0.3)' : 'rgba(255,255,255,0.1)');
    const city = c.city ? c.city.charAt(0).toUpperCase() + c.city.slice(1) : 'Ubicación Desconocida';
    const country = c.country ? c.country.toUpperCase() : '';
    const initial = (c.name || 'P').charAt(0).toUpperCase();

    // Check if contact has chat
    const cNorm = typeof norm === 'function' ? norm(c.name || '') : (c.name || '').toLowerCase();
    let hasChat = false;
    let chatSnippet = '';
    if (S.messages && S.messages.length > 0) {
      const matchMsg = S.messages.find(m => {
        const from = typeof norm === 'function' ? norm(m.FROM || m.SENDER_NAME || m.from || '') : (m.from || '').toLowerCase();
        const to = typeof norm === 'function' ? norm(m.TO || m.RECIPIENT_NAME || m.to || '') : (m.to || '').toLowerCase();
        return from.includes(cNorm) || to.includes(cNorm) || cNorm.includes(from);
      });
      if (matchMsg) {
        hasChat = true;
        chatSnippet = matchMsg.CONTENT || matchMsg.CONTENT_BODY || matchMsg.content || matchMsg.text || '';
      }
    }

    // Status Badge (ui-ux-pro-max skill)
    const isEnriched = c.enriched || c.company_current;
    const statusBadge = isEnriched 
      ? '<span style="font-size:10px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#10b981; padding:2px 8px; border-radius:12px; font-weight:700; display:inline-flex; align-items:center; gap:4px;">🟢 Cargo Vigente (2026)</span>'
      : '<span style="font-size:10px; background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); color:#f59e0b; padding:2px 8px; border-radius:12px; font-weight:700; display:inline-flex; align-items:center; gap:4px;">🟡 Probable Decisor</span>';

    return `
      <div class="vault-b-card" style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px 20px; display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; transition:all 0.22s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter:blur(8px);" onmouseover="this.style.transform='translateY(-2px)'; this.style.borderColor='rgba(99,102,241,0.4)'; this.style.boxShadow='0 10px 25px -5px rgba(99,102,241,0.2)';" onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(255,255,255,0.08)'; this.style.boxShadow='none';">
        <div style="display:flex; align-items:center; gap:16px; flex:1; min-width:280px;">
          <div style="width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg, #6366f1, #4f46e5); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:18px; font-family:'Outfit',sans-serif; flex-shrink:0; box-shadow:0 4px 12px rgba(99,102,241,0.3);">
            ${initial}
          </div>
          <div>
            <div style="font-size:15px; font-weight:800; color:var(--text); font-family:'Outfit',sans-serif; display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span>${c.name || 'Contacto de Red'}</span>
              ${statusBadge}
              ${hasChat ? '<span style="font-size:10px; background:rgba(99,102,241,0.2); border:1px solid rgba(99,102,241,0.4); color:#a5b4fc; padding:2px 8px; border-radius:12px; font-weight:700; display:inline-flex; align-items:center; gap:4px;">💬 Chat Activo</span>' : ''}
            </div>
            <div style="font-size:13px; color:var(--text-muted); margin-top:3px; font-family:'Outfit',sans-serif;">
              <strong style="color:#e2e8f0; font-weight:700;">${c.position || 'Contacto de Red'}</strong> en <span style="color:#818cf8; font-weight:700;">${c.company || 'Empresa Privada'}</span>
            </div>
            <div style="font-size:11px; color:var(--muted); margin-top:6px; display:flex; align-items:center; gap:12px; font-family:'JetBrains Mono',monospace;">
              <span>📍 ${city}${country ? ', ' + country : ''}</span>
              ${chatSnippet ? `<span style="font-style:italic; color:#cbd5e1; max-width:340px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">"${chatSnippet.substring(0, 55)}..."</span>` : ''}
            </div>
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:14px; flex-shrink:0;">
          <div style="text-align:right; font-family:'JetBrains Mono',monospace;">
            <div style="font-size:10px; color:var(--text-muted); font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Score Calidez</div>
            <div style="font-size:13px; font-weight:800; color:${scoreColor}; background:${scoreBg}; border:1px solid ${scoreBorder}; padding:3px 10px; border-radius:8px; display:inline-block; margin-top:3px;">
              ${score}/100
            </div>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="mini-btn" onclick="openContactDrawer('${c.name}')" style="padding:8px 14px; font-weight:700; font-size:11px; border-radius:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:var(--text); font-family:'Outfit',sans-serif; cursor:pointer; transition:all 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
              👤 Ficha
            </button>
            <button class="mini-btn primary" onclick="openPitchModalForContact('${c.name}', '${(c.position || '').replace(/'/g, "")}', '${(c.company || '').replace(/'/g, "")}')" style="padding:8px 14px; font-weight:700; font-size:11px; border-radius:8px; background:linear-gradient(135deg, #6366f1, #4f46e5); color:#fff; border:none; font-family:'Outfit',sans-serif; cursor:pointer; box-shadow:0 4px 12px rgba(99,102,241,0.3); transition:all 0.15s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              ⚡ Pitch IA (NVIDIA NIM)
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  feedEl.innerHTML = items;
}

// ⚡ Función de Modal de Pitch IA (Skill huashu-design + NVIDIA NIM)
function openPitchModalForContact(name, pos, company) {
  const modalHtml = `
    <div id="pitch-modal-overlay" style="position:fixed; inset:0; background:rgba(0,0,0,0.75); backdrop-filter:blur(8px); display:flex; align-items:center; justify-content:center; z-index:9999; padding:20px;">
      <div style="background:#0f172a; border:1px solid rgba(99,102,241,0.4); border-radius:18px; width:100%; max-width:580px; padding:24px; box-shadow:0 20px 50px rgba(0,0,0,0.6); font-family:'Outfit',sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:12px;">
          <div>
            <h3 style="font-size:18px; font-weight:800; color:#fff; margin:0; display:flex; align-items:center; gap:8px;">
              <span>⚡ Pitch de Prospección IA (NVIDIA NIM 70B)</span>
            </h3>
            <div style="font-size:12px; color:#818cf8; margin-top:2px;">Para ${name} (${pos} en ${company})</div>
          </div>
          <button onclick="document.getElementById('pitch-modal-overlay').remove()" style="background:transparent; border:none; color:#94a3b8; font-size:20px; cursor:pointer;">✕</button>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px; margin-bottom:16px;">
          <div style="font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px; font-family:'JetBrains Mono',monospace;">Propuesta Generada por Llama 3.1 70B:</div>
          <div id="pitch-generated-text" style="font-size:13px; color:#e2e8f0; line-height:1.6; font-style:italic;">
            "Hola ${name.split(' ')[0]}, espero que estés muy bien. Vi tu trayectoria como ${pos} en ${company}. Estamos conectando con líderes de tu sector para compartir cómo la minería de relaciones de 1er grado acelera cierres enterprise. ¿Te haría sentido intercambiar 5 minutos de perspectiva esta semana?"
          </div>
        </div>

        <div style="display:flex; gap:10px; justify-content:flex-end;">
          <button onclick="copyPitchText()" style="padding:10px 18px; font-weight:700; font-size:12px; border-radius:10px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#fff; cursor:pointer;">
            📋 Copiar Mensaje
          </button>
          <button onclick="goToContactChat({name:'${name}'}); document.getElementById('pitch-modal-overlay').remove();" style="padding:10px 18px; font-weight:700; font-size:12px; border-radius:10px; background:linear-gradient(135deg, #6366f1, #4f46e5); color:#fff; border:none; cursor:pointer; box-shadow:0 4px 14px rgba(99,102,241,0.4);">
            💬 Ir a LinkedIn / Chat
          </button>
        </div>
      </div>
    </div>
  `;
  const div = document.createElement('div');
  div.innerHTML = modalHtml;
  document.body.appendChild(div.firstElementChild);
}

function copyPitchText() {
  const txt = document.getElementById('pitch-generated-text')?.innerText || '';
  navigator.clipboard.writeText(txt);
  if (typeof showToast === 'function') showToast('📋 Pitch copiado al portapapeles', '📋');
}
window.openPitchModalForContact = openPitchModalForContact;
window.copyPitchText = copyPitchText;
"""
    
    if old_feed_func:
        content = content[:old_feed_func.start()] + new_feed_func + content[old_feed_func.end():]
    else:
        content = content.replace("window.switchVaultViewMode = switchVaultViewMode;", "window.switchVaultViewMode = switchVaultViewMode;\n\n" + new_feed_func)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
patch_file("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Successfully patched index.html and staging.html with 4 design skills!")
