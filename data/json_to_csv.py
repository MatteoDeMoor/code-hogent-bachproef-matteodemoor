import json
import csv
import os

# Lijst van mapnummers
folder_numbers = [11, 116, 12, 1238, 1267, 1470, 16, 2, 223, 35, 37, 43, 44, 49, 53, 55, 7, 72, 81, 87, 9]

# Pad naar de hoofddirectory met mappen
base_dir = r"D:\Hogent\Visual Studio Code\BP\open-data\data\matches"
output_dir = r"D:\Hogent\Visual Studio Code\BP\BP_code\csv"

# Velden die je wilt opnemen in de CSV
csv_columns = [
    "match_id", "match_date", "kick_off", "competition_id", "competition_name", "country_name",
    "season_id", "season_name", "home_team_id", "home_team_name", "away_team_id", "away_team_name",
    "home_score", "away_score", "match_week", "stadium_name", "stadium_country", "referee_name", "referee_country"
]

# Functie om één JSON-bestand om te zetten naar een rij voor de CSV
def json_to_csv_row(match_data):
    return {
        "match_id": match_data.get("match_id", None),
        "match_date": match_data.get("match_date", None),
        "kick_off": match_data.get("kick_off", None),
        "competition_id": match_data["competition"].get("competition_id", None),
        "competition_name": match_data["competition"].get("competition_name", None),
        "country_name": match_data["competition"].get("country_name", None),
        "season_id": match_data["season"].get("season_id", None),
        "season_name": match_data["season"].get("season_name", None),
        "home_team_id": match_data["home_team"].get("home_team_id", None),
        "home_team_name": match_data["home_team"].get("home_team_name", None),
        "away_team_id": match_data["away_team"].get("away_team_id", None),
        "away_team_name": match_data["away_team"].get("away_team_name", None),
        "home_score": match_data.get("home_score", None),
        "away_score": match_data.get("away_score", None),
        "match_week": match_data.get("match_week", None),
        # Controleer of het 'stadium'-veld bestaat voordat je het probeert te benaderen
        "stadium_name": match_data["stadium"].get("name", None) if "stadium" in match_data else None,
        "stadium_country": match_data["stadium"]["country"].get("name", None) if "stadium" in match_data and "country" in match_data["stadium"] else None,
        # Controleer of het 'referee'-veld bestaat
        "referee_name": match_data["referee"].get("name", None) if "referee" in match_data else None,
        "referee_country": match_data["referee"]["country"].get("name", None) if "referee" in match_data and "country" in match_data["referee"] else None
    }

# Controleer of de output directory bestaat, anders maak deze aan
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop door elke map in de lijst van folder_numbers
for folder_num in folder_numbers:
    json_dir = os.path.join(base_dir, str(folder_num))  # Pad naar de huidige map
    output_csv = os.path.join(output_dir, f"matches_{folder_num}.csv")  # Output CSV-bestandsnaam

    # Alle JSON-bestanden in de huidige map verwerken en omzetten naar CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

        # Loop door alle JSON-bestanden in de opgegeven directory
        for filename in os.listdir(json_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(json_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    # JSON-bestand laden
                    data = json.load(json_file)

                    # Omdat het JSON-bestand meerdere wedstrijden kan bevatten, loop je door elke wedstrijd heen
                    for match in data:
                        csv_row = json_to_csv_row(match)
                        writer.writerow(csv_row)

    print(f"Data uit map {folder_num} is succesvol omgezet naar {output_csv}")
