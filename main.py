import configparser
import os
import logging
from tonie_api.api import TonieAPI
from downloader import download_latest_episode_selenium
from datetime import datetime

# Set up detailed logging to both console and file
log_file_path = os.path.join(os.path.dirname(__file__), "mouse_to_tonie.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Read configuration from config.ini
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), "config.ini")
try:
    config.read(config_file_path)

    username = config["api_credentials"]["username"]
    password = config["api_credentials"]["password"]
    creative_tonie_name = config["tonie_config"]["creative_tonie_name"]
    clear_all_chapters_before_upload = config["app_config"]["clear_all_chapters_before_upload"] == "True"
    keep_downloaded_files = config["app_config"]["keep_downloaded_files"] == "True"
    download_url = config["app_config"]["download_url"]
    data_dir = config["app_config"]["data_dir"]
except (KeyError, configparser.NoSectionError, configparser.NoOptionError) as e:
    logger.error(f"Error on reading config file config.ini: {e}")
    exit(1)
except Exception as e:
    logger.error(f"Unexpected error while reading config: {e}")
    exit(1)

try:
    # Create the save directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory: {data_dir}")

    # Download the latest episode using downloader.py
    downloaded_file = download_latest_episode_selenium(download_url, data_dir)
    logger.info(f"Downloaded file: {downloaded_file}")

    # If downloaded_file is not None, upload it to the Tonie
    if downloaded_file is not None:
        try:
            # Connect to the Tonie API and get the list of Creative Tonies
            api = TonieAPI(username, password)
            logger.info("Connected to Tonie API")
            list_of_tonies = api.get_all_creative_tonies()
            logger.info(f"Retrieved {len(list_of_tonies)} Creative Tonies")

            # Find the CreativeTonie with the name in variable creative_tonie_name
            selected_tonie = next(
                (tonie for tonie in list_of_tonies if tonie.name == creative_tonie_name), None
            )

            if selected_tonie:
                logger.info(f"Found CreativeTonie: {selected_tonie.name}")
                if clear_all_chapters_before_upload:
                    try:
                        api.clear_all_chapter_of_tonie(selected_tonie)
                        logger.info(f"Cleared all chapters of the Tonie {selected_tonie.name}")
                    except Exception as e:
                        logger.error(f"Error clearing chapters: {e}")
                try:
                    api.upload_file_to_tonie(
                        selected_tonie,
                        downloaded_file,
                        "Mouse to Tonie" + " " + datetime.today().strftime("%Y-%m-%d"),
                    )
                    logger.info(f"Uploaded file {downloaded_file} to Tonie {selected_tonie.name}")
                except Exception as e:
                    logger.error(f"Error uploading file: {e}")
            else:
                logger.warning(f"No CreativeTonie found with the name '{creative_tonie_name}'")
        except Exception as e:
            logger.error(f"Error during Tonie API operations: {e}")

    # Clean up downloaded files if keep_downloaded_files is False
    if not keep_downloaded_files and downloaded_file is not None:
        try:
            os.remove(downloaded_file)
            logger.info(f"Removed downloaded file: {downloaded_file}")
        except OSError as e:
            logger.error(f"Error removing file {downloaded_file}: {e}")
except Exception as e:
    logger.error(f"An error occurred in the main workflow: {e}")