import time
import pandas as pd
from statsbombpy import sb

def inspect_euro_and_copa_2024():
    """
    Fetches only Copa America 2024 and UEFA Euro 2024 from open data,
    collects unique columns from all matches' event data, and prints them.
    """
    all_columns = set()

    # 1) Fetch all open-data competitions
    competitions = sb.competitions()
    print(f"Total competitions found: {len(competitions)}")

    # 2) Filter for Copa America 2024 and UEFA Euro 2024
    # Adjust the names below if they differ in sb.competitions().
    relevant_comps = competitions[
        (
            (competitions['competition_name'] == "Copa America") &
            (competitions['season_name'] == "2024")
        ) |
        (
            (competitions['competition_name'] == "UEFA Euro") &
            (competitions['season_name'] == "2024")
        )
    ]

    if relevant_comps.empty:
        print("No matching competitions found for Copa America 2024 or UEFA Euro 2024.")
        return

    # 3) For each relevant competition, fetch matches & events
    for idx, comp in relevant_comps.iterrows():
        comp_id = comp['competition_id']
        season_id = comp['season_id']
        comp_name = comp['competition_name']
        season_name = comp['season_name']

        print(f"Processing: {comp_name} ({season_name}), comp_id={comp_id}, season_id={season_id}")
        try:
            matches = sb.matches(competition_id=comp_id, season_id=season_id)
            print(f"Found {len(matches)} matches.")

            for match_id in matches['match_id']:
                try:
                    events_df = sb.events(match_id=match_id)
                    all_columns.update(events_df.columns)
                    time.sleep(0.1)  # Rate limit courtesy
                except Exception as e:
                    print(f"   Error fetching events for match_id={match_id}: {e}")

        except Exception as e:
            print(f"   Error fetching matches for {comp_name} ({season_name}): {e}")

    # 4) Print unique columns
    print("\n========================================")
    print("Unique columns found in Copa America 2024 & UEFA Euro 2024:\n")
    sorted_cols = sorted(all_columns)
    for col in sorted_cols:
        print(col)

    print(f"\nTotal unique columns: {len(all_columns)}")


if __name__ == "__main__":
    inspect_euro_and_copa_2024()
