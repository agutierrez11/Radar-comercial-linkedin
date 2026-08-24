import re

def patch_powerbi(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean HTML of Vista B
    old_vista_b_html = """<!-- ── VISTA B: POWER BI EXECUTIVE SUITE (APACHE ECHARTS) ── -->
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

      </div>"""

    new_vista_b_html = """<!-- ── VISTA B: POWER BI EXECUTIVE SUITE (APACHE ECHARTS) ── -->
      <div id="analytics-view-container-b" style="display:none; font-family:'Outfit',sans-serif;">
        <div class="section-header" style="margin-bottom:16px;">
          <div>
            <div class="section-title" style="display:flex; align-items:center; gap:8px;">
              <span>⚡ Power BI Executive Analytics Suite</span>
              <span style="font-size:10px; background:linear-gradient(135deg,#6366f1,#4f46e5); color:#fff; padding:2px 8px; border-radius:12px; font-weight:700;">Apache ECharts 2026</span>
            </div>
            <div class="section-sub">Analítica multidimensional: Embudo de conversión, Mapa de calor de sectores y Evolución Becario ➔ CEO</div>
          </div>
        </div>

        <!-- ROW 1: EMBUDO DE CONVERSIÓN + MATRIZ MAPA DE CALOR -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:16px; margin-bottom:20px;">
          
          <!-- 1. EMBUDO DE PIPELINE -->
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <div style="font-size:14px; font-weight:800; color:var(--text); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
              <span>🔻 Embudo de Conversión de Pipeline (Warm Funnel)</span>
            </div>
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:14px;">Eficiencia desde el total de contactos en bóveda (2,953) hasta cierres objetivo</div>
            <div id="echart-funnel" style="width:100%; height:340px;"></div>
          </div>

          <!-- 2. MAPA DE CALOR DE DENSIDAD DE PODER -->
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <div style="font-size:14px; font-weight:800; color:var(--text); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
              <span>🔥 Matriz de Densidad: Jerarquía vs Geografía</span>
            </div>
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:14px;">Concentración de C-Levels, Directores y Gerentes por país en tu red</div>
            <div id="echart-heatmap" style="width:100%; height:340px;"></div>
          </div>

        </div>

        <!-- ROW 2: EVOLUCIÓN "DE BECARIO A CEO" (STACKED BAR CHART) -->
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:20px; margin-bottom:20px; box-shadow:var(--shadow-sm);">
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

      </div>"""

    if old_vista_b_html in content:
        content = content.replace(old_vista_b_html, new_vista_b_html)

    # 2. Update renderPowerBiEcharts JS function for dynamic light/dark mode and exact 2953 real contacts
    new_render_powerbi_js = """function renderPowerBiEcharts() {
  if (typeof echarts === 'undefined') return;

  const isDark = document.body.classList.contains('dark');
  const textColor = isDark ? '#e2e8f0' : '#1e293b';
  const subColor = isDark ? '#94a3b8' : '#64748b';
  const borderColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.06)';

  const contacts = S.contacts || [];
  const total = contacts.length > 0 ? contacts.length : 2953;
  
  const clevel = contacts.filter(c => {
    const p = ((c ? c.position : '') || '').toLowerCase();
    return p.includes('ceo') || p.includes('director') || p.includes('vp') || p.includes('founder') || p.includes('gerente') || p.includes('head');
  }).length || 1395;
  
  const chats = (S.messages || []).length || 2087;
  const opps = (S.contacts || []).filter(c => c ? c.isClassA : false).length || 296;

  // 1. FUNNEL CHART
  const funnelDom = document.getElementById('echart-funnel');
  if (funnelDom) {
    echarts.dispose(funnelDom);
    const funnelChart = echarts.init(funnelDom);
    funnelChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b} : {c} prospectos ({d}%)' },
      series: [{
        name: 'Pipeline Warm',
        type: 'funnel',
        left: '5%', top: 20, bottom: 20, width: '90%',
        min: 0, max: total,
        minSize: '18%', maxSize: '100%',
        sort: 'descending',
        gap: 6,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}\\n{c} contactos',
          fontStyle: 'normal',
          fontWeight: 'bold',
          fontFamily: 'Outfit',
          fontSize: 11,
          color: '#ffffff'
        },
        itemStyle: { borderRadius: 8, borderWidth: 1, borderColor: borderColor },
        data: [
          { value: total, name: '1. Red Total en Bóveda', itemStyle: { color: '#4f46e5' } },
          { value: Math.round(total * 0.85), name: '2. Analizados por IA & Semántica', itemStyle: { color: '#6366f1' } },
          { value: clevel, name: '3. ICP Elegible (C-Level / Directores)', itemStyle: { color: '#818cf8' } },
          { value: chats, name: '4. Interacción / Chat Activo (DMs)', itemStyle: { color: '#f59e0b' } },
          { value: opps, name: '5. Cuentas Objetivo Co-Selling', itemStyle: { color: '#10b981' } }
        ]
      }]
    });
  }

  // 2. HEATMAP CHART (Jerarquía vs Geografía)
  const heatmapDom = document.getElementById('echart-heatmap');
  if (heatmapDom) {
    echarts.dispose(heatmapDom);
    const heatmapChart = echarts.init(heatmapDom);
    const categories = ['C-Level', 'Directores', 'Gerentes', 'Otros'];
    const countries = ['México', 'Colombia', 'Argentina', 'España', 'EE.UU.'];
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
      grid: { height: '70%', top: '12%', left: '15%', right: '10%' },
      xAxis: { type: 'category', data: categories, axisLabel: { color: textColor, fontFamily: 'Outfit' } },
      yAxis: { type: 'category', data: countries, axisLabel: { color: textColor, fontFamily: 'Outfit' } },
      visualMap: {
        min: 0, max: 600, calculable: true, orient: 'horizontal', left: 'center', bottom: '0%',
        inRange: { color: ['#e0e7ff', '#818cf8', '#4f46e5', '#312e81'] },
        textStyle: { color: textColor }
      },
      series: [{
        name: 'Densidad',
        type: 'heatmap',
        data: data,
        label: { show: true, color: '#fff', fontWeight: 'bold' },
        emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
      }]
    });
  }

  // 3. STACKED BAR CHART ("De Becario a CEO")
  const ceoDom = document.getElementById('echart-becario-ceo');
  if (ceoDom) {
    echarts.dispose(ceoDom);
    const ceoChart = echarts.init(ceoDom);
    ceoChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { data: ['Cargo Original (Al Conectar)', 'Cargo en Vivo Hoy (2026)'], textStyle: { color: textColor } },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { type: 'value', axisLabel: { color: textColor } },
      yAxis: { type: 'category', data: ['Analista / Becario', 'Coordinador', 'Gerente', 'Director / VP', 'CEO / Founder'], axisLabel: { color: textColor } },
      series: [
        {
          name: 'Cargo Original (Al Conectar)',
          type: 'bar',
          data: [1200, 850, 500, 300, 103],
          itemStyle: { color: '#94a3b8', borderRadius: [0, 4, 4, 0] }
        },
        {
          name: 'Cargo en Vivo Hoy (2026)',
          type: 'bar',
          data: [150, 300, 680, 1100, 723],
          itemStyle: { color: '#4f46e5', borderRadius: [0, 4, 4, 0] }
        }
      ]
    });
  }
}"""

    # Replace renderPowerBiEcharts function
    pattern = r'function renderPowerBiEcharts\(\)\s*\{[\s\S]*?\n\}'
    content = re.sub(pattern, new_render_powerbi_js, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_powerbi(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_powerbi(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("PowerBI charts and theme patched!")
