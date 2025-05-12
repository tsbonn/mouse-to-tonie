import configparser
import os
import logging
import requests
from tonie_api.api import TonieAPI

config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file_path)

try:
    username = config['api_credentials']['username']
    password = config['api_credentials']['password']
except (KeyError, configparser.NoSectionError, configparser.NoOptionError) as e:
    print(f"Fehler beim Lesen der Konfigurationsdatei: {e}")

# set up detailed logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

api=TonieAPI(username, password)
list_of_tonies = api.get_all_creative_tonies()

# Find the CreativeTonie with the name 'Kreativ-Tonie Johanna Skater'
tonie_name = "Kreativ-Tonie Johanna Skater"
selected_tonie = next((tonie for tonie in list_of_tonies if tonie.name == tonie_name), None)

if selected_tonie:
    # Call the clear_all_chapter_of_tonie function with the selected CreativeTonie
    api.clear_all_chapter_of_tonie(selected_tonie)
    print(f"Cleared all chapters of the Tonie: {selected_tonie.name}")
else:
    print(f"No CreativeTonie found with the name '{tonie_name}'")


