import configparser
import os
import logging
from tonie_api.api import TonieAPI

config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file_path)

try:
    username = config['api_credentials']['username']
    password = config['api_credentials']['password']
    creative_tonie_name = config['tonie_config']['creative_tonie_name']
    clear_all_before_upload = (config['app_config']['clear_all_before_upload'] == 'True')
except (KeyError, configparser.NoSectionError, configparser.NoOptionError) as e:
    print(f"Fehler beim Lesen der Konfigurationsdatei: {e}")

# Set up detailed logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Connect to the Tonie API and get the list of Creative Tonies
api=TonieAPI(username, password)
list_of_tonies = api.get_all_creative_tonies()

# Find the CreativeTonie with the name in variable creative_tonie_name
selected_tonie = next((tonie for tonie in list_of_tonies if tonie.name == creative_tonie_name), None)

if selected_tonie:
    print(f"Found CreativeTonie: {selected_tonie.name}")
    if clear_all_before_upload:
        api.clear_all_chapter_of_tonie(selected_tonie)
        print(f"Cleared all chapters of the Tonie: {selected_tonie.name}")
    api.upload_file_to_tonie(selected_tonie, "test.mp3", "Test Chapter")
    print(f"Uploaded file to Tonie: {selected_tonie.name}")
else:
    print(f"No CreativeTonie found with the name '{selected_tonie.name}'")


