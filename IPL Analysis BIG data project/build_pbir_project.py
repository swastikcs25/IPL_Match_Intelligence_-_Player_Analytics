import os
import json
import shutil

BASE_DIR = r"C:\Users\swast\Documents\IPL Analysis BIG data project"
REPORT_DIR = os.path.join(BASE_DIR, "IPL_Analytics_Dashboard.Report")
MODEL_DIR = os.path.join(BASE_DIR, "IPL_Analytics_Dashboard.SemanticModel")
THEME_FILE = os.path.join(BASE_DIR, "IPL_Dark_Analytics.json")
PBIP_FILE = os.path.join(BASE_DIR, "IPL_Analytics_Dashboard.pbip")

# 1. Custom Theme JSON
theme_config = {
    "name": "IPL Dark Analytics",
    "dataColors": [
        "#F5B700",  # Gold / Trophy Primary Accent
        "#00B4D8",  # Electric Cyan Secondary Accent
        "#EF476F",  # Alert / Rain Coral Red
        "#48CAE4",  # Sky Blue
        "#FFD166",  # Warm Yellow
        "#06D6A0",  # Emerald Green
        "#118AB2",  # Deep Teal
        "#F77F00"   # Amber Orange
    ],
    "background": "#0B132B",
    "foreground": "#FFFFFF",
    "tableAccent": "#F5B700",
    "visualStyles": {
        "*": {
            "*": {
                "background": [
                    {
                        "color": { "solid": { "color": "#1C2541" } },
                        "transparency": 0
                    }
                ],
                "border": [
                    {
                        "show": True,
                        "color": { "solid": { "color": "#3A506B" } },
                        "radius": 8
                    }
                ],
                "title": [
                    {
                        "show": True,
                        "fontColor": { "solid": { "color": "#FFFFFF" } },
                        "fontSize": 12,
                        "fontFamily": "Segoe UI Semibold"
                    }
                ],
                "subTitle": [
                    {
                        "show": True,
                        "fontColor": { "solid": { "color": "#CBD5E1" } },
                        "fontSize": 9,
                        "fontFamily": "Segoe UI"
                    }
                ],
                "labels": [
                    {
                        "color": { "solid": { "color": "#CBD5E1" } },
                        "fontSize": 10,
                        "fontFamily": "Segoe UI"
                    }
                ],
                "categoryAxis": [
                    {
                        "labelColor": { "solid": { "color": "#CBD5E1" } },
                        "titleColor": { "solid": { "color": "#FFFFFF" } },
                        "gridlineColor": { "solid": { "color": "#223150" } }
                    }
                ],
                "valueAxis": [
                    {
                        "labelColor": { "solid": { "color": "#CBD5E1" } },
                        "titleColor": { "solid": { "color": "#FFFFFF" } },
                        "gridlineColor": { "solid": { "color": "#223150" } }
                    }
                ]
            }
        },
        "page": {
            "*": {
                "background": [
                    {
                        "color": { "solid": { "color": "#0B132B" } },
                        "transparency": 0
                    }
                ]
            }
        },
        "card": {
            "*": {
                "labels": [
                    {
                        "color": { "solid": { "color": "#FFFFFF" } },
                        "fontSize": 24,
                        "fontFamily": "Segoe UI Semibold"
                    }
                ],
                "categoryLabels": [
                    {
                        "show": True,
                        "color": { "solid": { "color": "#CBD5E1" } },
                        "fontSize": 10,
                        "fontFamily": "Segoe UI"
                    }
                ]
            }
        },
        "tableEx": {
            "*": {
                "grid": [
                    {
                        "gridVertical": True,
                        "gridVerticalColor": { "solid": { "color": "#3A506B" } },
                        "gridHorizontal": True,
                        "gridHorizontalColor": { "solid": { "color": "#3A506B" } }
                    }
                ],
                "columnHeaders": [
                    {
                        "fontColor": { "solid": { "color": "#FFFFFF" } },
                        "backColor": { "solid": { "color": "#111B33" } },
                        "fontFamily": "Segoe UI Semibold",
                        "fontSize": 10
                    }
                ],
                "values": [
                    {
                        "fontColorPrimary": { "solid": { "color": "#CBD5E1" } },
                        "backColorPrimary": { "solid": { "color": "#1C2541" } },
                        "fontColorSecondary": { "solid": { "color": "#CBD5E1" } },
                        "backColorSecondary": { "solid": { "color": "#161E34" } },
                        "fontFamily": "Segoe UI",
                        "fontSize": 10
                    }
                ]
            }
        }
    }
}

