from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # You can remove this line if you want to see the browser window
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Set the path to the Chrome WebDriver executable
chrome_driver_path = r"C:\Users\arbin\Downloads\chromedriver_win32\chromedriver.exe"

# Set the WebDriver property to use the specified Chrome driver path
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

driver = webdriver.Chrome(options=chrome_options)


# URL to navigate to
url = "http://www.neopets.com/pirates/process_restaurant.phtml?type=add&item=15721"

counter = 0  # Initialize the counter

while counter < 9:
    try:
        driver.get(url)
        
        # Wait for the element to appear, or timeout after 6 seconds
        element = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#content > table > tbody > tr > td.content > center:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > center > form > input[type=submit]:nth-child(3)"))
        )
        
        # Click the element
        element.click()
        
        # Check if "Return to Krawk Island!!!" text appears on the page
        if "Return to Krawk Island!!!" in driver.page_source:
            counter += 1  # Increment the counter
        print(str(counter))
        # Wait for a few seconds before attempting again
        time.sleep(2)
    except:
        # If the element doesn't appear within 6 seconds, navigate back to the URL and try again
        continue
    # Prompt the user for input to repeat or exit

# Navigate to the Quick Stock page
driver.get("https://www.neopets.com/quickstock.phtml?r=")
time.sleep(10)

# Starting at the second row, as the first is likely a header
row_number = 2

while True:
    try:
        # Use the CSS selector to target the item name in the row
        item_selector = f"#content > table > tbody > tr > td.content > form > table > tbody > tr:nth-child({row_number}) > td:nth-child(1)"
        item_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, item_selector)))
        item_name = item_name_element.text.lower()  # Convert to lower case for case-insensitive matching
        
        # If the item name contains 'dubloon', find and click the deposit checkbox
        if 'dubloon' in item_name:
            deposit_checkbox_selector = f"#content > table > tbody > tr > td.content > form > table > tbody > tr:nth-child({row_number}) > td:nth-child(4) > input[type='checkbox']"
            deposit_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, deposit_checkbox_selector)))
            deposit_checkbox.click()

        row_number += 1
    except Exception as e:
        # If no more rows are found or an error occurs, break the loop
        print(f"No more items or an error occurred: {e}")
        break
        

# Locate and click the element with the given CSS selector
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.CSS_SELECTOR, "#content > table > tbody > tr > td.content > form > table > tbody > tr:nth-child(33) > td:nth-child(3) > input"))
)

element.click()

# Click the submit button after selecting all dubloons
submit_button_selector = "#content > table > tbody > tr > td.content > form > table > tbody > tr:nth-child(6) > td > input[type=submit]:nth-child(1)"
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector)))
submit_button.click()

user_input = input("Do you want to repeat the process? (yes/no): ").strip().lower()
if user_input != "yes":
    driver.quit()
# Close the WebDriver

