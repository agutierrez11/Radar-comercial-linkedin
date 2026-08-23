"""
apply_vault_ab_view.py
Adds A/B Toggle Bar on 'sec-network' ("Mi Bóveda") allowing users to switch between:
- Vista A: Clásica (Dashboard BI, Gráficos y Mapa GIS actual)
- Vista B: B2B Pro Rediseño (Inspirado en Attio & Linear: Búsqueda Protagonista, 3 KPIs nítidos, Feed Explicable & Panel Lateral Drawer)
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DIR = os.path.dirname(os.path.abspath(__file__))

def patch_vault_ab(file_name):
    file_path = os.path.join(DIR, file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. Toggle Bar HTML
    toggle_bar_html = """
      <!-- ── A/B TOGGLE BAR DE NAVEGACIÓN EN BÓVEDA ── -->
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:10px 16px; flex-wrap:wrap; gap:10px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:12px; font-weight:700; color:var(--text); font-family:'Outfit',sans-serif;">🎛️ Experiencia de Bóveda:</span>
          <span style="font-size:11px; color:var(--text-muted);">Selecciona la interfaz preferida para tu equipo</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px; background:var(--bg); padding:4px; border-radius:8px; border:1px solid var(--border);">
          <button class="mini-btn active" id="vault-mode-btn-a" onclick="switchVaultViewMode('A')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            📊 Vista A: Clásica (Dashboard & Mapa GIS)
          </button>
          <button class="mini-btn" id="vault-mode-btn-b" onclick="switchVaultViewMode('B')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            ✨ Vista B: Bóveda B2B Pro (Attio / Linear)
          </button>
        </div>
      </div>
"""

    # 2. Vista B HTML Container
    vista_b_html = """
      <!-- ── VISTA B: REDISEÑO B2B PRO (ATTIO / LINEAR SPEC) ── -->
      <div id="vault-view-container-b" style="display:none; font-family:'Outfit',sans-serif;">
        
        <!-- BÚSQUEDA HÉROE PROTAGONISTA -->
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:24px 20px; margin-bottom:20px; box-shadow:var(--shadow-sm);">
          <div style="text-align:center; max-width:640px; margin:0 auto 16px auto;">
            <h2 style="font-size:20px; font-weight:800; color:var(--text); margin-bottom:6px;">Explora tu Bóveda Privada de Inteligencia</h2>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.5;">Busca por nombre, cargo, empresa, palabras clave o temas de conversación en tu red.</p>
          </div>

          <div style="position:relative; max-width:720px; margin:0 auto 14px auto;">
            <input type="text" id="vault-b-search-input" class="filter-input" placeholder="🔍 Ejemplo: 'batas', 'cfo fintech', 'epp', 'pagos', 'compras hospital'..." style="width:100%; padding:14px 44px 14px 16px; font-size:14px; border-radius:10px; background:var(--bg); border:1px solid var(--accent); color:var(--text); outline:none; box-shadow:0 0 0 3px rgba(79,70,229,0.15);" onkeyup="handleVaultBSearch(event)">
            <button onclick="triggerVaultBSearch()" style="position:absolute; right:10px; top:50%; transform:translateY(-50%); background:var(--accent); color:white; border:none; border-radius:6px; padding:6px 14px; font-weight:700; font-size:12px; cursor:pointer;">Buscar</button>
          </div>

          <!-- CHIPS DE BÚSQUEDA RÁPIDA -->
          <div style="display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;">
            <span style="font-size:11px; color:var(--text-muted); font-weight:600;">Sugerencias:</span>
            <button class="mini-btn" onclick="quickSearchVaultB('hospital')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🩺 Compras Hospitales</button>
            <button class="mini-btn" onclick="quickSearchVaultB('pagos')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">💳 Payments / Fintech</button>
            <button class="mini-btn" onclick="quickSearchVaultB('epp')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🛡️ Equipos EPP</button>
            <button class="mini-btn" onclick="quickSearchVaultB('cfo')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🎯 Decisores C-Level</button>
          </div>
        </div>

        <!-- 3 KPIS COMERCIALES NÍTIDOS -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:20px;">
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(99,102,241,0.12); color:var(--accent); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">🎯</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Perfiles de Alto ICP</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-icp">296</div>
            </div>
          </div>
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(16,185,129,0.12); color:var(--green); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">💬</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Chats a Re-contactar</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-chats">14</div>
            </div>
          </div>
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(245,158,11,0.12); color:var(--amber); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">🚀</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Cuentas Objetivo Co-Selling</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-opps">8</div>
            </div>
          </div>
        </div>

        <!-- SEGMENTACIÓN & FILTROS SOBRIOS -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button class="mini-btn active" id="vb-filter-all" onclick="filterVaultB('all')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">Todos (<span id="vb-count-total">2,953</span>)</button>
            <button class="mini-btn" id="vb-filter-clevel" onclick="filterVaultB('clevel')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">🎯 C-Level & Directores</button>
            <button class="mini-btn" id="vb-filter-chats" onclick="filterVaultB('chats')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">💬 Con Historial de Chat</button>
            <button class="mini-btn" id="vb-filter-mexico" onclick="filterVaultB('mexico')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">🇲🇽 México</button>
          </div>
          <div style="font-size:12px; color:var(--text-muted);" id="vb-results-counter">
            Mostrando prospectos explicables de tu red
          </div>
        </div>

        <!-- FEED DE RESULTADOS EXPLICABLES ESTILO ATTIO/LINEAR -->
        <div id="vault-b-feed" style="display:flex; flex-direction:column; gap:10px;">
          <!-- Injected dynamically by renderVaultBFeed() -->
        </div>

      </div>
