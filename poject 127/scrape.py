from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# NASA Exoplanet Catalog Scraper
START_URL = "https://en.wikipedia.org/wiki/Brown_dwarf"
browser = webdriver.Chrome()  # Initializing Chrome WebDriver
browser.get(START_URL)  # Opening the specified URL in the browser

time.sleep(2)  # Adding a delay to allow the page to fully load

planets_data = []  # List to store extracted planet data

def scrape_nasa_exoplanets():
    for i in range(0, 5):  # Looping through a range of 10 pages (adjust as needed)
        print(f'Scraping page {i+1} ...')

        # BeautifulSoup Object
        soup = BeautifulSoup(browser.page_source, "html.parser")  # Creating a BeautifulSoup object for the current page

        # Loop to find elements using XPATH
        for planet in soup.find_all("div", class_='hds-content-item'):  # Finding all planet elements on the page

            planet_info = []  # List to store information about each planet

            # Extract planet name
            planet_info.append(planet.find('h3', class_='heading-22').text.strip())  # Finding and storing planet name

            information_to_extract = ["Light-Years From Earth", "Planet Mass",
                                      "Stellar Magnitude", "Discovery Date"]

            for info_name in information_to_extract:
                try:
                    # Extract other planet information
                    planet_info.append(planet.select_one(f'span:-soup-contains("{info_name}")')
                                       .find_next_sibling('span').text.strip())
                except:
                    planet_info.append('Unknown')  # Handling cases where information is not found

            planets_data.append(planet_info)  # Adding planet information to the list
       
        try:
            time.sleep(2)
            next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="primary"]/div/div[3]/div/div/div/div/div/div/div[2]/div[2]/nav/button[8]')))

            browser.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(2)

            next_button.click()  

        except:
            print(f"Error occurred while navigating to next page:")
            break

# Calling the scraping method
scrape_nasa_exoplanets()

# Define Header for DataFrame
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Create pandas DataFrame from the extracted data
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert DataFrame to CSV and save to file
planet_df_1.to_csv('scraped_data_nasa_exoplanets.csv', index=True, index_label="id")

# Step 1: Load the csv file of brown dwarf stars and clean the data
brown_dwarf_df = pd.read_csv('scraped_data.csv')
brown_dwarf_df.dropna(inplace=True)  # Remove rows with NaN values

# Step 2: Convert Mass and Radius columns to floating point values
brown_dwarf_df['Mass'] = brown_dwarf_df['Mass'].astype(float)
brown_dwarf_df['Radius'] = brown_dwarf_df['Radius'].astype(float)

# Step 3: Convert Mass and Radius columns to solar units
brown_dwarf_df['Mass'] = brown_dwarf_df