# Write theme to workspace
with open(THEME_FILE, "w", encoding="utf-8") as f:
    json.dump(theme_config, f, indent=2)

# 2. Master PBIP File
pbip_config = {
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": "IPL_Analytics_Dashboard.Report"
            }
        }
    ],
    "settings": {
        "enableAutoAuth": True
    }
}
with open(PBIP_FILE, "w", encoding="utf-8") as f:
    json.dump(pbip_config, f, indent=2)

# 3. Create Report Structure
os.makedirs(os.path.join(REPORT_DIR, ".pbi"), exist_ok=True)
os.makedirs(os.path.join(REPORT_DIR, "StaticResources", "RegisteredResources"), exist_ok=True)
definition_dir = os.path.join(REPORT_DIR, "definition")
pages_dir = os.path.join(definition_dir, "pages")
os.makedirs(pages_dir, exist_ok=True)

# Copy theme to RegisteredResources
shutil.copyfile(THEME_FILE, os.path.join(REPORT_DIR, "StaticResources", "RegisteredResources", "IPL_Dark_Analytics.json"))

# localSettings.json
with open(os.path.join(REPORT_DIR, ".pbi", "localSettings.json"), "w", encoding="utf-8") as f:
    json.dump({"version": "1.0"}, f, indent=2)

# definition.pbir
definition_pbir = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
    "version": "4.0",
    "datasetReference": {
        "byPath": {
            "path": "../IPL_Analytics_Dashboard.SemanticModel"
        },
        "byConnection": None
    }
}
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(definition_pbir, f, indent=2)

# definition/version.json
with open(os.path.join(definition_dir, "version.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/version/1.0.0/schema.json",
        "version": "2.0.0"
    }, f, indent=2)

