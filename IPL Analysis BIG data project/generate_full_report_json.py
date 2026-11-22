import os
import json
import uuid

BASE_DIR = r"C:\Users\swast\Documents\IPL Analysis BIG data project"
REPORT_DIR = os.path.join(BASE_DIR, "IPL_Analytics_Dashboard.Report")
REPORT_JSON_PATH = os.path.join(REPORT_DIR, "report.json")
DEF_PBIR_PATH = os.path.join(REPORT_DIR, "definition.pbir")

def new_id():
    return uuid.uuid4().hex[:20]

def make_proto_query(entities_and_fields):
    """
    entities_and_fields: list of tuples: (table, field_name, is_measure)
    """
    tables = {}
    for table, field_name, is_measure in entities_and_fields:
        if table not in tables:
            tables[table] = f"t_{len(tables)}"

    from_list = []
    for table, alias in tables.items():
        from_list.append({
            "Name": alias,
            "Entity": table,
            "Type": 0
        })

    select_list = []
    for table, field_name, is_measure in entities_and_fields:
        alias = tables[table]
        prop_kind = "Measure" if is_measure else "Column"
        select_list.append({
            prop_kind: {
                "Expression": {
                    "SourceRef": {
                        "Source": alias
                    }
                },
                "Property": field_name
            },
            "Name": f"{table}.{field_name}",
            "NativeReferenceName": field_name
        })

    return {
        "Version": 2,
        "From": from_list,
        "Select": select_list
    }

def make_container(x, y, width, height, z, tab_order, single_visual):
    vis_name = new_id()
    config_dict = {
        "name": vis_name,
        "layouts": [
            {
                "id": 0,
                "position": {
                    "x": float(x),
                    "y": float(y),
                    "z": int(z),
                    "width": float(width),
                    "height": float(height),
                    "tabOrder": int(tab_order)
                }
            }
        ],
        "singleVisual": single_visual
    }
    return {
        "x": float(x),
        "y": float(y),
        "z": int(z),
        "width": float(width),
        "height": float(height),
        "config": json.dumps(config_dict),
        "filters": "[]"
    }

