import urllib.request, json
import jsonschema

url = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    schema = json.loads(response.read().decode('utf-8'))

test_report = {
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
    },
    "customTheme": {
      "name": "IPL_Dark_Analytics",
      "reportVersionAtImport": {
        "visual": "2.14.0",
        "report": "3.4.0",
        "page": "2.3.1"
      },
      "type": "RegisteredResources"
    }
  },
  "resourcePackages": [
    {
      "name": "RegisteredResources",
      "type": "RegisteredResources",
      "items": [
        {
          "name": "IPL_Dark_Analytics",
          "path": "IPL_Dark_Analytics.json",
          "type": "CustomTheme"
        }
      ]
    }
  ],
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

jsonschema.validate(instance=test_report, schema=schema)
print("SUCCESS: VALIDATED AGAINST OFFICIAL MICROSOFT SCHEMA!")
