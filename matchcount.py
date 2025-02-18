from statsbombpy import sb

def count_free_matches():
    # Fetch all competitions
    all_comps = sb.competitions()
    free_competitions = {}
    total_matches = 0

    for _, comp in all_comps.iterrows():
        try:
            # Try to fetch matches for each competition
            matches = sb.matches(competition_id=comp['competition_id'], season_id=comp['season_id'])
            free_competitions[f"{comp['competition_name']} ({comp['season_name']})"] = len(matches)
            total_matches += len(matches)  # Add the number of matches to the total count
            print(f"Accessible: {comp['competition_name']} ({comp['season_name']}) - {len(matches)} matches")
        except Exception as e:
            # If access is denied, print a message and skip
            print(f"Not Accessible: {comp['competition_name']} ({comp['season_name']})")

    # Output results
    print("\nSummary:")
    for competition, match_count in free_competitions.items():
        print(f"{competition}: {match_count} matches")
    print(f"\nTotal Free Competitions: {len(free_competitions)}")
    print(f"Total Free Matches: {total_matches}")

count_free_matches()
