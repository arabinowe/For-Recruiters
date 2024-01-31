import tkinter as tk
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import tkinter.font as tkFont

def create_counter_window():
    global counter_label
    window = tk.Tk()
    window.title("Counter")
    window.attributes('-topmost', True)

    # Specify a larger font size
    font_style = tkFont.Font(family="Lucida Grande", size=20)

    counter_label = tk.Label(window, text="0", font=font_style)
    counter_label.pack()
    window.mainloop()


# Start Tkinter in a separate thread
tkinter_thread = threading.Thread(target=create_counter_window, daemon=True)
tkinter_thread.start()

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

def login():
    try:
        driver.get(r"http://www.neopets.com/pirates/process_restaurant.phtml?type=add&item=15721")
        time.sleep(2)
        username_field = driver.find_element(By.CSS_SELECTOR, "#loginUsername")
        username_field.send_keys("leviathan696")
        time.sleep(1)
        password_field = driver.find_element(By.CSS_SELECTOR, "#loginPassword")
        password_field.send_keys("CDiU8n9UaYhJ84B")
        time.sleep(1)
        login_button = driver.find_element(By.CSS_SELECTOR, "#loginButton")
        login_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")

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
            counter_label.config(text=str(counter))  # Update the Tkinter label
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
