import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up window.fn = function fn(
    funcs = ['navigate', 'switchAnalyticsViewMode', 'renderPowerBiEcharts', 'loadDemoData', 'switchVaultViewMode', 'applyNetworkFilters', 'resetMapZoom', 'unlockAnalyticsUI', 'closeLoginModal', 'quickLogin', 'submitCustomLogin', 'toggleAdminVaultMenu', 'toggleTheme', 'openAIConfigModal', 'exportCSV', 'exportVaultJson', 'importVaultJson']

    for fn in funcs:
        content = content.replace(f"window.{fn} = function {fn}(", f"function {fn}(")

    # Add clean window assignments at the very top script block
    top_window_assignments = "\n" + "\n".join([f"window.{fn} = function(...args) {{ if (typeof {fn} === 'function') return {fn}(...args); }};" for fn in funcs]) + "\n"

    # Insert after initial <script>
    if "window.renderPowerBiEcharts =" not in content:
        content = content.replace("<script>", "<script>\n" + top_window_assignments, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_file(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
clean_file(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Clean window bindings applied!")
