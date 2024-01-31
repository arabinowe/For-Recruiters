import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

# Specify the path to your GeckoDriver
gecko_driver_path = r"C:\Users\arbin\Downloads\geckodriver-v0.34.0-win64\geckodriver.exe"

# Setting up Firefox and GeckoDriver
options = Options()
options.headless = True  # This enables headless mode
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

def extract_item_data(item_url):
    driver.get(item_url)
    wait = WebDriverWait(driver, 10)
    try:
        # Extract the item name
        item_name_selector = "body > div.row > div.large-9.small-12.columns.content-wrapper > h1"
        item_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, item_name_selector))).text.strip()

        # Get the restock range value
        restock_range_selector = "div.large-3.push-2.small-12.columns > ul > li:nth-child(2) > p"
        restock_range_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, restock_range_selector))).text
        restock_values = list(map(int, re.findall(r'\d+', restock_range_text.replace(',', ''))))
        if len(restock_values) == 1:
            lowest_restock = highest_restock = restock_values[0]
        else:
            lowest_restock, highest_restock = restock_values
        average_restock = sum(restock_values) / len(restock_values)

        # Get the last three market prices and clean the text
        market_prices_selector = "div.large-7.push-2.small-12.columns > div.pricing-row-container > div"
        market_prices_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, market_prices_selector)))
        market_prices = [int(re.search(r'\d+', price.text.replace(',', '')).group()) for price in market_prices_elements if re.search(r'\d+', price.text)]
    # If there are less than 3 prices, we pad the list with the last available price or 0 if none are available
        while len(market_prices) < 3:
            market_prices.append(market_prices[-1] if market_prices else 0)        
        
        average_market_price = sum(market_prices) / len(market_prices)

        # Calculate average profit
        average_profit = average_market_price - average_restock

        return {
            'name': item_name,
            'url': item_url,
            'lowest_restock': lowest_restock,
            'highest_restock': highest_restock,
            'average_restock': average_restock,
            'latest_price': market_prices[0],
            'second_latest_price': market_prices[1],
            'third_latest_price': market_prices[2],
            'average_market_price': average_market_price,
            'average_profit': average_profit
        }
    except TimeoutException:
        print(f"No data available for {item_url}, skipping...")
        return None
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
        return None

def scrape_jellyneo_item_urls(base_url):
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    item_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.no-padding > li > a")))
    urls = [link.get_attribute('href') for link in item_links]
    return urls

# URL to scrape
category_url = "https://items.jellyneo.net/search/?cat[]=39&cat[]=64&sort=5&sort_dir=desc&limit=75&start=75"
item_urls = scrape_jellyneo_item_urls(category_url)

# Placeholder for data to write to CSV
item_data_list = []

# Extract data for each item
for item_url in item_urls:
    item_data = extract_item_data(item_url)
    if item_data:
        item_data_list.append(item_data)

# Writing data to CSV
csv_file_path = "jellyneo_item_data.csv"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'url', 'lowest_restock', 'highest_restock', 'average_restock', 'latest_price', 'second_latest_price', 'third_latest_price', 'average_market_price', 'average_profit'])
    writer.writeheader()
    for item_data in item_data_list:
        if item_data:  # Only write rows for which data was successfully retrieved
            writer.writerow(item_data)

# Close the browser
driver.quit()
