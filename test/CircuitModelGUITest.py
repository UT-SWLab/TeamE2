import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# You will need to change this if you are not using chromedriver for chrome v86
DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver')

# Homepage url
HOME_URL = 'https://f1stat-292509.uc.r.appspot.com/'


class CircuitModelGUITest(unittest.TestCase):
    def test_pagination_nextpage_circuit(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_circuits')
        nextPage = driver.find_element_by_css_selector("[aria-label='Next']")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_circuits?page=2')
    

    def test_pagination_prevpage_circuit(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_circuits?page=2')
        prevPage = driver.find_element_by_css_selector("[aria-label='Previous']")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_circuits?page=1')


    def test_pagination_nextpagenumber_circuit(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_circuits')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        nextPage = currentPage.find_element_by_xpath("following-sibling::li")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_circuits?page=2')


    def test_pagination_prevpagenumber_circuit(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_circuits?page=2')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        prevPage = currentPage.find_element_by_xpath("preceding-sibling::li")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_circuits?page=1') 
    

    def test_circuit_links(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_circuits')
        circuits = driver.find_elements_by_css_selector("[class='card card--1']")
        driver.maximize_window()
        for elem in circuits:
            driver.implicitly_wait(5)
            link = elem.find_element_by_css_selector("[class='card_link']")
            name = elem.find_element_by_css_selector("[class='card__title']").text
            print(name)
            driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
            window_before = driver.window_handles[0]
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            instanceName = driver.find_element_by_css_selector("[class = 'instance-header']").text
            self.assertEqual(name, instanceName)
            driver.close()
            driver.switch_to_window(window_before)

if __name__ == '__main__':
    unittest.main()
