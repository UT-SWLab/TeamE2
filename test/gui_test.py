import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# You will need to change this if you are not using chromedriver for chrome v86
DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver')

# Homepage url
HOME_URL = 'https://f1stat-292509.uc.r.appspot.com/'

class GUI_Test(unittest.TestCase):
    # navbar tests
    def test_navbar_home(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(HOME_URL)
        driver.find_element_by_link_text('Home').click()
        self.assertEqual(driver.current_url, HOME_URL)
    
    def test_navbar_driver_model_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(HOME_URL)
        driver.find_element_by_link_text('Drivers').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_drivers')

    def test_navbar_constructor_model_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(HOME_URL)
        driver.find_element_by_link_text('Constructors').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_constructors')

    def test_navbar_circuit_model_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(HOME_URL)
        driver.find_element_by_link_text('Circuits').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_circuits')

    def test_navbar_about_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(HOME_URL)
        driver.find_element_by_link_text('About').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}about')

    
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


    # Driver model page tests
    def test_pagination_nextpage_driver(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_drivers')
        driver.find_element_by_css_selector("[aria-label='Next']")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_drivers?page=2')
    
    def test_pagination_prevpage_driver(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_drivers?page=2')
        prevPage = driver.find_element_by_css_selector("[aria-label='Previous']")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_drivers?page=1')

    def test_pagination_nextpagenumber_driver(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_drivers')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        nextPage = currentPage.find_element_by_xpath("following-sibling::li")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_drivers?page=2')

    def test_pagination_prevpagenumber_driver(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_drivers?page=2')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        prevPage = currentPage.find_element_by_xpath("preceding-sibling::li")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_drivers?page=1') 

    def test_driver_model_links(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_drivers')
        drivers = driver.find_elements_by_css_selector("[class='card']")
        for elem in drivers:
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

    
    # Driver instance page tests
    def test_driver_wiki_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}drivers?id=20')
        driver.find_element_by_link_text('Read More').click()
        self.assertEqual(driver.current_url, 'https://en.wikipedia.org/wiki/Sebastian_Vettel')

    def test_driver_constructor_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}drivers?id=20')
        driver.find_element_by_link_text('Ferrari').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}constructors?id=6')

    def test_driver_circuit_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}drivers?id=20')
        driver.find_element_by_link_text('Silverstone Circuit').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}circuits?id=9')


    # Constructor model page tests
    def test_pagination_nextpage_constructor(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_constructors')
        nextPage = driver.find_element_by_css_selector("[aria-label='Next']")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_constructors?page=2')
    
    def test_pagination_prevpage_constructor(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_constructors?page=2')
        prevPage = driver.find_element_by_css_selector("[aria-label='Previous']")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_constructors?page=1')

    def test_pagination_nextpagenumber_constructor(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_constructors')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        nextPage = currentPage.find_element_by_xpath("following-sibling::li")
        nextPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_constructors?page=2')

    def test_pagination_prevpagenumber_constructor(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_constructors?page=2')
        currentPage = driver.find_element_by_css_selector("[class='page-item active']")
        prevPage = currentPage.find_element_by_xpath("preceding-sibling::li")
        prevPage.click()
        self.assertEqual(driver.current_url, f'{HOME_URL}models_constructors?page=1') 

    def test_constructor_links(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}models_constructors')
        constructors = driver.find_elements_by_css_selector("[class='card card--1']")
        print(len(constructors))
        for elem in constructors:
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


    # Constructor instance page tests
    def test_constructor_wiki_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}constructors?id=25')
        driver.find_element_by_link_text('Read More').click()
        self.assertEqual(driver.current_url, 'https://en.wikipedia.org/wiki/Tyrrell_Racing')

    def test_constructor_driver_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}constructors?id=25')
        driver.find_element_by_link_text('Jackie Stewart').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}drivers?id=328')

    def test_constructor_circuit_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}constructors?id=25')
        driver.find_element_by_link_text('Circuit Park Zandvoort').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}circuits?id=39')


    # Circuit model page tests
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

    
    # Circuit instance page tests
    def test_circuit_wiki_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}circuits?id=19')
        driver.find_element_by_link_text('Read More').click()
        self.assertEqual(driver.current_url, 'https://en.wikipedia.org/wiki/Indianapolis_Motor_Speedway')

    def test_circuit_driver_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}circuits?id=19')
        driver.find_element_by_link_text('Rubens Barrichello').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}drivers?id=22')

    def test_circuit_constructor_link(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(f'{HOME_URL}circuits?id=19')
        driver.find_element_by_link_text('Ferrari').click()
        self.assertEqual(driver.current_url, f'{HOME_URL}constructors?id=6')


if __name__ == '__main__':
    unittest.main()
