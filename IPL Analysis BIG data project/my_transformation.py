#important imports
from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col, input_file_name, regexp_extract, to_date, year, 
    when, sum, count, round
)
import os
import json

# ==========================================
# 1. BRONZE LAYER
# ==========================================
@dp.table(name="bronze_match_info")
def bronze_match_info():
    DATA_DIR = "/Volumes/workspace/default/ipl_raw/ipl_male_json"
    files = [f"{DATA_DIR}/{fname}" for fname in sorted(os.listdir(DATA_DIR)) if fname.endswith(".json")]
    
    match_info_rows = []
    for fpath in files:
        local_path = fpath.replace("dbfs:/", "/dbfs/") if "dbfs:/" in fpath else fpath
        with open(local_path, "r") as f:
            d = json.load(f)
        
        match_id = os.path.basename(fpath).replace(".json", "")
        info = d.get("info", {})
        
        match_info_rows.append({
            "match_id": match_id,
            "venue": info.get("venue"),
            "city": info.get("city"),
            "match_date": info.get("dates", [None])[0],
            "team_1": info.get("teams", [None, None])[0] if info.get("teams") else None,
            "team_2": info.get("teams", [None, None])[1] if info.get("teams") and len(info.get("teams")) > 1 else None,
            "toss_winner": info.get("toss", {}).get("winner"),
            "toss_decision": info.get("toss", {}).get("decision"),
            "winner": info.get("outcome", {}).get("winner"),
            "event_name": info.get("event", {}).get("name"),
            "season": info.get("season")
        })
    return spark.createDataFrame(match_info_rows)

@dp.table(name="bronze_deliveries")
def bronze_deliveries():
    DATA_DIR = "/Volumes/workspace/default/ipl_raw/ipl_male_json"
    files = [f"{DATA_DIR}/{fname}" for fname in sorted(os.listdir(DATA_DIR)) if fname.endswith(".json")]

    delivery_rows = []
    for fpath in files:
        local_path = fpath.replace("dbfs:/", "/dbfs/") if "dbfs:/" in fpath else fpath
        with open(local_path, "r") as f:
            d = json.load(f)
            
        match_id = os.path.basename(fpath).replace(".json", "")
        info = d.get("info", {})
        match_date = info.get("dates", [None])[0]
        venue = info.get("venue")
        
        for inn_idx, inn in enumerate(d.get("innings", [])):
            batting_team = inn.get("team")
            for over in inn.get("overs", []):
                over_no = over.get("over")
                for ball_idx, ball in enumerate(over.get("deliveries", [])):
                    runs = ball.get("runs", {})
                    extras = ball.get("extras", {}) or {}
                    wickets = ball.get("wickets", []) or []
                    
                    delivery_rows.append({
                        "match_id": match_id,
                        "match_date": match_date,
                        "venue": venue,
                        "innings_no": inn_idx + 1,
                        "batting_team": batting_team,
                        "over_no": over_no + 1, 
                        "ball_in_over": ball_idx + 1,
                        "batter": ball.get("batter"),
                        "bowler": ball.get("bowler"),
                        "non_striker": ball.get("non_striker"),
                        "runs_batter": runs.get("batter", 0),
                        "runs_extras": runs.get("extras", 0),
                        "runs_total": runs.get("total", 0),
                        "extra_wides": extras.get("wides", 0),
                        "extra_noballs": extras.get("noballs", 0),
                        "is_wicket": 1 if wickets else 0,
                        "wicket_kind": wickets[0].get("kind") if wickets else None,
                        "player_out": wickets[0].get("player_out") if wickets else None
                    })
    return spark.createDataFrame(delivery_rows)

# ==========================================
# 2. SILVER LAYER
# ==========================================
@dp.table(name="silver_match_info")
def silver_match_info():
    return (
        spark.read.table("bronze_match_info")
        .withColumn("match_date", to_date(col("match_date"), "yyyy-MM-dd"))
        .withColumn("season_year", year(col("match_date")))
        .withColumn("season", 
                    when(col("season").isNull(), col("season_year").cast("string"))
                    .otherwise(col("season")))
        .dropDuplicates(["match_id"])
    )

@dp.table(name="silver_deliveries")
def silver_deliveries():
    return (
        spark.read.table("bronze_deliveries")
        .withColumn("over_phase", 
                    when(col("over_no") <= 6, "Powerplay")
                    .when((col("over_no") > 6) & (col("over_no") <= 15), "Middle Overs")
                    .otherwise("Death Overs"))
        .withColumn("is_boundary", when(col("runs_batter").isin(4, 6), 1).otherwise(0))
        .filter(col("batter").isNotNull() & col("bowler").isNotNull())
    )

# ==========================================
# 3. GOLD LAYER
# ==========================================
@dp.materialized_view(name="gold_toss_impact")
def gold_toss_impact():
    df_info = spark.read.table("silver_match_info")
    df_toss = df_info.withColumn("toss_winner_won_match", when(col("toss_winner") == col("winner"), 1).otherwise(0))
    
    return (
        df_toss.groupBy("toss_decision")
        .agg(
            count("*").alias("total_matches"),
            sum("toss_winner_won_match").alias("toss_winner_wins"),
            round((sum("toss_winner_won_match") / count("*")) * 100, 2).alias("win_percentage")
        )
    )

@dp.materialized_view(name="gold_venue_stats")
def gold_venue_stats():
    df_deliveries = spark.read.table("silver_deliveries")
    df_match_scores = df_deliveries.groupBy("match_id", "venue").agg(sum("runs_total").alias("match_total_runs"))
    
    return (
        df_match_scores.groupBy("venue")
        .agg(
            count("match_id").alias("matches_hosted"),
            round(sum("match_total_runs") / count("match_id"), 2).alias("avg_score_per_match")
        )
        .orderBy(col("matches_hosted").desc())
    )

@dp.materialized_view(name="gold_player_phase_stats")
def gold_player_phase_stats():
    df_deliveries = spark.read.table("silver_deliveries")
    
    return (
        df_deliveries.filter(col("extra_wides") == 0)
        .groupBy("batter", "over_phase")
        .agg(
            sum("runs_batter").alias("total_runs"),
            count("*").alias("balls_faced"),
            sum("is_boundary").alias("total_boundaries")
        )
        .withColumn("strike_rate", round((col("total_runs") / col("balls_faced")) * 100, 2))
        .filter(col("balls_faced") > 100)
        .orderBy(col("strike_rate").desc())
    )
    # ==========================================
# 5. WEATHER LAYER (Silver & Gold)
# ==========================================

@dp.table(name="silver_weather")
def silver_weather():
    return (
        spark.read.table("bronze_weather")
        .withColumn("match_date", to_date(col("match_date"), "yyyy-MM-dd"))
    )
@dp.materialized_view(name="gold_weather_impact")
def gold_weather_impact():
    df_matches = spark.read.table("silver_match_info")
    df_weather = spark.read.table("silver_weather")
    
    # Weather table se sirf zaroori columns select kar rahe hain (duplicate venue/date hatane ke liye)
    df_weather_clean = df_weather.select("match_id", "temp_max", "temp_min", "precipitation", "wind_speed_max")
    
    # Ab join karenge
    df_joined = df_matches.join(df_weather_clean, on="match_id", how="inner")
    
    return (
        df_joined
        .withColumn("is_rain_affected", when(col("precipitation") > 0.5, 1).otherwise(0))
        .select("match_id", "venue", "match_date", "toss_decision", "winner", 
                "temp_max", "temp_min", "precipitation", "wind_speed_max", "is_rain_affected")
    )