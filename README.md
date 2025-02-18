# Football-dataviz
# Football Visualization Project

This project demonstrates how to:
1. **Fetch** open‐data match events from the StatsBombPy library for a specific competition/season (e.g., Bundesliga 2015/16).
2. **Filter** event data to only include shots and passes, and export the resulting dataset to a JSON file.
3. **Visualize** the data in a web interface:
   - A realistic football pitch rendered via D3.js
   - Interactive toggles (checkboxes) for Shots, Goals, Passes, Assists, and directional arrows
   - Team and Player dropdowns to filter the data
   - **Top scoring players** and **top scoring teams** displayed in a clickable list below the pitch

## Project Structure

## Data Pipeline

1. **StatsBombPy**  
   - We use `sb.competitions()` to find the desired competition/season.  
   - We then use `sb.matches()` to fetch match IDs for that competition/season.  
   - Finally, `sb.events()` to get the event data for each match, merging them into one DataFrame.

2. **Filtering**  
   - Only keep rows where `type` is `"Shot"` or `"Pass"`.  
   - Export columns like `shot_outcome`, `location`, `pass_end_location`, etc.  
   - Convert `NaN` to `None` for JSON compatibility.

3. **Front-End Visualization**  
   - An **HTML** file with embedded **D3.js** code.  
   - Renders a pitch with lines (center circle, penalty boxes, goals).  
   - Draws circles/lines for Shots, Goals, Passes, Assists.  
   - Toggles for each category plus directional lines.  
   - Team and Player dropdowns to filter data.  
   - **Top scoring players** and **teams** are displayed below the pitch, each clickable to filter the pitch to that player/team’s goals.

## Usage

1. **Install Dependencies**  
   ```bash
   pip install statsbombpy

Fetch Data

Run the Python script (e.g., fetch_data.py) that calls StatsBombPy to create subset_bundesliga.json.
Serve the index.html

Start a local server, for example:
bash
Copy
Edit
python -m http.server 8000
Open http://localhost:8000/index.html in your browser.
Interact

Toggle Shots, Goals, Passes, Assists checkboxes.
Select a Team or Player from dropdowns.
Click on a top‐scoring player or team to see only that player’s or team’s goals.

Future Plans
Positions: Incorporate player positions (Defender, Midfielder, etc.) to allow position-based filtering.
Set Pieces: Extend the data to track corners, free kicks, and other set pieces.
Performance Metrics: Show advanced stats like expected goals (xG) or pass completion rates.




---

### Next Steps

1. **Adjust** the number of top scorers or top teams if you want more or fewer.  
2. **Refine** how you handle toggles if you want to allow Shots/Passes/Assists to remain on while focusing on a player/team’s goals.  
3. **Expand** the project to handle advanced analytics (xG, set pieces, positional data) or integrate an actual backend for large-scale usage.
