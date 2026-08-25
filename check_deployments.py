import urllib.request

headers = {'User-Agent': 'Mozilla/5.0'}

gh_url = 'https://agutierrez11.github.io/Radar-comercial-linkedin/'
cf_url = 'https://radar-comercial-lknd.pages.dev/'

print("=== CHECKING GITHUB PAGES ===")
req_gh = urllib.request.Request(gh_url, headers=headers)
html_gh = urllib.request.urlopen(req_gh).read().decode('utf-8')
print("Contains 'Continuar con Google':", 'Continuar con Google' in html_gh)
print("Contains 'fillQuickLogin':", 'fillQuickLogin' in html_gh)
print("Contains 'login-error-alert':", 'login-error-alert' in html_gh)

print("\n=== CHECKING CLOUDFLARE PAGES ===")
req_cf = urllib.request.Request(cf_url, headers=headers)
html_cf = urllib.request.urlopen(req_cf).read().decode('utf-8')
print("Contains 'Continuar con Google':", 'Continuar con Google' in html_cf)
print("Contains 'fillQuickLogin':", 'fillQuickLogin' in html_cf)
print("Contains 'login-error-alert':", 'login-error-alert' in html_cf)
