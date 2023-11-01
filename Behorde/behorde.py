import traceback

from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv

import logging
import pygame

import time
import os

load_dotenv()

country = os.getenv('COUNTRY')
nbr_of_persons = os.getenv('ANZAHL_DER_PERSONEN')
with_family = os.getenv('WITH_FAMILY')
service_option = os.getenv('SERVICE_OPTION')
service_category = os.getenv('SERVICE_CATEGORY')
visa_type = os.getenv('VISA_TYPE')


def play_wav_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def get_traceback(e):
    """
    Gets the errors' Traceback
    :param e: the error object
    :return: the error message
    """
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


class Auslanderbehorde:
    def __init__(self, url):
        self.wait_time = 20
        self.sound_file = os.path.join(os.getcwd(), "alarm.wav")
        self.error_message = """Für die gewählte Dienstleistung sind aktuell keine Termine frei! Bitte"""
        self.url = url
        self.driver = None

    def _init_driver(self):
        """
        Initializes the scraper
        :return:
        """
        # Make a request to the video URL

        # some stuff that prevents us from being locked out
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        options.add_argument("disable-info bars")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=options)
        self.driver.implicitly_wait(self.wait_time)  # seconds
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.53 Safari/537.36'})

    def _enter_start_page(self):
        """
        Login to the homepage and choose booking an appointment
        :return:
        """
        logging.info("Accessing url: " + self.url)
        self.driver.get(self.url)
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div['
                                                        '4]/form/div/div/div/div/div/div/div/div/div/div[1]/div['
                                                        '1]/div[2]/a'))
        )
        time.sleep(5)
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div['
                                           '4]/form/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a').click()
        time.sleep(2)

    def _agree_on_terms(self):
        logging.info("Ticking off agreement")
        self.driver.find_element(By.XPATH, '//*[@id="xi-div-1"]/div[4]/label[2]/p').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'applicationForm:managedForm:proceed').click()
        time.sleep(5)

    def _set_service_option(self):
        condition = lambda ser: ser == service_option
        selection = self.driver.find_element(By.ID, 'xi-div-30')
        labels = selection.find_elements(By.TAG_NAME, 'label')
        selected_label = next((x for x in labels if condition(x.text)), None)
        selected_label.find_element(By.XPATH, './parent::*').click()
        time.sleep(5)

    def _set_service_category(self):
        if service_option == 'Aufenthaltstitel - beantragen' or service_option == 'Aufenthaltstitel - verlängern':
            condition = lambda cat: cat == service_category
            selection = self.driver.find_element(By.ID, 'xi-div-30')
            labels = selection.find_elements(By.TAG_NAME, 'label')
            selected_label = next((x for x in labels if condition(x.text)), None)
            selected_label.find_element(By.XPATH, './parent::*').click()
            time.sleep(5)

    def _set_visa_type(self):
        condition = lambda typ: typ == visa_type
        selection = self.driver.find_element(By.ID, 'xi-div-30')
        labels = selection.find_elements(By.TAG_NAME, 'label')
        selected_label = next((x for x in labels if condition(x.text)), None)
        selected_label.find_element(By.XPATH, './parent::*').click()
        time.sleep(5)

    def _success(self):
        logging.info("!!!Appointment Found - Do not close the window!!!!")
        while True:
            play_wav_file(self.sound_file)

    def _fill_out_form(self):
        logging.info("Filling out form.")
        # select country
        s = Select(self.driver.find_element(By.ID, 'xi-sel-400'))
        s.select_by_visible_text(country)
        # select the number of persons
        s = Select(self.driver.find_element(By.ID, 'xi-sel-422'))
        s.select_by_visible_text(nbr_of_persons)
        # select with family or not
        s = Select(self.driver.find_element(By.ID, 'xi-sel-427'))
        s.select_by_visible_text(with_family)
        # Click on the service option to use
        self._set_service_option()
        # Click on the category option to use
        self._set_service_category()
        # Tick the visa type to apply for
        self._set_visa_type()
        # Submit
        self.driver.find_element(By.ID, 'applicationForm:managedForm:proceed').click()
        time.sleep(10)

    def _check_appointment(self):
        apt_found = False
        if not (self.error_message in self.driver.page_source):
            apt_found = True
        return apt_found

    def run(self):
        """
        Run The process forever
        """
        try:
            found = False
            self._init_driver()
            # Test audio file
            # play_wav_file(self.sound_file)
            while not found:
                logging.info("Trying to find an appointment.")
                self._enter_start_page()
                self._agree_on_terms()
                self._fill_out_form()
                found = self._check_appointment()
            self._success()
        except Exception as e:
            logging.info(get_traceback(e))
            self.driver.quit()
            self.run()

    def _get_country_list(self):
        selection = self.driver.find_element(By.ID, 'xi-sel-400')
        countries = selection.find_elements(By.TAG_NAME, 'option')
        for child_element in countries:
            print(child_element.text)

    def _get_nbr_of_persons(self):
        selection = self.driver.find_element(By.ID, 'xi-sel-422')
        persons = selection.find_elements(By.TAG_NAME, 'option')
        for child_element in persons:
            print(child_element.text)

    def _get_with_family(self):
        selection = self.driver.find_element(By.ID, 'xi-sel-427')
        family = selection.find_elements(By.TAG_NAME, 'option')
        for child_element in family:
            print(child_element.text)

    def _get_service_options(self):
        selection = self.driver.find_element(By.ID, 'xi-div-30')
        inputs = selection.find_elements(By.TAG_NAME, 'label')
        for child_element in inputs:
            print(child_element.text)

    def _get_category_options(self):
        selection = self.driver.find_element(By.ID, 'inner-285-0-2')
        inputs = selection.find_elements(By.TAG_NAME, 'label')
        for child_element in inputs:
            print(child_element.text)

    def _get_visa_types(self):
        selection = self.driver.find_elements(By.XPATH, '//*[contains(@name, "level3")]')
        for element in selection:
            next_sibling = element.find_element(By.XPATH, 'following-sibling::*')
            print(next_sibling.text)
