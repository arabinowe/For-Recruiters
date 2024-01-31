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

logged_in = 0

def login():
    try:
        # Wait for the elements to be present
        driver.get(r"http://www.neopets.com/pirates/process_restaurant.phtml?type=add&item=15721")
        time.sleep(2)  # Adjust the sleep time as needed

        # Find the username field and type the username
        username_field = driver.find_element(By.CSS_SELECTOR, "#loginUsername")
        username_field.send_keys("")
        time.sleep(1)
        # Find the password field and type the password
        password_field = driver.find_element(By.CSS_SELECTOR, "#loginPassword")
        password_field.send_keys("")  # Replace with the actual password
        time.sleep(1)
        # Press Enter
        login_button = driver.find_element(By.CSS_SELECTOR, "#loginButton")
        login_button.click()
        logged_in=1
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to perform restaurant loop
def restaurant_loop():
    url = "http://www.neopets.com/pirates/process_restaurant.phtml?type=add&item=15721"
    counter = 0

    while counter < 10:
        try:
            driver.get(url)
            element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#content > table > tbody > tr > td.content > center:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > center > form > input[type=submit]:nth-child(3)"))
            )
            element.click()
            if "Return to Krawk Island!!!" in driver.page_source:
                counter += 1
            print(str(counter))
            time.sleep(2)
        except:
            continue

# Main loop
login()
while True:
    restaurant_loop()

    user_input = input("Do you want to repeat the entire process? (yes/no): ").strip().lower()
    if user_input == "yes":
        continue
    elif user_input == "no":
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

# Close the WebDriver and exit
driver.quit()
