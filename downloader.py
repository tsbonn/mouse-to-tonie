import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time
import logging

# license: This code is released under the MIT License

# Set up logging to both console and the same log file as main.py
log_file_path = os.path.join(os.path.dirname(__file__), "mouse_to_tonie.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def download_latest_episode_selenium(url, save_path="."):
    """
    Downloads the latest episode of an mp3 file from the given URL
    using Selenium to handle dynamically loaded content, and saves it
    to the specified save path.

    Install required packages:
    pip install requests beautifulsoup4 selenium

    Ensure you have the Chrome WebDriver installed and available in your PATH.
    If you get an error, try commenting in the service line in the code below.

    Args:
        url (str): The URL of the webpage containing the podcast episodes.
        save_path (str, optional): The path where the file should be saved.
                                    Defaults to the current directory.

    Returns:
        str or None: Full path to downloaded file or None in case of error.
    """
    driver = None  # Initialize driver to None
    try:
        # 1. Configure Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Uncomment the next lines if you have a specific path to the ChromeDriver
        # service = Service('/path/to/chromedriver')  # Specify your path to chromedriver, e.g., '/usr/local/bin/chromedriver'
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        logger.info(f"Fetching page: {url}")
        # 2. Fetch the webpage with Selenium
        driver.get(url)

        # Increased wait time for JavaScript to load, up to 10 seconds,
        # waiting for an element that might contain the links
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )  # Wait until the body is loaded
        )
        time.sleep(3)  # Additional short sleep to ensure all dynamic content settles

        # 3. Get the rendered page source
        page_source = driver.page_source

        # 4. Parse the HTML
        soup = BeautifulSoup(page_source, "html.parser")

        # 5. Find the link to the latest MP3 file
        mp3_url = None

        # Search for <a> tags with href ending in .mp3
        # This is often the most direct way to find download links.
        # We'll look for the first one, assuming it's the latest episode.
        for link in soup.find_all("a", href=True):
            if link["href"].endswith(".mp3"):
                mp3_url = link["href"]
                # Ensure the URL is absolute if it's relative
                if not mp3_url.startswith("http"):
                    # Basic relative URL handling; might need refinement for complex cases
                    # Example: if url is https://www.wdrmaus.de/hoeren/podcast60.php5
                    # and mp3_url is /path/to/file.mp3
                    from urllib.parse import urljoin

                    mp3_url = urljoin(url, mp3_url)
                break

        # If no direct .mp3 link found, try looking for common download link texts
        if not mp3_url:
            logger.warning("No direct .mp3 link found. Trying to find links by text content.")
            keywords = ["mp3-downloadpodcast", "Download", "herunterladen", "Podcast"]
            for link in soup.find_all("a", href=True):
                if any(
                    keyword.lower() in link.get_text().lower() for keyword in keywords
                ):
                    # Check if the href itself leads to a downloadable file
                    if ".mp3" in link["href"]:  # Heuristic check
                        mp3_url = link["href"]
                        if not mp3_url.startswith("http"):
                            from urllib.parse import urljoin

                            mp3_url = urljoin(url, mp3_url)
                        break

        if mp3_url:
            logger.info(f"Found mp3-url: {mp3_url}")

            # 6. Download the MP3 file
            response_mp3 = requests.get(mp3_url, stream=True)
            response_mp3.raise_for_status()

            # 7. Create a filename with currend date and save the file
            filename = (
                datetime.today().strftime("%Y-%m-%d")
                + "_"
                + mp3_url.split("/")[-1].split("?")[0]
            )  # Extract filename and remove query parameters
            # Clean filename from potential non-filesystem characters if necessary (optional)
            filename = "".join(
                c for c in filename if c.isalnum() or c in (".", "_", "-")
            )

            full_path = os.path.join(save_path, filename)

            with open(full_path, "wb") as file:
                for chunk in response_mp3.iter_content(chunk_size=8192):
                    file.write(chunk)

            logger.info(f"Latest episode saved at: {full_path}")
            return full_path
        else:
            logger.warning("No direct mp3-link found on given page.")
            logger.warning("Maybe the website structure has changed, or the correct link is hidden deeper in some JavaScript-structure.")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Exception on performing request of website or mp3-file: {e}")
        return None
    except Exception as e:
        logger.error(f"An unknown exception occured: {e}")
        return None
    finally:
        if driver:
            driver.quit()
