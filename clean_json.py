import json
import numpy as np
import pandas as pd

# Load the original JSON file
input_file = "bundesliga_events.json"
output_file = "cleaned_bundesliga_events.json"

try:
    # Open the JSON file with UTF-8 encoding
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)  # Load JSON data

    # Convert to pandas DataFrame for cleaning
    df = pd.DataFrame(data)

    # Replace problematic values
    df = df.replace([np.nan, np.inf, -np.inf], None)
    
    # Convert back to list of dictionaries
    cleaned_data = df.to_dict(orient="records")

    # Save cleaned JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Cleaned JSON saved successfully as {output_file}")

except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
except UnicodeDecodeError as e:
    print(f"Encoding error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
