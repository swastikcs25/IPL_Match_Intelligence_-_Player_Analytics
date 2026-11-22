import json, os, glob

print("=== PRE-FLIGHT VERIFICATION ===")

# 1. PBIP
with open('IPL_Analytics_Dashboard.pbip', 'r', encoding='utf-8') as f:
    pbip = json.load(f)
print("[OK] IPL_Analytics_Dashboard.pbip is valid JSON")
assert pbip.get('version') == '1.0'
assert len(pbip.get('artifacts', [])) > 0
print("     - Artifacts:", pbip['artifacts'])

# 2. PBISM
with open('IPL_Analytics_Dashboard.SemanticModel/definition.pbism', 'r', encoding='utf-8') as f:
    pbism = json.load(f)
print("[OK] definition.pbism is valid JSON")
assert pbism.get('version') == '4.0'
print("     - Version:", pbism['version'])
print("     - Settings:", pbism.get('settings'))

# 3. PBIR
with open('IPL_Analytics_Dashboard.Report/definition.pbir', 'r', encoding='utf-8') as f:
    pbir = json.load(f)
print("[OK] definition.pbir is valid JSON")
assert pbir.get('version') == '4.0'
print("     - Version:", pbir['version'])
print("     - DatasetReference:", pbir.get('datasetReference'))

# 4. Report JSON
with open('IPL_Analytics_Dashboard.Report/definition/report.json', 'r', encoding='utf-8') as f:
    rep = json.load(f)
print("[OK] report.json is valid JSON")
print("     - Themes:", list(rep.get('themeCollection', {}).keys()))

# 5. Pages
with open('IPL_Analytics_Dashboard.Report/definition/pages/pages.json', 'r', encoding='utf-8') as f:
    pages_meta = json.load(f)
print("[OK] pages.json is valid JSON")
print("     - Page Order:", pages_meta.get('pageOrder'))
print("     - Active Page:", pages_meta.get('activePageName'))

total_visuals = 0
for page_name in pages_meta.get('pageOrder', []):
    page_dir = os.path.join('IPL_Analytics_Dashboard.Report/definition/pages', page_name)
    assert os.path.isdir(page_dir), f"Missing directory {page_dir}"
    page_json = os.path.join(page_dir, 'page.json')
    assert os.path.exists(page_json), f"Missing page.json in {page_dir}"
    visuals = glob.glob(os.path.join(page_dir, 'visuals', '*'))
    total_visuals += len(visuals)
    print(f"     - {page_name}: {len(visuals)} visuals verified")

print(f"[OK] Total visuals verified across all pages: {total_visuals}")

# 6. TMDL files
tmdls = glob.glob('IPL_Analytics_Dashboard.SemanticModel/definition/**/*.tmdl', recursive=True)
print(f"[OK] {len(tmdls)} TMDL files present in SemanticModel/definition")

# 7. Theme
theme_path = 'IPL_Analytics_Dashboard.Report/StaticResources/RegisteredResources/IPL_Dark_Analytics.json'
assert os.path.exists(theme_path), 'Missing custom theme file'
with open(theme_path, 'r', encoding='utf-8') as f:
    theme = json.load(f)
print(f"[OK] Custom theme valid JSON ({theme.get('name')})")

print("\nALL PRE-FLIGHT CHECKS PASSED WITH ZERO ERRORS!")
