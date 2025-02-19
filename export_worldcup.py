import time
import json
import pandas as pd
import numpy as np
from statsbombpy import sb

def export_subset_worldcup_2018(output_file="subset_worldcup2018.json"):
    """
    Fetches the 2018 FIFA World Cup data, filters for Shots & Passes,
    and exports columns needed for Shots, Goals, Passes, and Assists.
    """
    # 1) Fetch all competitions
    competitions = sb.competitions()
    # Filter for FIFA World Cup (competition_id=43) and season_name="2018"
    worldcup_comp = competitions[
        (competitions['competition_id'] == 43) &
        (competitions['season_name'] == "2018")
    ]
    
    if worldcup_comp.empty:
        raise ValueError("No 2018 FIFA World Cup competition found in open data.")

    # 2) Extract competition and season details
    selected = worldcup_comp.iloc[0]
    comp_id = selected['competition_id']
    season_id = selected['season_id']
    print(f"Processing competition_id={comp_id}, season_id={season_id} (2018 FIFA World Cup)")

    # 3) Fetch matches for the specified season
    matches = sb.matches(competition_id=comp_id, season_id=season_id)
    print(f"Found {len(matches)} matches for the 2018 World Cup.")

    # 4) Fetch events for all matches
    all_events = []
    for match_id in matches['match_id']:
        print(f"Fetching events for match_id={match_id}")
        events_df = sb.events(match_id=match_id)
        all_events.append(events_df)
        time.sleep(0.2)  # Avoid API rate limiting

    # 5) Combine all match events
    df = pd.concat(all_events, ignore_index=True)
    print(f"Total events fetched: {len(df)}")

    # 6) Keep only Shots & Passes
    df_needed = df[df['type'].isin(['Shot', 'Pass'])].copy()
    print(f"Filtered to {len(df_needed)} events (Shots and Passes).")

    # 7) Specify columns to export
    columns_we_need = [
        'match_id', 'team', 'player', 'type', 'minute', 'second',
        'location', 'shot_end_location', 'shot_outcome',
        'pass_end_location', 'pass_shot_assist'
    ]
    columns_final = [c for c in columns_we_need if c in df_needed.columns]
    df_subset = df_needed[columns_final].copy()
    print(f"Exporting columns: {columns_final}")

    # 8) Replace NaN/Inf with None for JSON compatibility
    df_subset = df_subset.replace([np.nan, np.inf, -np.inf], None)

    # 9) Export to JSON
    records = df_subset.to_dict(orient='records')
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(df_subset)} events to {output_file}.")

if __name__ == "__main__":
    export_subset_worldcup_2018("subset_worldcup2018.json")