# definition/report.json
report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.1.0/schema.json",
    "themeCollection": {
        "customTheme": {
            "name": "IPL_Dark_Analytics",
            "reportVersionAtImport": {
                "visual": "2.5.0",
                "report": "3.1.0",
                "page": "2.3.0"
            },
            "type": "RegisteredResources"
        }
    },
    "settings": {
        "useNewFilterPaneExperience": True,
        "allowChangeFilterTypes": True,
        "useStylableVisualContainerHeader": True,
        "queryLimitOption": 6
    }
}
with open(os.path.join(definition_dir, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

# definition/pages/pages.json
pages_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
    "pageOrder": [
        "Page1_ExecutiveSummary",
        "Page2_TossStrategy",
        "Page3_VenueWeather",
        "Page4_PlayerPerformance",
        "Tooltip_BatterBreakdown"
    ],
    "activePageName": "Page1_ExecutiveSummary"
}
with open(os.path.join(pages_dir, "pages.json"), "w", encoding="utf-8") as f:
    json.dump(pages_json, f, indent=2)

# Helper functions for PBIR visual generation
def make_measure_projection(table, measure, query_ref=None):
    qref = query_ref or f"{table}.{measure}"
    return {
        "field": {
            "Measure": {
                "Expression": {
                    "SourceRef": {
                        "Entity": table
                    }
                },
                "Property": measure
            }
        },
        "queryRef": qref,
        "nativeQueryRef": measure
    }

def make_column_projection(table, column, query_ref=None, active=True):
    qref = query_ref or f"{table}.{column}"
    proj = {
        "field": {
            "Column": {
                "Expression": {
                    "SourceRef": {
                        "Entity": table
                    }
                },
                "Property": column
            }
        },
        "queryRef": qref,
        "nativeQueryRef": column
    }
    if active:
        proj["active"] = True
    return proj

def make_visual_file(page_path, visual_name, visual_type, position, query_state=None, objects=None):
    vis_dir = os.path.join(page_path, "visuals", visual_name)
    os.makedirs(vis_dir, exist_ok=True)
    vis_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
        "name": visual_name,
        "position": position,
        "visual": {
            "visualType": visual_type
        }
    }
    if query_state:
        vis_data["visual"]["query"] = {
            "queryState": query_state
        }
    if objects:
        vis_data["visual"]["objects"] = objects
    with open(os.path.join(vis_dir, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(vis_data, f, indent=2)

def make_header_textbox(page_path, visual_name, title, subtitle):
    pos = {"x": 16, "y": 16, "z": 0, "width": 760, "height": 64, "tabOrder": 0}
    objs = {
        "general": [
            {
                "properties": {
                    "paragraphs": [
                        {
                            "textRuns": [
                                {
                                    "value": title + "\n",
                                    "textStyle": {
                                        "fontFamily": "Segoe UI Semibold",
                                        "fontSize": "15pt",
                                        "fontWeight": "bold",
                                        "color": "#FFFFFF"
                                    }
                                },
                                {
                                    "value": subtitle,
                                    "textStyle": {
                                        "fontFamily": "Segoe UI",
                                        "fontSize": "9pt",
                                        "color": "#CBD5E1"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    make_visual_file(page_path, visual_name, "textbox", pos, objects=objs)

def make_slicer(page_path, visual_name, x, y, width, height, z, tab_order, table, column, title):
    pos = {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": tab_order}
    query_state = {
        "Values": {
            "projections": [make_column_projection(table, column)]
        }
    }
    objs = {
        "general": [
            {
                "properties": {
                    "title": {
                        "expr": {
                            "Literal": {
                                "Value": f"'{title}'"
                            }
                        }
                    }
                }
            }
        ]
    }
    make_visual_file(page_path, visual_name, "slicer", pos, query_state=query_state, objects=objs)

def make_card(page_path, visual_name, x, y, width, height, z, tab_order, table, measure, title):
    pos = {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": tab_order}
    query_state = {
        "Values": {
            "projections": [make_measure_projection(table, measure)]
        }
    }
    objs = {
        "general": [
            {
                "properties": {
                    "title": {
                        "expr": {
                            "Literal": {
                                "Value": f"'{title}'"
                            }
                        }
                    }
                }
            }
        ]
    }
    make_visual_file(page_path, visual_name, "card", pos, query_state=query_state, objects=objs)

# ----------------- PAGE 1: Executive Summary -----------------
p1_dir = os.path.join(pages_dir, "Page1_ExecutiveSummary")
os.makedirs(p1_dir, exist_ok=True)
with open(os.path.join(p1_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "Page1_ExecutiveSummary",
        "displayName": "Executive Summary",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280
    }, f, indent=2)

make_header_textbox(
    p1_dir, "v01_header",
    "IPL EXECUTIVE SUMMARY | MATCH INTELLIGENCE",
    "Databricks Gold Layer Analytics | Tournament Performance, Toss Impact & Venue Scoring"
)
make_slicer(p1_dir, "v02_slicer_venue", 792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue")
make_slicer(p1_dir, "v03_slicer_toss", 1040, 16, 224, 64, 2, 2, "Dim_Toss_Decision", "toss_decision", "Filter Toss Decision")

# Top Row KPI Cards
make_card(p1_dir, "v04_kpi_matches", 16, 96, 300, 100, 3, 3, "_Measures", "Total Matches Analyzed", "Total Matches Analyzed")
make_card(p1_dir, "v05_kpi_toss_win", 332, 96, 300, 100, 4, 4, "_Measures", "Overall Toss Win %", "Overall Toss Win %")
make_card(p1_dir, "v06_kpi_avg_score", 648, 96, 300, 100, 5, 5, "_Measures", "Overall Avg Match Score", "Overall Avg Match Score")
make_card(p1_dir, "v07_kpi_rain_pct", 964, 96, 300, 100, 6, 6, "_Measures", "Rain Impact %", "Rain-Affected Matches (%)")

# Middle Row: Left Clustered Column Chart of Bat vs Field Win %
make_visual_file(
    p1_dir, "v08_chart_toss_win_pct", "columnChart",
    {"x": 16, "y": 212, "z": 7, "width": 616, "height": 240, "tabOrder": 7},
    query_state={
        "Category": {"projections": [make_column_projection("toss stat", "toss_decision")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Overall Toss Win %")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Bat vs. Field Toss Win %'"}}}}}]}
)

# Middle Row: Right Horizontal Bar Chart of Top 10 High-Scoring Venues
make_visual_file(
    p1_dir, "v09_chart_top_venues", "barChart",
    {"x": 648, "y": 212, "z": 8, "width": 616, "height": 240, "tabOrder": 8},
    query_state={
        "Category": {"projections": [make_column_projection("gold venue stats", "venue")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Overall Avg Match Score")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top 10 High-Scoring Venues (Avg Match Score)'"}}}}}]}
)

# Bottom Row: Left Stacked Bar Chart of Rain-Affected vs Clear Matches by Venue
make_visual_file(
    p1_dir, "v10_chart_rain_by_venue", "stackedBarChart",
    {"x": 16, "y": 468, "z": 9, "width": 616, "height": 236, "tabOrder": 9},
    query_state={
        "Category": {"projections": [make_column_projection("Dim_Venue", "venue")]},
        "Y": {"projections": [
            make_measure_projection("_Measures", "Clear Matches"),
            make_measure_projection("_Measures", "Rain Affected Matches")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Rain-Affected vs. Clear Matches by Venue'"}}}}}]}
)

# Bottom Row: Right Top 5 Batters by Total Runs with Strike Rate in Tooltips
make_visual_file(
    p1_dir, "v11_chart_top_batters", "barChart",
    {"x": 648, "y": 468, "z": 10, "width": 616, "height": 236, "tabOrder": 10},
    query_state={
        "Category": {"projections": [make_column_projection("Gold Player phase stats", "batter")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Total Runs")]},
        "Tooltips": {"projections": [make_measure_projection("_Measures", "Weighted Strike Rate")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top Batters by Total Runs (Hover for Strike Rate)'"}}}}}]}
)

# ----------------- PAGE 2: Toss Strategy & Match Outcomes -----------------
p2_dir = os.path.join(pages_dir, "Page2_TossStrategy")
os.makedirs(p2_dir, exist_ok=True)
with open(os.path.join(p2_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "Page2_TossStrategy",
        "displayName": "Toss Strategy & Outcomes",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280
    }, f, indent=2)

make_header_textbox(
    p2_dir, "v01_header",
    "TOSS STRATEGY & MATCH OUTCOMES",
    "Win Conversion by Decision | Comparative Analysis of Batting First vs. Fielding First"
)
make_slicer(p2_dir, "v02_slicer_venue", 792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue")
make_slicer(p2_dir, "v03_slicer_toss", 1040, 16, 224, 64, 2, 2, "Dim_Toss_Decision", "toss_decision", "Filter Toss Decision")

# Top Row: 3 KPI Cards
make_card(p2_dir, "v04_kpi_toss_wins", 16, 96, 405, 100, 3, 3, "_Measures", "Toss Winner Match Wins", "Total Tosses Won")
make_card(p2_dir, "v05_kpi_bat_win_pct", 437, 96, 405, 100, 4, 4, "_Measures", "Bat First Win %", "Bat First Win %")
make_card(p2_dir, "v06_kpi_field_win_pct", 858, 96, 406, 100, 5, 5, "_Measures", "Field First Win %", "Field First Win %")

# Middle Row: Left (40%) Donut Chart comparing Toss Decision Split
make_visual_file(
    p2_dir, "v07_donut_toss_split", "donutChart",
    {"x": 16, "y": 212, "z": 6, "width": 492, "height": 240, "tabOrder": 6},
    query_state={
        "Category": {"projections": [make_column_projection("toss stat", "toss_decision")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Total Toss Matches")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Toss Decision Split (Bat vs Field)'"}}}}}]}
)

# Middle Row: Right (60%) Clustered Bar Chart comparing Total Matches vs Toss Winner Wins
make_visual_file(
    p2_dir, "v08_bar_matches_vs_wins", "barChart",
    {"x": 524, "y": 212, "z": 7, "width": 740, "height": 240, "tabOrder": 7},
    query_state={
        "Category": {"projections": [make_column_projection("toss stat", "toss_decision")]},
        "Y": {"projections": [
            make_measure_projection("_Measures", "Total Toss Matches"),
            make_measure_projection("_Measures", "Toss Winner Match Wins")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Total Matches vs Toss Winner Wins by Toss Decision'"}}}}}]}
)

# Bottom Row: Wide Matrix/Table showing Venue-level Toss Decision breakdown
make_visual_file(
    p2_dir, "v09_matrix_venue_toss", "tableEx",
    {"x": 16, "y": 468, "z": 8, "width": 1248, "height": 236, "tabOrder": 8},
    query_state={
        "Values": {"projections": [
            make_column_projection("Dim_Venue", "venue"),
            make_column_projection("Gold weather impact", "toss_decision"),
            make_measure_projection("_Measures", "Total Matches Analyzed"),
            make_measure_projection("_Measures", "Toss Winner Match Wins"),
            make_measure_projection("_Measures", "Rain Affected Matches")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Venue-Level Toss Decision Breakdown & Match Outcomes'"}}}}}]}
)

# ----------------- PAGE 3: Venue & Weather Intelligence -----------------
p3_dir = os.path.join(pages_dir, "Page3_VenueWeather")
os.makedirs(p3_dir, exist_ok=True)
with open(os.path.join(p3_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "Page3_VenueWeather",
        "displayName": "Venue & Weather Intel",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280
    }, f, indent=2)

make_header_textbox(
    p3_dir, "v01_header",
    "VENUE & WEATHER INTELLIGENCE",
    "Environmental Conditions | Temperature, Thermal Dynamics, Precipitation & Scoring Patterns"
)
make_slicer(p3_dir, "v02_slicer_venue", 792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue")
make_slicer(p3_dir, "v03_slicer_rain", 1040, 16, 224, 64, 2, 2, "Gold weather impact", "is_rain_affected", "Rain Affected (0/1)")

# Top Row: 4 KPI Cards
make_card(p3_dir, "v04_kpi_total_venues", 16, 96, 300, 100, 3, 3, "_Measures", "Total Venues", "Total Venues")
make_card(p3_dir, "v05_kpi_highest_scoring", 332, 96, 300, 100, 4, 4, "_Measures", "Highest Scoring Venue", "Highest Venue Avg Score")
make_card(p3_dir, "v06_kpi_avg_max_temp", 648, 96, 300, 100, 5, 5, "_Measures", "Avg Max Temp (°C)", "Avg Max Temp (°C)")
make_card(p3_dir, "v07_kpi_rain_games", 964, 96, 300, 100, 6, 6, "_Measures", "Rain Affected Matches", "Total Rain-Affected Games")

# Middle Row: Left (55%) Scatter Chart plotting Matches Hosted vs Avg Score per Match
make_visual_file(
    p3_dir, "v08_scatter_hosted_vs_score", "scatterChart",
    {"x": 16, "y": 212, "z": 7, "width": 678, "height": 240, "tabOrder": 7},
    query_state={
        "Category": {"projections": [make_column_projection("gold venue stats", "venue")]},
        "X": {"projections": [make_column_projection("gold venue stats", "matches_hosted", active=False)]},
        "Y": {"projections": [make_column_projection("gold venue stats", "avg_score_per_match", active=False)]},
        "Size": {"projections": [make_column_projection("gold venue stats", "matches_hosted", active=False)]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Matches Hosted vs Avg Score per Match (Sized by Venue Volume)'"}}}}}]}
)

# Middle Row: Right (45%) Combo Chart showing Avg Max Temp and Precipitation
make_visual_file(
    p3_dir, "v09_combo_temp_rain", "lineClusteredColumnComboChart",
    {"x": 710, "y": 212, "z": 8, "width": 554, "height": 240, "tabOrder": 8},
    query_state={
        "Category": {"projections": [make_column_projection("Dim_Venue", "venue")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Avg Max Temp (°C)")]},
        "Y2": {"projections": [make_measure_projection("_Measures", "Avg Precipitation (mm)")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Avg Max Temperature (°C) & Precipitation (mm) across Venues'"}}}}}]}
)

# Bottom Row: Wide Detailed Venue & Weather Table
make_visual_file(
    p3_dir, "v10_table_venue_weather", "tableEx",
    {"x": 16, "y": 468, "z": 9, "width": 1248, "height": 236, "tabOrder": 9},
    query_state={
        "Values": {"projections": [
            make_column_projection("Dim_Venue", "venue"),
            make_column_projection("gold venue stats", "matches_hosted"),
            make_column_projection("gold venue stats", "avg_score_per_match"),
            make_measure_projection("_Measures", "Avg Max Temp (°C)"),
            make_measure_projection("_Measures", "Avg Precipitation (mm)"),
            make_measure_projection("_Measures", "Rain Affected Matches")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Detailed Venue & Weather Data Summary'"}}}}}]}
)

# ----------------- PAGE 4: Player Performance & Phase Analytics -----------------
p4_dir = os.path.join(pages_dir, "Page4_PlayerPerformance")
os.makedirs(p4_dir, exist_ok=True)
with open(os.path.join(p4_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "Page4_PlayerPerformance",
        "displayName": "Player & Phase Analytics",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280
    }, f, indent=2)

make_header_textbox(
    p4_dir, "v01_header",
    "PLAYER PERFORMANCE & PHASE ANALYTICS",
    "Over Phase Breakdown (Powerplay, Middle, Death Overs) | Batting Strike Rates & Boundary Efficiency"
)
make_slicer(p4_dir, "v02_slicer_phase", 792, 16, 232, 64, 1, 1, "Gold Player phase stats", "over_phase", "Over Phase")
make_slicer(p4_dir, "v03_slicer_batter", 1040, 16, 224, 64, 2, 2, "Gold Player phase stats", "batter", "Search Batter")

# Top Row: 4 KPI Cards
make_card(p4_dir, "v04_kpi_total_runs", 16, 96, 300, 100, 3, 3, "_Measures", "Total Runs", "Total Runs")
make_card(p4_dir, "v05_kpi_weighted_sr", 332, 96, 300, 100, 4, 4, "_Measures", "Weighted Strike Rate", "Weighted Strike Rate")
make_card(p4_dir, "v06_kpi_total_boundaries", 648, 96, 300, 100, 5, 5, "_Measures", "Total Boundaries", "Total Boundaries")
make_card(p4_dir, "v07_kpi_death_overs_sr", 964, 96, 300, 100, 6, 6, "_Measures", "Death Overs SR", "Death Overs Strike Rate")

# Middle Row: Left (55%) Clustered Bar Chart of Top 15 Batters
make_visual_file(
    p4_dir, "v08_bar_top_15_batters", "barChart",
    {"x": 16, "y": 212, "z": 7, "width": 678, "height": 240, "tabOrder": 7},
    query_state={
        "Category": {"projections": [make_column_projection("Gold Player phase stats", "batter")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Total Runs")]},
        "Tooltips": {"projections": [
            make_measure_projection("_Measures", "Weighted Strike Rate"),
            make_measure_projection("_Measures", "Total Boundaries")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top Batters by Total Runs (with Strike Rate in Tooltip)'"}}}}}]}
)

# Middle Row: Right (45%) 100% Stacked Bar Chart showing Run Distribution across Phases
make_visual_file(
    p4_dir, "v09_stacked_phase_dist", "hundredPercentStackedBarChart",
    {"x": 710, "y": 212, "z": 8, "width": 554, "height": 240, "tabOrder": 8},
    query_state={
        "Category": {"projections": [make_column_projection("Gold Player phase stats", "batter")]},
        "Series": {"projections": [make_column_projection("Gold Player phase stats", "over_phase")]},
        "Y": {"projections": [make_measure_projection("_Measures", "Total Runs")]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Run Distribution across Powerplay, Middle & Death Overs'"}}}}}]}
)

# Bottom Row: Left (50%) Clustered Column Chart comparing Strike Rate and Boundaries by Phase
make_visual_file(
    p4_dir, "v10_col_phase_sr_boundaries", "columnChart",
    {"x": 16, "y": 468, "z": 9, "width": 616, "height": 236, "tabOrder": 9},
    query_state={
        "Category": {"projections": [make_column_projection("Gold Player phase stats", "over_phase")]},
        "Y": {"projections": [
            make_measure_projection("_Measures", "Weighted Strike Rate"),
            make_measure_projection("_Measures", "Total Boundaries")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Average Strike Rate and Total Boundaries by Over Phase'"}}}}}]}
)

# Bottom Row: Right (50%) Interactive Batter Leaderboard Table
make_visual_file(
    p4_dir, "v11_table_batter_leaderboard", "tableEx",
    {"x": 648, "y": 468, "z": 10, "width": 616, "height": 236, "tabOrder": 10},
    query_state={
        "Values": {"projections": [
            make_column_projection("Gold Player phase stats", "batter"),
            make_column_projection("Gold Player phase stats", "over_phase"),
            make_measure_projection("_Measures", "Total Runs"),
            make_column_projection("Gold Player phase stats", "balls_faced"),
            make_measure_projection("_Measures", "Total Boundaries"),
            make_measure_projection("_Measures", "Weighted Strike Rate")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Interactive Batter Leaderboard & Phase Efficiency'"}}}}}]}
)

# ----------------- TOOLTIP PAGE: Batter Phase Tooltip -----------------
tooltip_dir = os.path.join(pages_dir, "Tooltip_BatterBreakdown")
os.makedirs(tooltip_dir, exist_ok=True)
with open(os.path.join(tooltip_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "Tooltip_BatterBreakdown",
        "displayName": "Batter Phase Tooltip",
        "displayOption": "ActualSize",
        "height": 280,
        "width": 380,
        "visibility": "HiddenInViewMode",
        "type": "Tooltip"
    }, f, indent=2)

make_header_textbox(
    tooltip_dir, "v01_tooltip_title",
    "BATTER OVER-PHASE BREAKDOWN",
    "Hover Intelligence | Runs & Strike Rate Profile"
)
make_visual_file(
    tooltip_dir, "v02_tooltip_chart", "columnChart",
    {"x": 16, "y": 70, "z": 1, "width": 348, "height": 130, "tabOrder": 1},
    query_state={
        "Category": {"projections": [make_column_projection("Gold Player phase stats", "over_phase")]},
        "Y": {"projections": [
            make_measure_projection("_Measures", "Total Runs"),
            make_measure_projection("_Measures", "Weighted Strike Rate")
        ]}
    },
    objects={"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Runs & Strike Rate by Phase'"}}}}}]}
)
make_card(tooltip_dir, "v03_tooltip_kpi_runs", 16, 210, 166, 60, 2, 2, "_Measures", "Total Runs", "Phase Runs")
make_card(tooltip_dir, "v04_tooltip_kpi_sr", 198, 210, 166, 60, 3, 3, "_Measures", "Weighted Strike Rate", "Phase SR")

print("PBIR Report structure successfully written!")
