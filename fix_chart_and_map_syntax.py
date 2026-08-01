import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove extra brace on line 1881 inside initGisMap
old_gis_init = """    gisLayerGroup = L.layerGroup().addTo(gisMap);
  }
  }"""
new_gis_init = """    gisLayerGroup = L.layerGroup().addTo(gisMap);
  }"""

if old_gis_init in html:
    html = html.replace(old_gis_init, new_gis_init)
    print("✅ Sintaxis de initGisMap corregida (llave extra eliminada).")

# 2. Fix Chart.js y-axis ticks autoSkip: false so NO country label is skipped or hidden
old_chart_y = "y: { ticks: { color: txtColor, font:{size:10} }, grid: { display: false } }"
new_chart_y = "y: { ticks: { color: txtColor, autoSkip: false, font:{size:11, family:'Outfit'} }, grid: { display: false } }"

if old_chart_y in html:
    html = html.replace(old_chart_y, new_chart_y)
    print("✅ Chart.js autoSkip desactivado: Todos los nombres de países se mostrarán visibles sin saltar ningún país.")

# 3. Adjust chart container height in CSS
old_chart_css = ".chart-container { height: 160px; position: relative; }"
new_chart_css = ".chart-container { height: 240px; position: relative; }"

if old_chart_css in html:
    html = html.replace(old_chart_css, new_chart_css)
    print("✅ Chart-container ampliado a 240px de altura para acomodar todas las etiquetas de países.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Todos los fixes aplicados a index.html")
