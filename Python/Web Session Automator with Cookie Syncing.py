import requests
from bs4 import BeautifulSoup
import datetime
import random
import time
from datetime import timedelta
import os
from http.cookiejar import MozillaCookieJar
from concurrent.futures import ThreadPoolExecutor
import csv
from selenium.common.exceptions import NoSuchElementException
import json

class WebSession:
    def __init__(self, username, password, proxy=None):
        self.session = requests.Session()
        if proxy:
            self.session.proxies.update(proxy)
        self.base_url = 'https://www.example.com'
        self.headers = {
            'Referer': f'{self.base_url}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        self.username = username
        self.password = password
        self.cookies_file_path = f"C:\\Users\\user\\Documents\\Cookies\\{username}_Cookies.txt"
        self.load_cookies()

    def load_cookies(self):
        cookies_file_path = f"C:\\Program Files\\example\\Data\\{self.username}_Cookies.txt"
        if os.path.exists(cookies_file_path):
            with open(cookies_file_path, 'r') as file:
                cookie_data = file.read().strip().split('; ')
                for cookie_item in cookie_data:
                    if '=' in cookie_item:
                        name, value = cookie_item.split('=', 1)
                        cookie = requests.cookies.create_cookie(
                            name=name,
                            value=value,
                            domain='.example.com',
                            path='/',
                            secure=False,
                            expires=None
                        )
                        self.session.cookies.set_cookie(cookie)
        else:
            print(f"Cookies file not found for {self.username}.")

    def check_login_status(self):
        home_url = f'{self.base_url}/home'
        response = self.session.get(home_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        user_profile = soup.find("div", {"class": "user-profile"})
        
        if user_profile:
            print(f"Session appears to be logged in for {self.username}.")
            return True
        else:
            print(f"Session appears to be logged out for {self.username}.")
            return False
    
    def save_cookies(self):
        cookies_file_path = f"C:\\Program Files\\examples\\Data\\{self.username}_Cookies.txt"
        os.makedirs(os.path.dirname(cookies_file_path), exist_ok=True)
        
        cookie_data = []
        for cookie in self.session.cookies:
            cookie_item = f"{cookie.name}={cookie.value}"
            cookie_data.append(cookie_item)
        
        cookie_string = "; ".join(cookie_data)
        
        with open(cookies_file_path, 'w') as file:
            file.write(cookie_string)
        
        print(f"Cookies saved for {self.username}.")
        
    def login(self):
        self.load_cookies()
        if self.check_login_status():
            print(f"Already logged in using cookies for {self.username}.")
            return True

        login_page_url = 'https://www.example.com/login'
        response = self.session.get(login_page_url)
        if response.status_code != 200:
            print(f"Failed to load login page for {self.username}.")
            return False

        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

        login_url = 'https://www.example.com/login'
        data = {
            'username': self.username,
            'password': self.password,
            'csrf_token': csrf_token,
            'remember': '1',
        }

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            response = self.session.post(login_url, data=data)

            if response.status_code == 200 and 'session_id' in self.session.cookies:
                print(f"Login successful for {self.username}!")
                self.save_cookies()
                return True
            elif response.status_code != 403:
                print(f"Login failed for {self.username} with status code {response.status_code}. Retrying...")
                time.sleep(retry_delay)
            else:
                print(f"Login failed for {self.username} with status code {response.status_code}.")
                return False

        print(f"Max retries exceeded for {self.username}. Login failed.")
        return False

    def update_value(self):
        response = self.session.get(f'{self.base_url}/account', headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        value_element = soup.find('span', class_='value')

        if value_element:
            value = ''.join(filter(str.isdigit, value_element.text.strip()))

            file_exists = os.path.isfile(r"C:\Users\user\Documents\Values\values.csv")

            with open(r"C:\Users\user\Documents\Values\values.csv", 'r' if file_exists else 'w', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)

                username_exists = False
                for i, row in enumerate(rows):
                    if len(row) > 0 and row[0] == self.username:
                        username_exists = True
                        rows[i] = [self.username, value]
                        break

                if not username_exists:
                    rows.append([self.username, value])

            with open(r"C:\Users\user\Documents\Values\values.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            print(f"Updated value for {self.username}: {value}")
        else:
            print(f"Could not find value for {self.username}")

    def navigate_to_page(self, page_url):
        try:
            response = self.session.get(page_url, headers=self.headers)
            if response.status_code == 200:
                print(f"Navigated to {page_url} successfully for {self.username}.")
            else:
                print(f"Failed to navigate to {page_url} for {self.username}.")
        except NoSuchElementException:
            print(f"NoSuchElementException occurred while navigating to {page_url} for {self.username}")

    def process_items(self):
        response = self.session.get(f'{self.base_url}/items', headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        item_data = {}

        rows = soup.find_all('tr', class_='item-row')
        for index, row in enumerate(rows, start=1):
            item_name = row.find('td', class_='item-name').text.strip()
            item_id = row.find('input', {'name': lambda x: x.startswith('item_')})['value']
            item_data[f'item_{index}'] = item_id

        response = self.session.post(f'{self.base_url}/process_items', data=item_data, headers=self.headers)

        if response.status_code == 200:
            print(f"Items processed successfully for {self.username}.")
    
    def fetch_balance(self):
        response = self.session.get(f'{self.base_url}/balance', headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            balance_element = soup.find('span', class_='balance')
            if balance_element:
                balance = ''.join(filter(str.isdigit, balance_element.text))
                balance_int = int(balance)
                balance_with_commas = f"{balance_int:,}"
                print(f"Current balance: {balance_with_commas}")
                return balance_with_commas
            else:
                print("Could not find the balance.")
                return None
        else:
            print("Failed to navigate to the balance page.")
            return None
   
    def withdraw(self, amount):
        amount_without_commas = amount.replace(',', '')
        amount_int = int(amount_without_commas)
        if amount_int >= 50:
            withdraw_data = {
                'action': 'withdraw',
                'amount': str(amount_int),
            }
            response = self.session.post(f'{self.base_url}/withdraw', data=withdraw_data, headers=self.headers)
            if response.status_code == 200:
                print("Withdrawal successful.")
            else:
                print("Failed to withdraw.")
        else:
            print("Insufficient balance for withdrawal.")


credentials = [
{"username": "user1", "password": "password1", "proxy": {"http": "http://proxy1:port1"}},
{"username": "user2", "password": "password2", "proxy": {"http": "http://proxy2:port2"}},
# ... (rest of the obfuscated credentials)
]

random.shuffle(credentials)
start_time = time.time()

completed_iterations = 0


def handle_web_session(cred):
    try:
        web_session = WebSession(cred["username"], cred["password"], proxy=cred["proxy"])
        web_session.login()
        time.sleep(random.uniform(10, 13))
        balance = web_session.fetch_balance()
        if balance:
            web_session.withdraw(balance)
        time.sleep(random.uniform(1, 5))    
        
        web_session.navigate_to_page(f'{web_session.base_url}/items')
        time.sleep(random.uniform(1, 13))
        web_session.process_items()
        time.sleep(random.uniform(1, 5))
        web_session.navigate_to_page(f'{web_session.base_url}/items')
        
        time.sleep(random.uniform(1, 5))
        web_session.process_items()
        time.sleep(random.uniform(1, 5))
        web_session.navigate_to_page(f'{web_session.base_url}/items')

        time.sleep(random.uniform(30, 60))
    except Exception as e:
        print(f"An error occurred for {cred['username']}: {e}")


def main(credentials):
    num_credentials = len(credentials)
    processed_count = 0

    remaining_credentials = credentials.copy()

    with ThreadPoolExecutor(max_workers=10) as executor:
        while processed_count < num_credentials:
            index = random.randint(0, len(remaining_credentials) - 1)
            selected_credential = remaining_credentials.pop(index)
            executor.submit(handle_web_session, selected_credential)
            processed_count += 1
            time.sleep(random.uniform(1, 5))

    print("Done")


if __name__ == "__main__":
    main(credentials)