from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import pandas
from datetime import date


USERNAME = ""  # insert username
PASSWORD = ""  # insert password


class MojoData:
    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=path)
        self.names = []
        self.addresses = []
        self.numbers = []
        self.cities = []
        self.zips = []
        self.emails = []
        self.state = []

    def login(self):  # logs user into Mojo
        self.driver.get("https://lb11.mojosells.com/login/?source=www.mojosells.com")
        time.sleep(2)
        username = self.driver.find_element(By.NAME, "email")
        username.click()
        username.send_keys(USERNAME)
        username.send_keys(Keys.TAB)
        password = self.driver.find_element(By.NAME, "password")
        password.click()
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(3)

    def find_scrape_list(self):  # finds list labeled "To Scrape". This code is specific to this user.
        self.driver.get('https://app631.mojosells.com/main/?frame=/data_management/')
        time.sleep(3)
        self.driver.switch_to.frame('g_site_iframe')
        self.driver.find_element(By.ID, 'list_item_71').click()
        time.sleep(1)

    def find_names(self):  # scrapes name from list of names in Mojo
        scrape_names = self.driver.find_elements(By.CLASS_NAME, 'custom_name_full_name')
        for name in scrape_names:
            self.names.append(name.text)

    def find_addresses(self):  # scrapes addresses from Mojo
        scrape_addresses = self.driver.find_elements(By.CLASS_NAME, 'custom_name_address')
        for address in scrape_addresses:
            self.addresses.append(address.text)
        scrape_city = self.driver.find_elements(By.CLASS_NAME, 'custom_name_city')
        for city in scrape_city:
            self.cities.append(city.text)
        scrape_state = self.driver.find_elements(By.CLASS_NAME, 'custom_name_state')
        for state in scrape_state:
            self.state.append(state.text)
        scrape_zips = self.driver.find_elements(By.CLASS_NAME, 'custom_name_zip_code')
        for zipcode in scrape_zips:
            self.zips.append(zipcode.text)

    def find_numbers(self):  # scrapes phone numbers from Mojo
        scrape_numbers = self.driver.find_elements(By.CLASS_NAME, 'custom_name_phone')
        for number in scrape_numbers:
            self.numbers.append(number.text)

    def find_emails(self):  # scrapes emails from Mojo
        scrape_emails = self.driver.find_elements(By.CLASS_NAME, 'custom_name_email')
        for email in scrape_emails:
            self.emails.append(email.text)

    def next_page(self):  # scrolls to the bottom of the pages and clicks "next" button
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.driver.find_element(By.ID, 'contacts_table_next').click()
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0)")

    def compile_mojo_data(self):   # compiles scraped data into .csv
        today = date.today().strftime("%B %d")
        data_dict = {
            "name": self.names,
            "address": self.addresses,
            "city": self.cities,
            "state": self.state,
            "zip": self.zips,
            "number": self.numbers,
            "email": self.emails
        }
        data = pandas.DataFrame(data_dict)
        data.to_csv(f"{today}_neighborhood_data.csv")