"""

    # 3. JS Functions for Vault A/B Mode Switching and Feed Rendering
    vault_ab_js = """
// ═══════════════════════════════════════════════════════════════════════
// VISTA A/B DE BÓVEDA (VISTA A: CLÁSICA BI vs VISTA B: B2B PRO ATTIO/LINEAR)
// ═══════════════════════════════════════════════════════════════════════
window.currentVaultViewMode = 'A';

function switchVaultViewMode(mode) {
  window.currentVaultViewMode = mode;
  const btnA = document.getElementById('vault-mode-btn-a');
  const btnB = document.getElementById('vault-mode-btn-b');
  const containerA = document.getElementById('vault-view-container-a');
  const containerB = document.getElementById('vault-view-container-b');

  if (mode === 'B') {
    if (btnB) { btnB.classList.add('active'); btnB.style.background = 'var(--accent)'; btnB.style.color = '#fff'; }
    if (btnA) { btnA.classList.remove('active'); btnA.style.background = 'transparent'; btnA.style.color = 'var(--text-muted)'; }
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    renderVaultBFeed();
    showToast('✨ Vista B2B Pro (Estilo Attio / Linear) activada.', '✨');
  } else {
    if (btnA) { btnA.classList.add('active'); btnA.style.background = 'var(--accent)'; btnA.style.color = '#fff'; }
    if (btnB) { btnB.classList.remove('active'); btnB.style.background = 'transparent'; btnB.style.color = 'var(--text-muted)'; }
    if (containerB) containerB.style.display = 'none';
    if (containerA) containerA.style.display = 'block';
    showToast('📊 Vista Clásica (Dashboard BI & Mapa GIS) activada.', '📊');
  }
}
window.switchVaultViewMode = switchVaultViewMode;

