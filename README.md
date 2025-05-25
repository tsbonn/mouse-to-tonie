# Mouse to Tonie

A Python tool to automatically download the latest episode of a podcast (default "Die Sendung mit der Maus") and upload it to a Creative Tonie using the [tonie-api](https://pypi.org/project/tonie-api/) library.

## Features

- Downloads the latest podcast episode using Selenium (handles dynamic web pages)
- Uploads the episode to a specified Creative Tonie
- Optionally clears all chapters before upload
- Logs all actions and errors to both the console and a log file (`mouse_to_tonie.log`)

---

## Requirements

- Python 3.8+
- Google Chrome browser
- [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=de) (matching your Chrome version, and available in your PATH)
- The following Python packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `tonie-api`
  - `pydantic`

---

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tsbonn/mouse-to-tonie.git
   cd mouse-to-tonie
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**

   ```bash
   pip install requests beautifulsoup4 selenium tonie-api pydantic
   ```

4. **Install ChromeDriver:**

   - Download the version matching your Chrome browser from [here](https://sites.google.com/chromium.org/driver/).
   - Place the executable in your PATH or specify its location in `downloader.py` if needed.

5. **Configure your settings:**

   - Copy `sampe_config.ini` to `config.ini` and replace placeholders

---

## Usage

1. **Run the main script:**

   ```bash
   python main.py
   ```

2. **Logs:**

   - All actions and errors are logged to both the console and `mouse_to_tonie.log` in the project directory.

---

## Troubleshooting

- **ChromeDriver errors:**  
  Ensure ChromeDriver is installed and matches your Chrome version. Adjust the path in `downloader.py` if necessary.

- **Network errors:**  
  If you see connection errors, check your internet connection and the target URLs.

- **Tonie API errors:**  
  Make sure your Toniecloud credentials are correct and your account has access to the specified Creative Tonie.

---

## License

MIT License, see LICENSE file

---

## Credits

- [tonie-api](https://github.com/toniebox-reverse-engineering/tonie-api) for TonieCloud API access
- [Selenium](https://www.selenium.dev/) for browser automation

---

## Disclaimer

This project is not affiliated with Tonies®, Boxine GmbH, ARD, WDR or Sendung mit der Maus. Use at your own risk.