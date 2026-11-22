import os, json

base = r'c:\Users\swast\Documents\IPL Analysis BIG data project'
report_dir = os.path.join(base, 'IPL_Analytics_Dashboard.Report')
model_dir  = os.path.join(base, 'IPL_Analytics_Dashboard.SemanticModel')

print("=" * 60)
print("FINAL STATE VALIDATION")
print("=" * 60)

# 1. definition.pbir
pbir = json.load(open(os.path.join(report_dir, 'definition.pbir')))
has_schema = any('schema' in k for k in pbir.keys())
print(f"\n1. definition.pbir")
print(f"   Has $schema: {has_schema}")
print(f"   Version: {pbir.get('version')}")
print(f"   Dataset path: {pbir.get('datasetReference',{}).get('byPath',{}).get('path','?')}")

# 2. definition/report.json
rep = json.load(open(os.path.join(report_dir, 'definition', 'report.json')))
rep_schema = rep.get('$schema','NOT SET')
print(f"\n2. definition/report.json")
print(f"   Schema: {rep_schema[-30:]}")

# 3. definition/version.json
ver = json.load(open(os.path.join(report_dir, 'definition', 'version.json')))
print(f"\n3. definition/version.json: {ver}")

# 4. pages.json + visuals
pages = json.load(open(os.path.join(report_dir, 'definition', 'pages', 'pages.json')))
print(f"\n4. Pages ({len(pages['pageOrder'])} total):")
total_visuals = 0
for pid in pages['pageOrder']:
    pdir = os.path.join(report_dir, 'definition', 'pages', pid)
    vdir = os.path.join(pdir, 'visuals')
    pjson = json.load(open(os.path.join(pdir, 'page.json')))
    vcount = 0
    if os.path.exists(vdir):
        for root, dirs, files in os.walk(vdir):
            for f in files:
                if f == 'visual.json':
                    vcount += 1
    total_visuals += vcount
    print(f"   [{pjson['displayName']}] ({pjson['width']}x{pjson['height']}) -> {vcount} visuals")
print(f"   TOTAL VISUALS: {total_visuals}")

# 5. SemanticModel
pbism = json.load(open(os.path.join(model_dir, 'definition.pbism')))
pbism_schema_ok = any('schema' in k for k in pbism.keys())
tables = [f.replace('.tmdl','') for f in os.listdir(os.path.join(model_dir, 'definition', 'tables'))]
print(f"\n5. SemanticModel")
print(f"   definition.pbism $schema: {'OK' if pbism_schema_ok else 'MISSING'}")
print(f"   Tables ({len(tables)}): {', '.join(tables)}")

# 6. .pbix
pbix = os.path.join(base, 'IPL_Analytics_Dashboard.pbix')
print(f"\n6. .pbix size: {os.path.getsize(pbix):,} bytes")

# 7. .pbip
pbip = json.load(open(os.path.join(base, 'IPL_Analytics_Dashboard.pbip')))
print(f"\n7. .pbip artifacts: {pbip.get('artifacts')}")

# 8. Theme
theme_path = os.path.join(report_dir, 'StaticResources', 'RegisteredResources', 'IPL_Dark_Analytics.json')
print(f"\n8. Theme file: {'EXISTS' if os.path.exists(theme_path) else 'MISSING'}")

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)