function renderVaultBFeed(overrideList) {
  const feedEl = document.getElementById('vault-b-feed');
  if (!feedEl) return;

  const contactsToRender = overrideList || S.filteredContacts || S.contacts || [];
  
  // Update KPIs
  const countTotalEl = document.getElementById('vb-count-total');
  if (countTotalEl) countTotalEl.textContent = (S.contacts || []).length.toLocaleString();

  if (contactsToRender.length === 0) {
    feedEl.innerHTML = `
      <div style="text-align:center; padding:40px 20px; background:var(--surface); border:1px solid var(--border); border-radius:12px; color:var(--text-muted);">
        <div style="font-size:32px; margin-bottom:8px;">🔍</div>
        <div style="font-size:14px; font-weight:700; color:var(--text);">No se encontraron prospectos</div>
        <div style="font-size:12px; margin-top:4px;">Intenta con otros términos como "cfo", "batas", "hospital", "epp" o limpia tus filtros.</div>
      </div>
    `;
    return;
  }

  const items = contactsToRender.slice(0, 30).map(c => {
    const score = c.engagement_score || 80;
    const scoreColor = score >= 80 ? 'var(--green)' : (score >= 60 ? 'var(--amber)' : 'var(--text-muted)');
    const scoreBg = score >= 80 ? 'rgba(16,185,129,0.1)' : (score >= 60 ? 'rgba(245,158,11,0.1)' : 'rgba(255,255,255,0.05)');
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

    return `
      <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; transition:all 0.2s; box-shadow:var(--shadow-sm);">
        <div style="display:flex; align-items:center; gap:14px; flex:1; min-width:260px;">
          <div style="width:44px; height:44px; border-radius:10px; background:linear-gradient(135deg, var(--accent), #4338ca); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:16px; flex-shrink:0;">
            ${initial}
          </div>
          <div>
            <div style="font-size:14px; font-weight:700; color:var(--text); display:flex; align-items:center; gap:8px;">
              <span>${c.name || 'Contacto de Red'}</span>
              ${hasChat ? '<span style="font-size:9px; background:rgba(99,102,241,0.15); color:var(--accent); padding:2px 6px; border-radius:4px; font-weight:700;">💬 Chat Activo</span>' : ''}
            </div>
            <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
              <strong>${c.position || 'Contacto de Red'}</strong> • <span style="color:var(--text);">${c.company || 'Empresa Privada'}</span>
            </div>
            <div style="font-size:11px; color:var(--muted); margin-top:4px; display:flex; align-items:center; gap:10px;">
              <span>📍 ${city}${country ? ', ' + country : ''}</span>
              ${chatSnippet ? `<span style="font-style:italic; max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">"${chatSnippet.substring(0, 50)}..."</span>` : ''}
            </div>
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:12px; flex-shrink:0;">
          <div style="text-align:right;">
            <div style="font-size:10px; color:var(--text-muted); font-weight:600; text-transform:uppercase;">Score de Calidez</div>
            <div style="font-size:13px; font-weight:800; color:${scoreColor}; background:${scoreBg}; padding:2px 8px; border-radius:6px; display:inline-block; margin-top:2px;">
              ${score}/100
            </div>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="mini-btn" onclick="openContactDrawer('${c.name}')" style="padding:8px 12px; font-weight:700; font-size:11px; border-radius:8px; background:var(--bg); border:1px solid var(--border); color:var(--text);">
              👤 Ver Ficha
            </button>
            <button class="mini-btn primary" onclick="goToContactChat({name:'${c.name}'})" style="padding:8px 12px; font-weight:700; font-size:11px; border-radius:8px;">
              💬 Ir al Chat
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  feedEl.innerHTML = items;
}
window.renderVaultBFeed = renderVaultBFeed;

function handleVaultBSearch(e) {
  if (e.key === 'Enter') triggerVaultBSearch();
}
window.handleVaultBSearch = handleVaultBSearch;

function triggerVaultBSearch() {
  const input = document.getElementById('vault-b-search-input');
  if (!input) return;
  const query = (input.value || '').trim().toLowerCase();
  if (!query) {
    renderVaultBFeed();
    return;
  }

  const filtered = (S.contacts || []).filter(c => {
    const name = (c.name || '').toLowerCase();
    const pos = (c.position || '').toLowerCase();
    const comp = (c.company || '').toLowerCase();
    const city = (c.city || '').toLowerCase();
    return name.includes(query) || pos.includes(query) || comp.includes(query) || city.includes(query);
  });

  renderVaultBFeed(filtered);
  showToast(`🔍 ${filtered.length} prospectos encontrados para "${query}".`, '🔍');
}
window.triggerVaultBSearch = triggerVaultBSearch;

function quickSearchVaultB(term) {
  const input = document.getElementById('vault-b-search-input');
  if (input) {
    input.value = term;
    triggerVaultBSearch();
  }
}
window.quickSearchVaultB = quickSearchVaultB;

function filterVaultB(category) {
  ['all', 'clevel', 'chats', 'mexico'].forEach(cat => {
    const btn = document.getElementById(`vb-filter-${cat}`);
    if (btn) btn.classList.remove('active');
  });
  const activeBtn = document.getElementById(`vb-filter-${category}`);
  if (activeBtn) activeBtn.classList.add('active');

  let filtered = S.contacts || [];
  if (category === 'clevel') {
    filtered = filtered.filter(c => {
      const p = (c.position || '').toLowerCase();
      return p.includes('ceo') || p.includes('director') || p.includes('founder') || p.includes('vp') || p.includes('gerente');
    });
  } else if (category === 'chats') {
    filtered = filtered.filter(c => {
      const cNorm = typeof norm === 'function' ? norm(c.name || '') : (c.name || '').toLowerCase();
      return (S.messages || []).some(m => {
        const from = (m.FROM || m.SENDER_NAME || m.from || '').toLowerCase();
        return from.includes(cNorm);
      });
    });
  } else if (category === 'mexico') {
    filtered = filtered.filter(c => (c.country || '').toLowerCase().includes('mexico') || (c.city || '').toLowerCase().includes('mexico') || (c.city || '').toLowerCase().includes('cdmx'));
  }

  renderVaultBFeed(filtered);
}
window.filterVaultB = filterVaultB;

function openContactDrawer(contactName) {
  const c = (S.contacts || []).find(x => x.name === contactName);
  if (!c) return;
  alert(`👤 Ficha Comercial de Prospecto:\\n\\nNombre: ${c.name}\\nCargo: ${c.position || 'N/A'}\\nEmpresa: ${c.company || 'N/A'}\\nUbicación: ${c.city || ''}, ${c.country || ''}\\nScore de Calidez: ${c.engagement_score || 80}/100\\n\\nRelación detectada en tu Bóveda Privada.`);
}
window.openContactDrawer = openContactDrawer;
"""

    # Wrap existing sec-network contents inside container A
    sec_network_start = '<div class="section" id="sec-network">'
    if sec_network_start in html and 'vault-view-container-a' not in html:
        # Wrap everything between sec-network header and section end in container A
        html = html.replace(
            sec_network_start,
            sec_network_start + "\n" + toggle_bar_html + "\n" + '      <div id="vault-view-container-a">'
        )
        # Close container A before sec-network closing div
        html = html.replace(
            '<!-- ── PROFILE ── -->',
            '      </div><!-- END vault-view-container-a -->\n\n' + vista_b_html + '\n    </div><!-- END sec-network -->\n\n    <!-- ── PROFILE ── -->'
        )

    if "VISTA A/B DE BÓVEDA" not in html:
        html = html.replace("</script>\n</body>", vault_ab_js + "\n</script>\n</body>")

    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html)
    print(f"VAULT_AB_VIEW_APPLIED: {file_name}")

patch_vault_ab("staging.html")
patch_vault_ab("index.html")
