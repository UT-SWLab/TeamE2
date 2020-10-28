import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# You will need to change this if you are not using chromedriver for chrome v86
DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver')

# Homepage url
HOME_URL = 'https://f1stat-292509.uc.r.appspot.com/'

class GUI_Test(unittest.TestCase):
    # Driver model page tests
    # def test_driver_model_links(self):
    #     driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    #     driver.get(f'{HOME_URL}models_drivers')
    #     drivers = driver.find_elements_by_css_selector("[class='card']")
    #     for elem in drivers:
    #         driver.implicitly_wait(5)
    #         link = elem.find_element_by_css_selector("[class='card_link']")
    #         name = elem.find_element_by_css_selector("[class='card__title']").text
    #         print(name)
    #         driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
    #         window_before = driver.window_handles[0]
    #         window_after = driver.window_handles[1]
    #         driver.switch_to_window(window_after)
    #         instanceName = driver.find_element_by_css_selector("[class = 'instance-header']").text
    #         self.assertEqual(name, instanceName)
    #         driver.close()
    #         driver.switch_to_window(window_before)

    
    # About page tests
    def test_github_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}about')
        driver.find_element_by_link_text('Check out our Github Repo here!').click()
        self.assertEqual(driver.current_url, 'https://github.com/UT-SWLab/TeamE2')

    def test_ergast_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}about')
        driver.find_element_by_link_text('Ergast').click()
        self.assertEqual(driver.current_url, 'https://ergast.com/mrd/')

    def test_sportradar_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}about')
        driver.find_element_by_link_text('Sportradar').click()
        self.assertEqual(driver.current_url, 'https://developer.sportradar.com/docs/read/racing/Formula_1_v2')

    def test_rapid_api_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}about')
        driver.find_element_by_link_text('Rapid API').click()
        self.assertEqual(driver.current_url, 'https://rapidapi.com/api-sports/api/api-formula-1')


if __name__ == '__main__':
    unittest.main()