def make_header_container(title, subtitle):
    vis = {
        "visualType": "textbox",
        "objects": {
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
    }
    return make_container(16, 16, 760, 64, 0, 0, vis)

def make_slicer_container(x, y, width, height, z, tab_order, table, column, title):
    proto = make_proto_query([(table, column, False)])
    vis = {
        "visualType": "slicer",
        "projections": {
            "Values": [
                {"queryRef": f"{table}.{column}", "active": True}
            ]
        },
        "prototypeQuery": proto,
        "objects": {
            "general": [
                {
                    "properties": {
                        "title": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }
            ]
        }
    }
    return make_container(x, y, width, height, z, tab_order, vis)

def make_card_container(x, y, width, height, z, tab_order, table, measure, title):
    proto = make_proto_query([(table, measure, True)])
    vis = {
        "visualType": "card",
        "projections": {
            "Values": [
                {"queryRef": f"{table}.{measure}"}
            ]
        },
        "prototypeQuery": proto,
        "objects": {
            "general": [
                {
                    "properties": {
                        "title": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }
            ]
        }
    }
    return make_container(x, y, width, height, z, tab_order, vis)

# Page 1: Executive Summary
p1_containers = [
    make_header_container("IPL EXECUTIVE SUMMARY | MATCH INTELLIGENCE", "Databricks Gold Layer Analytics | Tournament Performance, Toss Decisions & Venue Scoring"),
    make_slicer_container(792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue"),
    make_slicer_container(1040, 16, 224, 64, 2, 2, "Dim_Toss_Decision", "toss_decision", "Filter Toss Decision"),
    # KPIs
    make_card_container(16, 96, 300, 100, 3, 3, "_Measures", "Total Matches Analyzed", "Total Matches Analyzed"),
    make_card_container(332, 96, 300, 100, 4, 4, "_Measures", "Overall Toss Win %", "Overall Toss Win %"),
    make_card_container(648, 96, 300, 100, 5, 5, "_Measures", "Overall Avg Match Score", "Overall Avg Match Score"),
    make_card_container(964, 96, 300, 100, 6, 6, "_Measures", "Rain Impact %", "Rain-Affected Matches (%)"),
    # Middle: Left Clustered Column Chart Bat vs Field Win %
    make_container(16, 212, 616, 240, 7, 7, {
        "visualType": "columnChart",
        "projections": {
            "Category": [{"queryRef": "toss stat.toss_decision", "active": True}],
            "Y": [{"queryRef": "_Measures.Overall Toss Win %"}]
        },
        "prototypeQuery": make_proto_query([("toss stat", "toss_decision", False), ("_Measures", "Overall Toss Win %", True)]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Bat vs. Field Toss Win %'"}}}}}]}
    }),
    # Middle: Right Top 10 High-Scoring Venues
    make_container(648, 212, 616, 240, 8, 8, {
        "visualType": "barChart",
        "projections": {
            "Category": [{"queryRef": "gold venue stats.venue", "active": True}],
            "Y": [{"queryRef": "_Measures.Overall Avg Match Score"}]
        },
        "prototypeQuery": make_proto_query([("gold venue stats", "venue", False), ("_Measures", "Overall Avg Match Score", True)]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top 10 High-Scoring Venues (Avg Match Score)'"}}}}}]}
    }),
    # Bottom: Left Rain-Affected vs Clear Matches by Venue
    make_container(16, 468, 616, 236, 9, 9, {
        "visualType": "stackedBarChart",
        "projections": {
            "Category": [{"queryRef": "Dim_Venue.venue", "active": True}],
            "Y": [
                {"queryRef": "_Measures.Clear Matches"},
                {"queryRef": "_Measures.Rain Affected Matches"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Dim_Venue", "venue", False),
            ("_Measures", "Clear Matches", True),
            ("_Measures", "Rain Affected Matches", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Rain-Affected vs. Clear Matches by Venue'"}}}}}]}
    }),
    # Bottom: Right Top Batters by Total Runs
    make_container(648, 468, 616, 236, 10, 10, {
        "visualType": "barChart",
        "projections": {
            "Category": [{"queryRef": "Gold Player phase stats.batter", "active": True}],
            "Y": [{"queryRef": "_Measures.Total Runs"}],
            "Tooltips": [{"queryRef": "_Measures.Weighted Strike Rate"}]
        },
        "prototypeQuery": make_proto_query([
            ("Gold Player phase stats", "batter", False),
            ("_Measures", "Total Runs", True),
            ("_Measures", "Weighted Strike Rate", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top Batters by Total Runs (Hover for Strike Rate)'"}}}}}]}
    })
]

# Page 2: Toss Strategy & Match Outcomes
p2_containers = [
    make_header_container("TOSS STRATEGY & MATCH OUTCOMES", "Win Conversion by Decision | Comparative Analysis of Batting First vs. Fielding First"),
    make_slicer_container(792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue"),
    make_slicer_container(1040, 16, 224, 64, 2, 2, "Dim_Toss_Decision", "toss_decision", "Filter Toss Decision"),
    make_card_container(16, 96, 405, 100, 3, 3, "_Measures", "Toss Winner Match Wins", "Total Tosses Won"),
    make_card_container(437, 96, 405, 100, 4, 4, "_Measures", "Bat First Win %", "Bat First Win %"),
    make_card_container(858, 96, 406, 100, 5, 5, "_Measures", "Field First Win %", "Field First Win %"),
    # Donut
    make_container(16, 212, 492, 240, 6, 6, {
        "visualType": "donutChart",
        "projections": {
            "Category": [{"queryRef": "toss stat.toss_decision", "active": True}],
            "Y": [{"queryRef": "_Measures.Total Toss Matches"}]
        },
        "prototypeQuery": make_proto_query([("toss stat", "toss_decision", False), ("_Measures", "Total Toss Matches", True)]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Toss Decision Split (Bat vs Field)'"}}}}}]}
    }),
    # Bar Total vs Wins
    make_container(524, 212, 740, 240, 7, 7, {
        "visualType": "barChart",
        "projections": {
            "Category": [{"queryRef": "toss stat.toss_decision", "active": True}],
            "Y": [
                {"queryRef": "_Measures.Total Toss Matches"},
                {"queryRef": "_Measures.Toss Winner Match Wins"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("toss stat", "toss_decision", False),
            ("_Measures", "Total Toss Matches", True),
            ("_Measures", "Toss Winner Match Wins", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Total Matches vs Toss Winner Wins by Toss Decision'"}}}}}]}
    }),
    # Wide Matrix / Table
    make_container(16, 468, 1248, 236, 8, 8, {
        "visualType": "tableEx",
        "projections": {
            "Values": [
                {"queryRef": "Dim_Venue.venue"},
                {"queryRef": "Gold weather impact.toss_decision"},
                {"queryRef": "_Measures.Total Matches Analyzed"},
                {"queryRef": "_Measures.Toss Winner Match Wins"},
                {"queryRef": "_Measures.Rain Affected Matches"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Dim_Venue", "venue", False),
            ("Gold weather impact", "toss_decision", False),
            ("_Measures", "Total Matches Analyzed", True),
            ("_Measures", "Toss Winner Match Wins", True),
            ("_Measures", "Rain Affected Matches", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Venue-Level Toss Decision Breakdown & Match Outcomes'"}}}}}]}
    })
]

# Page 3: Venue & Weather Intelligence
p3_containers = [
    make_header_container("VENUE & WEATHER INTELLIGENCE", "Environmental Conditions | Temperature, Thermal Dynamics, Precipitation & Scoring Patterns"),
    make_slicer_container(792, 16, 232, 64, 1, 1, "Dim_Venue", "venue", "Filter by Venue"),
    make_slicer_container(1040, 16, 224, 64, 2, 2, "Gold weather impact", "is_rain_affected", "Rain Affected (0/1)"),
    make_card_container(16, 96, 300, 100, 3, 3, "_Measures", "Total Venues", "Total Venues"),
    make_card_container(332, 96, 300, 100, 4, 4, "_Measures", "Highest Scoring Venue", "Highest Venue Avg Score"),
    make_card_container(648, 96, 300, 100, 5, 5, "_Measures", "Avg Max Temp (°C)", "Avg Max Temp (°C)"),
    make_card_container(964, 96, 300, 100, 6, 6, "_Measures", "Rain Affected Matches", "Total Rain-Affected Games"),
    # Scatter
    make_container(16, 212, 678, 240, 7, 7, {
        "visualType": "scatterChart",
        "projections": {
            "Category": [{"queryRef": "gold venue stats.venue", "active": True}],
            "X": [{"queryRef": "gold venue stats.matches_hosted"}],
            "Y": [{"queryRef": "gold venue stats.avg_score_per_match"}],
            "Size": [{"queryRef": "gold venue stats.matches_hosted"}]
        },
        "prototypeQuery": make_proto_query([
            ("gold venue stats", "venue", False),
            ("gold venue stats", "matches_hosted", False),
            ("gold venue stats", "avg_score_per_match", False)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Matches Hosted vs Avg Score per Match (Sized by Venue Volume)'"}}}}}]}
    }),
    # Combo
    make_container(710, 212, 554, 240, 8, 8, {
        "visualType": "lineClusteredColumnComboChart",
        "projections": {
            "Category": [{"queryRef": "Dim_Venue.venue", "active": True}],
            "Y": [{"queryRef": "_Measures.Avg Max Temp (°C)"}],
            "Y2": [{"queryRef": "_Measures.Avg Precipitation (mm)"}]
        },
        "prototypeQuery": make_proto_query([
            ("Dim_Venue", "venue", False),
            ("_Measures", "Avg Max Temp (°C)", True),
            ("_Measures", "Avg Precipitation (mm)", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Avg Max Temperature (°C) & Precipitation (mm) across Venues'"}}}}}]}
    }),
    # Detailed Table
    make_container(16, 468, 1248, 236, 9, 9, {
        "visualType": "tableEx",
        "projections": {
            "Values": [
                {"queryRef": "Dim_Venue.venue"},
                {"queryRef": "gold venue stats.matches_hosted"},
                {"queryRef": "gold venue stats.avg_score_per_match"},
                {"queryRef": "_Measures.Avg Max Temp (°C)"},
                {"queryRef": "_Measures.Avg Precipitation (mm)"},
                {"queryRef": "_Measures.Rain Affected Matches"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Dim_Venue", "venue", False),
            ("gold venue stats", "matches_hosted", False),
            ("gold venue stats", "avg_score_per_match", False),
            ("_Measures", "Avg Max Temp (°C)", True),
            ("_Measures", "Avg Precipitation (mm)", True),
            ("_Measures", "Rain Affected Matches", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Detailed Venue & Weather Data Summary'"}}}}}]}
    })
]

# Page 4: Player Performance & Phase Analytics
p4_containers = [
    make_header_container("PLAYER PERFORMANCE & PHASE ANALYTICS", "Over Phase Breakdown (Powerplay, Middle, Death Overs) | Batting Strike Rates & Boundary Efficiency"),
    make_slicer_container(792, 16, 232, 64, 1, 1, "Gold Player phase stats", "over_phase", "Over Phase"),
    make_slicer_container(1040, 16, 224, 64, 2, 2, "Gold Player phase stats", "batter", "Search Batter"),
    make_card_container(16, 96, 300, 100, 3, 3, "_Measures", "Total Runs", "Total Runs"),
    make_card_container(332, 96, 300, 100, 4, 4, "_Measures", "Weighted Strike Rate", "Weighted Strike Rate"),
    make_card_container(648, 96, 300, 100, 5, 5, "_Measures", "Total Boundaries", "Total Boundaries"),
    make_card_container(964, 96, 300, 100, 6, 6, "_Measures", "Death Overs SR", "Death Overs Strike Rate"),
    # Top 15 Batters
    make_container(16, 212, 678, 240, 7, 7, {
        "visualType": "barChart",
        "projections": {
            "Category": [{"queryRef": "Gold Player phase stats.batter", "active": True}],
            "Y": [{"queryRef": "_Measures.Total Runs"}],
            "Tooltips": [
                {"queryRef": "_Measures.Weighted Strike Rate"},
                {"queryRef": "_Measures.Total Boundaries"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Gold Player phase stats", "batter", False),
            ("_Measures", "Total Runs", True),
            ("_Measures", "Weighted Strike Rate", True),
            ("_Measures", "Total Boundaries", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Top Batters by Total Runs (with Strike Rate in Tooltip)'"}}}}}]}
    }),
    # 100% Stacked Bar
    make_container(710, 212, 554, 240, 8, 8, {
        "visualType": "hundredPercentStackedBarChart",
        "projections": {
            "Category": [{"queryRef": "Gold Player phase stats.batter", "active": True}],
            "Series": [{"queryRef": "Gold Player phase stats.over_phase", "active": True}],
            "Y": [{"queryRef": "_Measures.Total Runs"}]
        },
        "prototypeQuery": make_proto_query([
            ("Gold Player phase stats", "batter", False),
            ("Gold Player phase stats", "over_phase", False),
            ("_Measures", "Total Runs", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Run Distribution across Powerplay, Middle & Death Overs'"}}}}}]}
    }),
    # Column Phase SR & Boundaries
    make_container(16, 468, 616, 236, 9, 9, {
        "visualType": "columnChart",
        "projections": {
            "Category": [{"queryRef": "Gold Player phase stats.over_phase", "active": True}],
            "Y": [
                {"queryRef": "_Measures.Weighted Strike Rate"},
                {"queryRef": "_Measures.Total Boundaries"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Gold Player phase stats", "over_phase", False),
            ("_Measures", "Weighted Strike Rate", True),
            ("_Measures", "Total Boundaries", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Average Strike Rate and Total Boundaries by Over Phase'"}}}}}]}
    }),
    # Batter Leaderboard Table
    make_container(648, 468, 616, 236, 10, 10, {
        "visualType": "tableEx",
        "projections": {
            "Values": [
                {"queryRef": "Gold Player phase stats.batter"},
                {"queryRef": "Gold Player phase stats.over_phase"},
                {"queryRef": "_Measures.Total Runs"},
                {"queryRef": "Gold Player phase stats.balls_faced"},
                {"queryRef": "_Measures.Total Boundaries"},
                {"queryRef": "_Measures.Weighted Strike Rate"}
            ]
        },
        "prototypeQuery": make_proto_query([
            ("Gold Player phase stats", "batter", False),
            ("Gold Player phase stats", "over_phase", False),
            ("_Measures", "Total Runs", True),
            ("Gold Player phase stats", "balls_faced", False),
            ("_Measures", "Total Boundaries", True),
            ("_Measures", "Weighted Strike Rate", True)
        ]),
        "objects": {"general": [{"properties": {"title": {"expr": {"Literal": {"Value": "'Interactive Batter Leaderboard & Phase Efficiency'"}}}}}]}
    })
]

sections = [
    {
        "name": "Section_ExecutiveSummary",
        "displayName": "Executive Summary",
        "filters": "[]",
        "ordinal": 0,
        "width": 1280.0,
        "height": 720.0,
        "config": "{}",
        "visualContainers": p1_containers
    },
    {
        "name": "Section_TossStrategy",
        "displayName": "Toss Strategy & Outcomes",
        "filters": "[]",
        "ordinal": 1,
        "width": 1280.0,
        "height": 720.0,
        "config": "{}",
        "visualContainers": p2_containers
    },
    {
        "name": "Section_VenueWeather",
        "displayName": "Venue & Weather Intel",
        "filters": "[]",
        "ordinal": 2,
        "width": 1280.0,
        "height": 720.0,
        "config": "{}",
        "visualContainers": p3_containers
    },
    {
        "name": "Section_PlayerPerformance",
        "displayName": "Player & Phase Analytics",
        "filters": "[]",
        "ordinal": 3,
        "width": 1280.0,
        "height": 720.0,
        "config": "{}",
        "visualContainers": p4_containers
    }
]

report_dict = {
    "config": json.dumps({
        "version": "5.57",
        "themeCollection": {
            "customTheme": {
                "name": "IPL_Dark_Analytics",
                "reportVersionAtImport": "5.57",
                "type": "RegisteredResources"
            }
        },
        "activeSectionIndex": 0,
        "defaultDrillFilterOtherVisuals": True,
        "settings": {
            "useNewFilterPaneExperience": True,
            "allowChangeFilterTypes": True,
            "useStylableVisualContainerHeader": True
        }
    }),
    "layoutOptimization": 0,
    "theme": "IPL_Dark_Analytics",
    "sections": sections
}

# Write root report.json
with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(report_dict, f, indent=2)
print("Wrote IPL_Analytics_Dashboard.Report/report.json successfully!")

# Write definition/report.json as well
def_report_path = os.path.join(REPORT_DIR, "definition", "report.json")
with open(def_report_path, "w", encoding="utf-8") as f:
    json.dump(report_dict, f, indent=2)
print("Wrote definition/report.json successfully!")

# Ensure definition.pbir supports standard PBIP version 1.0 (so Desktop opens report.json without requiring preview toggle)
pbir_content = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": "../IPL_Analytics_Dashboard.SemanticModel"
        },
        "byConnection": None
    }
}
with open(DEF_PBIR_PATH, "w", encoding="utf-8") as f:
    json.dump(pbir_content, f, indent=2)
print("Updated definition.pbir to version 1.0 successfully!")
