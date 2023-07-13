# LinkedIn Auto Endorse Bot

This is a Python script that automates the process of endorsing skills for your LinkedIn connections. The script uses the Selenium library to control a web browser and perform automated actions on the LinkedIn website.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed on your system
- Selenium library installed (`pip install selenium`)
- Chrome WebDriver executable (`chromedriver`) placed in the specified path

## Setup

1. Install the required libraries using the following command:

   ```
   pip install selenium progress
   ```

2. Download the Chrome WebDriver executable appropriate for your Chrome browser version and operating system from the official Selenium WebDriver website: [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

3. Specify the path to the Chrome WebDriver executable by updating the `CHROMEDRIVER_PATH` variable in the code.

4. Provide your LinkedIn account credentials by replacing the empty strings `username` and `password` with your LinkedIn username and password in the code.

## Usage

1. Run the script using the following command:

   ```
   python linkedin_auto_endorse_bot.py
   ```

2. The script will launch a Chrome browser window and prompt you to sign in to your LinkedIn account. If you have previously signed in and saved your cookies, it will automatically load the cookies for authentication.

3. Once signed in, the script will navigate to the "Connections" page and scroll to the bottom of the page to load all your connections.

4. It will then visit each connection's profile and endorse their skills one by one.

5. The progress will be displayed in the console, and a CSV file named `connections.csv` with the links to all your connections will be created.

6. After endorsing skills for all connections, the script will terminate the browser session.

**Note:** Please use this script responsibly and adhere to LinkedIn's terms of service.
