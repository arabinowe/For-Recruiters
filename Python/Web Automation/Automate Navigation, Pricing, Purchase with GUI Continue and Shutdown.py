import tkinter as tk
import tkinter.font as tkFont
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Flag to control the loop based on GUI action
continue_flag = False
shutdown_flag = False

# Function to be called when the continue button is pressed
def on_yes_button_pressed():
    global continue_flag
    continue_flag = True

# Function to be called when the shutdown button is pressed
def on_shutdown_button_pressed():
    global shutdown_flag, driver
    shutdown_flag = True
    try:
        driver.quit()  # Close the WebDriver to interrupt the loop
    except Exception as e:
        print(f"Shutdown Error: {e}")
        
# Tkinter setup
def create_counter_window():
    try:
        print("Starting Tkinter GUI thread...")
        global counter_label, window
        window = tk.Tk()
        window.title("Counter")
        window.attributes('-topmost', True)
        
        font_style = tkFont.Font(family="Lucida Grande", size=20)
        counter_label = tk.Label(window, text="0", font=font_style)
        counter_label.pack()
        
        yes_button = tk.Button(window, text="Continue Script", command=on_yes_button_pressed)
        yes_button.pack()
        
        shutdown_button = tk.Button(window, text="Shutdown", command=on_shutdown_button_pressed)
        shutdown_button.pack()

        print("Tkinter window is about to enter mainloop.")
        window.mainloop()
    except Exception as e:
        print(f"Tkinter Error: {e}")
        
# Start Tkinter in a separate thread (only once)
tkinter_thread = threading.Thread(target=create_counter_window, daemon=True)
tkinter_thread.start()


# Move all items into safety deposit box to protect items from restaurant loop
def quickstock_sdb():
    driver.get("https://www.neopets.com/quickstock.phtml")
    driver.find_element(By.XPATH, "//input[@type='radio' and @name='checkall' and contains(@onclick, 'check_all(2);')]").click()
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit' and contains(@onclick, 'check_discard()')]").click()



def main_loop():
    global continue_flag, shutdown_flag
    login()
    while True:
        if shutdown_flag:
            break
        restaurant_loop()
        if continue_flag:
            continue_flag = False
            continue
    time.sleep(1)
        
# Set up Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_driver_path = r"C:\Users\arbin\Downloads\chromedriver_win32\chromedriver.exe"
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

driver = webdriver.Chrome(options=chrome_options)

price = 68000  # Your target price
item_name = "One Hundred Dubloon Coin"
# Buys Dubloons!
def shop_wizard(driver, price, item_name):
    try:
        # Wait for the search input to be present on the page
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#shopwizard"))
        )
        # Clear the search field and type the item name
        search_input.clear()
        search_input.send_keys(item_name)

        # Wait for the search button to be clickable and click it
        search_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_wizard > div"))
        )
        search_button.click()
        print(f"Searched for '{item_name}'")
        
        time.sleep(2)
        # Wait for the results to be present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#shopWizardFormResults > div.wizard-results-grid.wizard-results-grid-shop > ul"))
        )
        items = driver.find_elements(By.CSS_SELECTOR, "#shopWizardFormResults > div.wizard-results-grid.wizard-results-grid-shop > ul > li:nth-child(2)")
        lowest_price = float('inf')
        lowest_price_element = None

        time.sleep(2)
        # Loop through items and check the price
        for item in items:
            item_price_text = item.find_element(By.CSS_SELECTOR, "div").text
            item_price = int(item_price_text.replace(" NP", "").replace(",", ""))
            if item_price < lowest_price:
                lowest_price = item_price
                lowest_price_element = item

        if lowest_price <= price and lowest_price_element is not None:
            # Click on the shop owner's name of the listing with the lowest price
            shop_owner_link = lowest_price_element.find_element(By.CSS_SELECTOR, "a")
            shop_owner_link.click()
            print("Clicked on the shop owner's name.")
            
            # Wait for the shop item to be clickable
            shop_item = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@style, 'text-align: center')]/table/tbody/tr/td/a/img"))
            )
            shop_item.click()
            print("Clicked on the shop item.")

            # Wait for the alert to be present and accept it
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = Alert(driver)
            alert.accept()
            print("Accepted the alert.")
            return True
        else:
            # If no price is low enough, click the resubmit button
            resubmit_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#resubmitWizard"))
            )
            resubmit_button.click()
            return False

    except NoSuchElementException:
        print("No such element found")
        return False
    except TimeoutException:
        print("Loading took too much time!")
        return False
    except Exception as e:
        print(f"Unexpected error when checking prices or clicking items: {e}")
        return False

    try:
        # Wait for the shop item to be clickable
        shop_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@style, 'text-align: center')]/table/tbody/tr/td/a/img"))
        )
        shop_item.click()
        print("Clicked on the shop item.")
    except TimeoutException:
        print("Shop item was not clickable.")
        return False
    except Exception as e:
        print(f"Error clicking on shop item: {e}")
        return False

    try:
        # Wait for the alert to be present and accept it
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()
        print("Accepted the alert.")
        return True
    except TimeoutException:
        print("No alert appeared.")
        return False
    except Exception as e:
        print(f"Error accepting alert: {e}")
        return False


def login():
    try:
        driver.get(r"https://www.neopets.com/shops/wizard.phtml")
        time.sleep(2)
        username_field = driver.find_element(By.CSS_SELECTOR, "#loginUsername")
        username_field.send_keys("")
        time.sleep(1)
        password_field = driver.find_element(By.CSS_SELECTOR, "#loginPassword")
        password_field.send_keys("")
        time.sleep(1)
        login_button = driver.find_element(By.CSS_SELECTOR, "#loginButton")
        login_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")

def update_counter_label(counter):
    counter_label.config(text=str(counter))

def restaurant_loop():
    global window, driver  # Ensure driver is declared as global if it's initialized outside this function
    url = "http://www.neopets.com/pirates/process_restaurant.phtml?type=add&item=15721"
    counter = 0
    attempts = 0
    max_attempts = 10

    while counter < 10 and attempts < max_attempts:
        try:
            driver.get(url)
            element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#content > table > tbody > tr > td.content > center:nth-child(5) > form > table > tbody > tr:nth-child(3) > td > center > form > input[type=submit]:nth-child(3)"))
            )
            element.click()
            if "Return to Krawk Island!!!" in driver.page_source:
                counter += 1
                attempts = 0  # Reset attempts on successful action
            else:
                attempts += 1  # Increment attempts if the expected outcome isn't met
            window.after(0, update_counter_label, counter)  # Thread-safe update
            print(f"Counter: {counter}")
            time.sleep(2)
        except Exception as e:
            print(f"Loop Interrupted: {e}")
            attempts += 1  # Increment attempts on exception
            time.sleep(2)  # Wait a bit before trying again

        if attempts >= max_attempts:
            print("Maximum attempts reached, exiting loop.")
            break

    if counter < 10:
        print("Failed to complete 10 iterations.")
    else:
        print("Completed 10 iterations successfully.")


# Main loop
login()
for i in range(10):
    driver.get(r'https://www.neopets.com/shops/wizard.phtml')
    shop_wizard(driver, price,item_name="One Hundred Dubloon Coin")
    restaurant_loop()
    quickstock_sdb()
    counter = 0
    print(f'That\'s loop {i}!')

# Close the WebDriver and exit
driver.quit()
