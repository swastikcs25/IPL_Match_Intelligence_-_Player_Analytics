import os
import re

BASE_DIR = r"C:\Users\swast\Documents\IPL Analysis BIG data project"
SEMANTIC_DIR = os.path.join(BASE_DIR, "IPL_Analytics_Dashboard.SemanticModel")
DEF_DIR = os.path.join(SEMANTIC_DIR, "definition")
TABLES_DIR = os.path.join(DEF_DIR, "tables")
CULTURES_DIR = os.path.join(DEF_DIR, "cultures")

os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(CULTURES_DIR, exist_ok=True)

# definition.pbism
with open(os.path.join(SEMANTIC_DIR, "definition.pbism"), "w", encoding="utf-8") as f:
    f.write('{\n  "version": "1.0"\n}\n')

# database.tmdl
with open(os.path.join(DEF_DIR, "database.tmdl"), "w", encoding="utf-8") as f:
    f.write('database\n\tcompatibilityLevel: 1550\n')

# Read exported TMDL
with open(r'C:\Users\swast\.gemini\antigravity\brain\c2d99e17-6c15-4b63-963b-ac5550c2d4be\.system_generated\steps\106\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# Slice sections based on known line indices
# Indices:
# 9: table 'Gold Player phase stats'
# 78: table 'gold venue stats'
# 122: table 'Gold weather impact'
# 238: table DateTableTemplate_0e87374e-1a0d-4a84-8128-c2a72ef91164
# 356: table LocalDateTable_f79414b4-2a98-4eae-98f6-bdade8f796d9
# 472: table 'toss stat'
# 523: table _Measures
# 672: table Dim_Venue
# 685: table Dim_Toss_Decision
# 697: relationships start
# 718: cultureInfo en-IN

table_slices = [
    ("Gold Player phase stats", 9, 78),
    ("gold venue stats", 78, 122),
    ("Gold weather impact", 122, 238),
    ("DateTableTemplate_0e87374e-1a0d-4a84-8128-c2a72ef91164", 238, 356),
    ("LocalDateTable_f79414b4-2a98-4eae-98f6-bdade8f796d9", 356, 472),
    ("toss stat", 472, 523),
    ("_Measures", 523, 672),
    ("Dim_Venue", 672, 685),
    ("Dim_Toss_Decision", 685, 697),
]

def unindent(line):
    if line.startswith('\t'):
        return line[1:]
    return line

for tbl_name, start, end in table_slices:
    tbl_lines = lines[start:end]
    # Remove one leading tab
    processed = [unindent(l) for l in tbl_lines]
    # Strip empty trailing lines
    while processed and not processed[-1].strip():
        processed.pop()
    content = "\n".join(processed) + "\n"
    out_path = os.path.join(TABLES_DIR, f"{tbl_name}.tmdl")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote table: {tbl_name}.tmdl")

# relationships.tmdl
rel_lines = lines[697:718]
rel_processed = [unindent(l) for l in rel_lines]
while rel_processed and not rel_processed[-1].strip():
    rel_processed.pop()
with open(os.path.join(DEF_DIR, "relationships.tmdl"), "w", encoding="utf-8") as f:
    f.write("\n".join(rel_processed) + "\n")
print("Wrote relationships.tmdl")

# cultures/en-IN.tmdl
with open(os.path.join(CULTURES_DIR, "en-IN.tmdl"), "w", encoding="utf-8") as f:
    f.write("cultureInfo en-IN\n")
print("Wrote cultures/en-IN.tmdl")

# model.tmdl
model_lines = lines[0:9]
model_content = "\n".join(model_lines) + """
\tannotation __PBI_TimeIntelligenceEnabled = 1

\tannotation PBIDesktopVersion = 2.159.1231.0 (24.12)

\tannotation PBI_QueryOrder = ["Gold Player phase stats","gold venue stats","Gold weather impact","toss stat"]

\tannotation PBI_ProTooling = ["MCP-PBIModeling"]
"""
with open(os.path.join(DEF_DIR, "model.tmdl"), "w", encoding="utf-8") as f:
    f.write(model_content.strip() + "\n")
print("Wrote model.tmdl")

print("All SemanticModel TMDL files successfully written!")
