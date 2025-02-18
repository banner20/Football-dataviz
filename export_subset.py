import time
import json
import pandas as pd
import numpy as np
from statsbombpy import sb

def export_subset_bundesliga(output_file="subset_bundesliga2.json"):
    """
    Fetches the 2015/16 season of Bundesliga, filters for Shots & Passes,
    and exports columns needed for Shots, Goals, Passes, and Assists.
    """
    # Fetch all competitions
    competitions = sb.competitions()
    bundesliga_comp = competitions[(competitions['competition_id'] == 9) & (competitions['season_name'] == "2015/2016")]
    
    if bundesliga_comp.empty:
        raise ValueError("No Bundesliga competition found for the 2015/16 season in open data.")

    # Extract competition and season details
    selected = bundesliga_comp.iloc[0]
    comp_id = selected['competition_id']
    season_id = selected['season_id']
    print(f"Processing competition_id={comp_id}, season_id={season_id}")

    # Fetch matches for the specified season
    matches = sb.matches(competition_id=comp_id, season_id=season_id)
    print(f"Found {len(matches)} matches for the 2015/16 season.")

    # Fetch events for all matches
    all_events = []
    for match_id in matches['match_id']:
        print(f"Fetching events for match_id={match_id}")
        events_df = sb.events(match_id=match_id)
        all_events.append(events_df)
        time.sleep(0.2)  # Avoid API rate limiting

    # Combine all match events
    df = pd.concat(all_events, ignore_index=True)
    print(f"Total events fetched: {len(df)}")

    # Keep only Shots & Passes
    df_needed = df[df['type'].isin(['Shot', 'Pass'])].copy()
    print(f"Filtered to {len(df_needed)} events (Shots and Passes).")

    # Specify columns to export
    columns_we_need = [
        'match_id', 'team', 'player', 'type', 'minute', 'second',
        'location', 'shot_end_location', 'shot_outcome',
        'pass_end_location', 'pass_shot_assist'
    ]
    columns_final = [c for c in columns_we_need if c in df_needed.columns]
    df_subset = df_needed[columns_final].copy()
    print(f"Exporting columns: {columns_final}")

    # Replace NaN/Inf with None for JSON compatibility
    df_subset = df_subset.replace([np.nan, np.inf, -np.inf], None)

    # Export to JSON
    records = df_subset.to_dict(orient='records')
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(df_subset)} events to {output_file}.")

if __name__ == "__main__":
    export_subset_bundesliga("subset_bundesliga2.json")
