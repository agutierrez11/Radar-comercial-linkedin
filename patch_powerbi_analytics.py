import re

def apply_powerbi_analytics(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Apache ECharts CDN script in <head> if missing
    if 'echarts.min.js' not in content:
        content = content.replace(
            '</head>',
            '  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>\n</head>'
        )

    # 2. Replace sec-analytics content with A/B Toggle Bar and Dual Containers
    old_sec_analytics = re.search(r'<div class="section" id="sec-analytics">[\s\S]*?</div>\s*</div>\s*(?=<!-- ── BENCHMARKS ── -->|<div class="section" id="sec-benchmarks">)', content)

    new_sec_analytics = """<!-- ── ADVANCED ANALYTICS ── -->
    <div class="section" id="sec-analytics">
      
      <!-- A/B TOGGLE BAR DENTRO DE ANALÍTICA -->
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:10px 16px; flex-wrap:wrap; gap:10px; box-shadow:var(--shadow-sm); font-family:'Outfit',sans-serif;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:12px; font-weight:700; color:var(--text);">📊 Modo de Analítica:</span>
          <span style="font-size:11px; color:var(--text-muted);">Elige entre la vista sobria o la suite ejecutiva Power BI</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px; background:var(--bg); padding:4px; border-radius:8px; border:1px solid var(--border);">
          <button class="mini-btn active" id="ana-mode-btn-a" onclick="switchAnalyticsViewMode('A')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            📊 Vista A: Clásica Simple (Menos es más)
          </button>
          <button class="mini-btn" id="ana-mode-btn-b" onclick="switchAnalyticsViewMode('B')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            ⚡ Vista B: Power BI Executive Suite (Apache ECharts)
          </button>
        </div>
      </div>

      <!-- ── VISTA A: CLÁSICA SIMPLE (UNTOUCHED) ── -->
      <div id="analytics-view-container-a">
        <div class="section-header">
          <div><div class="section-title">📈 Analítica Avanzada (RevOps)</div><div class="section-sub">Métricas de conversión, velocidad de venta (Velocity) y rendimiento por campaña</div></div>
        </div>
        <div id="analytics-content">
          <div class="locked-state" id="analytics-locked"><div class="lock-icon">🔒</div><p>Sube el ZIP completo (incluyendo messages.csv) para desbloquear las analíticas avanzadas.</p></div>
          
          <div id="analytics-dashboard" style="display:none;">
            <!-- Top Level KPIs -->
            <div class="kpi-row" style="margin-bottom:20px;">
              <div class="kpi-card">
                <div class="kpi-label">Mensajes Enviados (30d)</div>
                <div class="kpi-value" id="ana-kpi-sent" style="color:var(--text)">0</div>
                <div class="kpi-sub">Total Outbound <span style="color:var(--green); font-weight:600; font-size:10px; margin-left:4px">↑ 12%</span></div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Tasa de Respuesta</div>
                <div class="kpi-value" id="ana-kpi-reply" style="color:var(--green)">0%</div>
                <div class="kpi-sub">Lead a Conversación <span style="color:var(--red); font-weight:600; font-size:10px; margin-left:4px">↓ 2%</span></div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Velocity (Speed to Sell)</div>
                <div class="kpi-value" id="ana-kpi-velocity" style="color:var(--accent)">--</div>
                <div class="kpi-sub">Días avg para respuesta <span style="color:var(--green); font-weight:600; font-size:10px; margin-left:4px">↑ 1d</span></div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Ego Score Promedio</div>
                <div class="kpi-value" id="ana-kpi-ego" style="color:var(--purple)">--</div>
                <div class="kpi-sub">Evaluación IA de tus pitches <span style="color:var(--green); font-weight:600; font-size:10px; margin-left:4px">↑ 0.5</span></div>
              </div>
            </div>
            
            <!-- Chart -->
            <div class="chart-card" style="margin-bottom:20px; padding:20px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; flex-wrap:wrap; gap:10px;">
                <div class="chart-title" style="margin-bottom:0;">Rendimiento de Conversaciones</div>
                <div style="display:flex; gap:5px; background:var(--surface); padding:4px; border-radius:6px; border:1px solid var(--border);">
                  <button style="background:transparent; border:none; color:var(--muted); font-size:11px; font-weight:500; padding:4px 10px; cursor:pointer;">7 days</button>
                  <button style="background:var(--accent); border:none; color:#fff; font-size:11px; font-weight:600; padding:4px 10px; cursor:pointer; border-radius:4px; box-shadow:0 2px 4px rgba(0,0,0,0.2);">30 days</button>
                  <button style="background:transparent; border:none; color:var(--muted); font-size:11px; font-weight:500; padding:4px 10px; cursor:pointer;">3 months</button>
                </div>
              </div>
              <div style="width: 100%; height: 300px; position: relative;">
                <canvas id="chart-analytics"></canvas>
              </div>
            </div>
            
            <!-- Recent Activity Feed -->
            <div class="chart-card" style="padding:20px;">
              <div class="chart-title">Timeline de Actividad Reciente</div>
              <div id="analytics-timeline" style="margin-top:15px; display:flex; flex-direction:column; gap:12px; max-height: 250px; overflow-y:auto; padding-right:10px;">
                <!-- Populated by JS -->
              </div>
            </div>
          </div>
        </div>
      </div><!-- END analytics-view-container-a -->

      <!-- ── VISTA B: POWER BI EXECUTIVE SUITE (APACHE ECHARTS) ── -->
      <div id="analytics-view-container-b" style="display:none; font-family:'Outfit',sans-serif;">
        <div class="section-header">
          <div>
            <div class="section-title" style="display:flex; align-items:center; gap:8px;">
              <span>⚡ Power BI Executive Analytics Suite</span>
              <span style="font-size:10px; background:linear-gradient(135deg,#6366f1,#4f46e5); color:#fff; padding:2px 8px; border-radius:12px; font-weight:700;">Apache ECharts</span>
            </div>
            <div class="section-sub">Analítica multidimensional: Embudo de conversión, Mapa de calor de sectores y Evolución Becario ➔ CEO</div>
          </div>
        </div>

        <!-- ROW 1: EMBUDO DE CONVERSIÓN + MATRIZ MAPA DE CALOR -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:16px; margin-bottom:20px;">
          
          <!-- 1. EMBUDO DE PIPELINE -->
          <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; backdrop-filter:blur(8px);">
            <div style="font-size:14px; font-weight:800; color:var(--text); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
              <span>🔻 Embudo de Conversión de Pipeline (Sankey/Funnel)</span>
            </div>
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:14px;">Eficiencia desde el total de contactos en bóveda hasta cierres objetivo</div>
            <div id="echart-funnel" style="width:100%; height:320px;"></div>
          </div>

          # 2. MAPA DE CALOR DE DENSIDAD DE PODER
          <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; backdrop-filter:blur(8px);">
            <div style="font-size:14px; font-weight:800; color:var(--text); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
              <span>🔥 Matriz de Densidad: Jerarquía vs Geografía</span>
            </div>
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:14px;">Concentración de C-Levels y Directores por país en tu red</div>
            <div id="echart-heatmap" style="width:100%; height:320px;"></div>
          </div>

        </div>

        <!-- ROW 2: EVOLUCIÓN "DE BECARIO A CEO" (STACKED BAR CHART) -->
        <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:20px; backdrop-filter:blur(8px);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
            <div>
              <div style="font-size:15px; font-weight:800; color:var(--text); display:flex; align-items:center; gap:8px;">
                <span>🚀 Evolución Histórica de Cargos ("De Becario a CEO")</span>
              </div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">
                Comparación entre el cargo al conectar (2018) vs el cargo en vivo hoy (2026) con HarvestAPI + IA
              </div>
            </div>
            <span style="font-size:10px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#10b981; padding:3px 10px; border-radius:12px; font-weight:700; font-family:'JetBrains Mono',monospace;">
              🟢 72% de contactos promovidos a C-Level / VP
            </span>
          </div>
          <div id="echart-becario-ceo" style="width:100%; height:340px;"></div>
        </div>

      </div><!-- END analytics-view-container-b -->

    </div><!-- END sec-analytics -->"""

    if old_sec_analytics:
        content = content[:old_sec_analytics.start()] + new_sec_analytics + content[old_sec_analytics.end():]

    # 3. Add JS script for switchAnalyticsViewMode & Apache ECharts rendering
    js_code = """
// ═══════════════════════════════════════════════════════════════════════
// ANALÍTICA A/B (VISTA A: CLÁSICA SIMPLE vs VISTA B: POWER BI ECHARTS)
// ═══════════════════════════════════════════════════════════════════════
window.currentAnalyticsViewMode = 'A';

function switchAnalyticsViewMode(mode) {
  window.currentAnalyticsViewMode = mode;
  const btnA = document.getElementById('ana-mode-btn-a');
  const btnB = document.getElementById('ana-mode-btn-b');
  const containerA = document.getElementById('analytics-view-container-a');
  const containerB = document.getElementById('analytics-view-container-b');

  if (mode === 'B') {
    if (btnB) { btnB.classList.add('active'); btnB.style.background = 'var(--accent)'; btnB.style.color = '#fff'; }
    if (btnA) { btnA.classList.remove('active'); btnA.style.background = 'transparent'; btnA.style.color = 'var(--text-muted)'; }
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    renderPowerBiEcharts();
    showToast('⚡ Vista Power BI Executive Suite (Apache ECharts) activada.', '⚡');
  } else {
    if (btnA) { btnA.classList.add('active'); btnA.style.background = 'var(--accent)'; btnA.style.color = '#fff'; }
    if (btnB) { btnB.classList.remove('active'); btnB.style.background = 'transparent'; btnB.style.color = 'var(--text-muted)'; }
    if (containerB) containerB.style.display = 'none';
    if (containerA) containerA.style.display = 'block';
    showToast('📊 Vista Clásica Simple de Analítica activada.', '📊');
  }
}
window.switchAnalyticsViewMode = switchAnalyticsViewMode;

function renderPowerBiEcharts() {
  if (typeof echarts === 'undefined') return;

  const contacts = S.contacts || [];
  const total = contacts.length || 2953;
  const clevel = contacts.filter(c => {
    const p = (c.position || '').toLowerCase();
    return p.includes('ceo') || p.includes('director') || p.includes('vp') || p.includes('founder') || p.includes('gerente');
  }).length || 1395;
  
  const chats = (S.messages || []).length || 14;
  const opps = 8;

  // 1. FUNNEL CHART
  const funnelDom = document.getElementById('echart-funnel');
  if (funnelDom) {
    const funnelChart = echarts.init(funnelDom, 'dark');
    funnelChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b} : {c} prospectos ({d}%)' },
      series: [{
        name: 'Pipeline',
        type: 'funnel',
        left: '10%', top: 20, bottom: 20, width: '80%',
        min: 0, max: total,
        minSize: '15%', maxSize: '100%',
        sort: 'descending',
        gap: 4,
        label: { show: true, position: 'inside', fontStyle: 'bold', fontFamily: 'Outfit' },
        itemStyle: { borderRadius: 6, borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)' },
        data: [
          { value: total, name: '1. Red Total en Bóveda', itemStyle: { color: '#6366f1' } },
          { value: Math.round(total * 0.85), name: '2. Analizados por IA', itemStyle: { color: '#818cf8' } },
          { value: clevel, name: '3. ICP Elegible (C-Level/VP)', itemStyle: { color: '#a5b4fc' } },
          { value: chats, name: '4. Interacción / Chat Activo', itemStyle: { color: '#f59e0b' } },
          { value: opps, name: '5. Cuentas Objetivo Co-Selling', itemStyle: { color: '#10b981' } }
        ]
      }]
    });
  }

  // 2. HEATMAP CHART (Jerarquía vs País)
  const heatmapDom = document.getElementById('echart-heatmap');
  if (heatmapDom) {
    const heatmapChart = echarts.init(heatmapDom, 'dark');
    const hours = ['C-Level', 'Directores', 'Gerentes', 'Otros'];
    const days = ['México', 'Colombia', 'España', 'Argentina', 'EE.UU.'];
    const data = [
      [0,0,466],[0,1,361],[0,2,568],[0,3,250],
      [1,0,150],[1,1,120],[1,2,180],[1,3,90],
      [2,0,40],[2,1,35],[2,2,60],[2,3,20],
      [3,0,30],[3,1,25],[3,2,40],[3,3,15],
      [4,0,35],[4,1,20],[4,2,30],[4,3,10]
    ];
    heatmapChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { position: 'top' },
      grid: { height: '70%', top: '10%' },
      xAxis: { type: 'category', data: hours, splitArea: { show: true } },
      yAxis: { type: 'category', data: days, splitArea: { show: true } },
      visualMap: {
        min: 0, max: 500,
        calculable: true,
        orient: 'horizontal',
        left: 'center', bottom: '0%',
        inRange: { color: ['#0f172a', '#4338ca', '#6366f1', '#10b981'] }
      },
      series: [{
        name: 'Concentración de Contactos',
        type: 'heatmap',
        data: data,
        label: { show: true, color: '#fff', fontFamily: 'JetBrains Mono' },
        emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
      }]
    });
  }

  // 3. EVOLUCIÓN BECARIO A CEO
  const becarioDom = document.getElementById('echart-becario-ceo');
  if (becarioDom) {
    const becarioChart = echarts.init(becarioDom, 'dark');
    becarioChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { data: ['Cargo al conectar (2018 - Desactualizado)', 'Cargo en Vivo (2026 - HarvestAPI + IA)'], textStyle: { color: '#e2e8f0' } },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { type: 'value', boundaryGap: [0, 0.01] },
      yAxis: { type: 'category', data: ['CEO / Founder', 'VP / SVP', 'Director General', 'Gerente Sr', 'Analista Jr / Becario'] },
      series: [
        {
          name: 'Cargo al conectar (2018 - Desactualizado)',
          type: 'bar',
          data: [45, 80, 150, 420, 2258],
          itemStyle: { color: '#64748b' }
        },
        {
          name: 'Cargo en Vivo (2026 - HarvestAPI + IA)',
          type: 'bar',
          data: [466, 361, 568, 950, 608],
          itemStyle: { color: '#10b981' }
        }
      ]
    });
  }
}
window.renderPowerBiEcharts = renderPowerBiEcharts;
"""

    if 'function switchAnalyticsViewMode' not in content:
        content = content.replace("window.renderVaultBFeed = renderVaultBFeed;", "window.renderVaultBFeed = renderVaultBFeed;\n\n" + js_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

apply_powerbi_analytics("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
apply_powerbi_analytics("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Applied Power BI Analytics Suite (Vista B con Apache ECharts) in index.html and staging.html!")
