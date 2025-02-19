import time
import json
import pandas as pd
import numpy as np
from statsbombpy import sb

def export_euro_2024_subset(output_file="subset_euro_2024.json"):
    """
    Fetches only the columns we need from StatsBomb open data
    for the UEFA Euro 2024 competition, if it exists in open data.

    Note: If 'UEFA Euro 2024' doesn't exist in the open data feed,
    this will raise a ValueError. Adjust competition/season names if needed.
    """

    # 1) Desired columns from your earlier list. If any don't exist in the data, they'll be skipped.
    columns_we_need = [
        "id", "index", "match_id", "team", "team_id", "player", "player_id",
        "type", "minute", "second", "period", "duration", "timestamp",
        "possession", "possession_team", "possession_team_id",
        "location", "shot_end_location", "shot_outcome", "shot_statsbomb_xg",
        "shot_aerial_won", "shot_body_part", "shot_technique", "shot_type",
        "shot_deflected", "shot_open_goal", "pass_end_location", "pass_shot_assist",
        "pass_goal_assist", "pass_deflected", "pass_cut_back", "pass_switch",
        "pass_through_ball", "pass_outcome", "pass_technique", "pass_type",
        "pass_aerial_won", "pass_assisted_shot_id", "dribble_outcome", "dribble_no_touch",
        "duel_outcome", "duel_type", "foul_committed_type", "foul_committed_advantage",
        "foul_committed_card", "foul_committed_penalty", "foul_won_advantage",
        "foul_won_penalty", "ball_recovery_offensive", "ball_recovery_recovery_failure",
        "counterpress", "goalkeeper_outcome", "goalkeeper_position", "goalkeeper_type",
        "goalkeeper_body_part", "goalkeeper_end_location", "under_pressure", "play_pattern",
        "bad_behaviour_card", "50_50", "tactics", "position"
    ]

    # 2) Fetch competitions and filter for UEFA Euro 2024
    competitions = sb.competitions()
    euro_comp = competitions[
        (competitions['competition_name'] == "UEFA Euro") &
        (competitions['season_name'] == "2024")
    ]
    if euro_comp.empty:
        raise ValueError("No UEFA Euro 2024 competition found in open data.")

    selected = euro_comp.iloc[0]
    comp_id = selected['competition_id']
    season_id = selected['season_id']
    print(f"Processing UEFA Euro 2024 => competition_id={comp_id}, season_id={season_id}")

    # 3) Fetch matches
    matches = sb.matches(competition_id=comp_id, season_id=season_id)
    print(f"Found {len(matches)} matches for UEFA Euro 2024.")

    # 4) Collect event data for each match
    all_events = []
    for match_id in matches['match_id']:
        print(f"Fetching events for match_id={match_id}")
        events_df = sb.events(match_id=match_id)
        # Optionally ensure 'match_id' column is present
        events_df['match_id'] = match_id
        all_events.append(events_df)
        time.sleep(0.2)  # courtesy sleep

    # 5) Combine into one DataFrame
    df = pd.concat(all_events, ignore_index=True)
    print(f"Total events fetched: {len(df)}")

    # 6) Keep only the columns we need (skip any that don't exist)
    columns_final = [c for c in columns_we_need if c in df.columns]
    df_needed = df[columns_final].copy()
    print(f"Keeping {len(columns_final)} columns out of {len(columns_we_need)} requested.")

    # 7) Replace NaN/Inf with None for JSON compatibility
    df_needed = df_needed.replace([np.nan, np.inf, -np.inf], None)

    # 8) Export to JSON
    records = df_needed.to_dict(orient='records')
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(records)} events to {output_file}.")

if __name__ == "__main__":
    export_euro_2024_subset("subset_euro_2024.json")
