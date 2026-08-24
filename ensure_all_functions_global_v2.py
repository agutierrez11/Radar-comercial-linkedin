import re

def make_global(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find function navigate, function switchAnalyticsViewMode, function renderPowerBiEcharts, etc.
    funcs = ['navigate', 'switchAnalyticsViewMode', 'renderPowerBiEcharts', 'loadDemoData', 'switchVaultViewMode', 'applyNetworkFilters', 'resetMapZoom', 'unlockAnalyticsUI', 'closeLoginModal', 'quickLogin', 'submitCustomLogin', 'toggleAdminVaultMenu', 'toggleTheme', 'openAIConfigModal', 'exportCSV', 'exportVaultJson', 'importVaultJson']
    
    bind_code = "\n" + "\n".join([f"if (typeof {fn} !== 'undefined') window.{fn} = {fn};" for fn in funcs]) + "\n"

    for fn in funcs:
        content = content.replace(f"function {fn}(", f"window.{fn} = function {fn}(")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

make_global(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
make_global(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Functions bound globally!")
