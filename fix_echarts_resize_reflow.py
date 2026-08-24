import re

def fix_reflow(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update switchAnalyticsViewMode to use setTimeout before renderPowerBiEcharts
    old_switch = """if (mode === 'B') {
    if (btnB) { btnB.classList.add('active'); btnB.style.background = 'var(--accent)'; btnB.style.color = '#fff'; }
    if (btnA) { btnA.classList.remove('active'); btnA.style.background = 'transparent'; btnA.style.color = 'var(--text-muted)'; }
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    if (typeof renderPowerBiEcharts === 'function') renderPowerBiEcharts();
    if (typeof showToast === 'function') showToast('⚡ Vista Power BI Executive Suite (Apache ECharts) activada.', '⚡');
  }"""

    new_switch = """if (mode === 'B') {
    if (btnB) { btnB.classList.add('active'); btnB.style.background = 'var(--accent)'; btnB.style.color = '#fff'; }
    if (btnA) { btnA.classList.remove('active'); btnA.style.background = 'transparent'; btnA.style.color = 'var(--text-muted)'; }
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    setTimeout(() => {
      if (typeof renderPowerBiEcharts === 'function') renderPowerBiEcharts();
    }, 100);
    if (typeof showToast === 'function') showToast('⚡ Vista Power BI Executive Suite (Apache ECharts) activada.', '⚡');
  }"""

    if old_switch in content:
        content = content.replace(old_switch, new_switch)

    # Add resize calls inside renderPowerBiEcharts
    if 'funnelChart.setOption(' in content and 'funnelChart.resize()' not in content:
        content = content.replace(
            "funnelChart.setOption({",
            "funnelChart.setOption({\n"
        )
        content = content.replace(
            "// 2. HEATMAP CHART",
            "setTimeout(() => { try { funnelChart.resize(); } catch(e){} }, 150);\n  // 2. HEATMAP CHART"
        )
        content = content.replace(
            "// 3. STACKED BAR CHART",
            "setTimeout(() => { try { heatmapChart.resize(); } catch(e){} }, 150);\n  // 3. STACKED BAR CHART"
        )
        content = content.replace(
            "ceoChart.setOption({",
            "ceoChart.setOption({\n"
        )
        # Add resize for ceoChart at bottom of function
        content = content.replace(
            "  }\n}",
            "    setTimeout(() => { try { ceoChart.resize(); } catch(e){} }, 150);\n  }\n}"
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_reflow(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_reflow(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Reflow and resize fixed!")
