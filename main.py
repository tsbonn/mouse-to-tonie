import configparser
import os
import logging
from tonie_api.api import TonieAPI
from downloader import download_latest_episode_selenium
from datetime import datetime

# Read configuration from config.ini
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_file_path)

try:
    username = config["api_credentials"]["username"]
    password = config["api_credentials"]["password"]
    creative_tonie_name = config["tonie_config"]["creative_tonie_name"]
    clear_all_chapters_before_upload = config["app_config"]["clear_all_chapters_before_upload"] == "True"
    keep_downloaded_files = config["app_config"]["keep_downloaded_files"] == "True"
    download_url = config["app_config"]["download_url"]
    data_dir = config["app_config"]["data_dir"]
except (KeyError, configparser.NoSectionError, configparser.NoOptionError) as e:
    print(f"Error on reading config file: {e}")

# Set up detailed logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Create the save directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Download the latest episode using downloader.py
downloaded_file = download_latest_episode_selenium(download_url, data_dir)

# If downloaded_file is not None, upload it to the Tonie
if downloaded_file is not None:
    # Connect to the Tonie API and get the list of Creative Tonies
    api = TonieAPI(username, password)
    list_of_tonies = api.get_all_creative_tonies()

    # Find the CreativeTonie with the name in variable creative_tonie_name
    selected_tonie = next(
        (tonie for tonie in list_of_tonies if tonie.name == creative_tonie_name), None
    )

    if selected_tonie:
        print(f"Found CreativeTonie: {selected_tonie.name}")
        if clear_all_chapters_before_upload:
            api.clear_all_chapter_of_tonie(selected_tonie)
            print(f"Cleared all chapters of the Tonie {selected_tonie.name}")
        api.upload_file_to_tonie(
            selected_tonie,
            downloaded_file,
            "Mouse to Tonie" + " " + datetime.today().strftime("%Y-%m-%d"),
        )
        print(f"Uploaded file {downloaded_file} to Tonie {selected_tonie.name}")
    else:
        print(f"No CreativeTonie found with the name '{selected_tonie.name}'")

# Clean up downloaded files if keep_downloaded_files is False
if not keep_downloaded_files and downloaded_file is not None:
    try:
        os.remove(downloaded_file)
        print(f"Removed downloaded file: {downloaded_file}")
    except OSError as e:
        print(f"Error removing file {downloaded_file}: {e}")