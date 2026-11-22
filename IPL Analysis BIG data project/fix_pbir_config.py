import json
import os

report_dir = r"c:\Users\swast\Documents\IPL Analysis BIG data project\IPL_Analytics_Dashboard.Report"

# 1. Update definition.pbir
pbir_path = os.path.join(report_dir, "definition.pbir")
pbir_data = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
    "version": "4.0",
    "datasetReference": {
        "byPath": {
            "path": "../IPL_Analytics_Dashboard.SemanticModel"
        },
        "byConnection": None
    }
}
with open(pbir_path, "w", encoding="utf-8") as f:
    json.dump(pbir_data, f, indent=2)
print("Updated definition.pbir successfully")

# 2. Update definition/report.json
def_report_path = os.path.join(report_dir, "definition", "report.json")
def_report_data = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
    "themeCollection": {
        "baseTheme": {
            "name": "Fluent2-CY26SU10",
            "reportVersionAtImport": {
                "visual": "2.14.0",
                "report": "3.4.0",
                "page": "2.3.1"
            },
            "type": "SharedResources"
        }
    },
    "objects": {
        "section": [
            {
                "properties": {
                    "verticalAlignment": {
                        "expr": {
                            "Literal": {
                                "Value": "'Top'"
                            }
                        }
                    }
                }
            }
        ]
    },
    "settings": {
        "useStylableVisualContainerHeader": True,
        "exportDataMode": "AllowSummarized",
        "defaultDrillFilterOtherVisuals": True,
        "allowChangeFilterTypes": True,
        "useEnhancedTooltips": True,
        "useDefaultAggregateDisplayName": True
    }
}
with open(def_report_path, "w", encoding="utf-8") as f:
    json.dump(def_report_data, f, indent=2)
print("Updated definition/report.json successfully")

# 3. Remove legacy report.json at root of IPL_Analytics_Dashboard.Report if it conflicts with PBIR
legacy_root_report = os.path.join(report_dir, "report.json")
if os.path.exists(legacy_root_report):
    # Rename to report.json.bak so it does not confuse PBIR loader
    backup_path = legacy_root_report + ".bak"
    if os.path.exists(backup_path):
        os.remove(backup_path)
    os.rename(legacy_root_report, backup_path)
    print("Renamed legacy root report.json to report.json.bak")

print("All PBIR configs aligned!")
