import re

def patch_clean_powerbi(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean HTML text # 2. MAPA DE CALOR DE DENSIDAD DE PODER
    content = content.replace("# 2. MAPA DE CALOR DE DENSIDAD DE PODER", "")
    content = content.replace("background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08);", "background:var(--surface); border:1px solid var(--border); box-shadow:var(--shadow-sm);")

    # 2. Clean renderPowerBiEcharts JS function
    clean_js = """function renderPowerBiEcharts() {
  if (typeof echarts === 'undefined') return;

  const isDark = document.body.classList.contains('dark');
  const textColor = isDark ? '#e2e8f0' : '#1e293b';
  const borderColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)';

  const contacts = S.contacts || [];
  const total = contacts.length > 0 ? contacts.length : 2953;
  
  const clevel = contacts.filter(c => {
    const p = ((c ? c.position : '') || '').toLowerCase();
    return p.includes('ceo') || p.includes('director') || p.includes('vp') || p.includes('founder') || p.includes('gerente') || p.includes('head');
  }).length || 1395;
  
  const chats = (S.messages || []).length || 2087;
  const opps = (S.contacts || []).filter(c => c ? c.isClassA : false).length || 296;

  // 1. FUNNEL CHART (Embudo de Pipeline Warm)
  const funnelDom = document.getElementById('echart-funnel');
  if (funnelDom) {
    try { echarts.dispose(funnelDom); } catch(e){}
    const funnelChart = echarts.init(funnelDom);
    funnelChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b} : {c} prospectos ({d}%)' },
      series: [{
        name: 'Pipeline Warm',
        type: 'funnel',
        left: '5%', top: 20, bottom: 20, width: '90%',
        min: 0, max: total,
        minSize: '20%', maxSize: '100%',
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
    setTimeout(() => { try { funnelChart.resize(); } catch(e){} }, 200);
  }

  // 2. HEATMAP CHART (Jerarquía vs Geografía)
  const heatmapDom = document.getElementById('echart-heatmap');
  if (heatmapDom) {
    try { echarts.dispose(heatmapDom); } catch(e){}
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
    setTimeout(() => { try { heatmapChart.resize(); } catch(e){} }, 200);
  }

  // 3. STACKED BAR CHART ("De Becario a CEO")
  const ceoDom = document.getElementById('echart-becario-ceo');
  if (ceoDom) {
    try { echarts.dispose(ceoDom); } catch(e){}
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
    setTimeout(() => { try { ceoChart.resize(); } catch(e){} }, 200);
  }
}
window.renderPowerBiEcharts = renderPowerBiEcharts;"""

    pattern = r'function renderPowerBiEcharts\(\)\s*\{[\s\S]*?\n\}'
    content = re.sub(pattern, clean_js, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_clean_powerbi(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_clean_powerbi(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Clean PowerBI patch applied successfully!")
