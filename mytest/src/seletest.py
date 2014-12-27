from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose import with_setup # optional

#import nltk

class TestMe:
    
    @classmethod
    def setup_class(cls):
        print ("\nsetup_class() init method for TestMe\n")
 
    @classmethod
    def teardown_class(cls):
        print ("\nteardown_class() cleanup method for TestMe\n")
    
    def test_browser(self):    
        driver = webdriver.Firefox()
        driver.get("http://www.google.co.in")
        print "header title = " + driver.title
        assert "Google" in driver.title , "Could not found Google in driver title"
        elem = driver.find_element_by_name("q")
        elem.send_keys("aruba networks")
        driver.find_element_by_name("btnG").click()


        try:
            WebDriverWait(driver, 30).until(
                                                      EC.presence_of_element_located((By.ID, "resultStats"))
                                                      )
            findElements = driver.find_elements(By.XPATH, "//*[@id='rso']//h3/a")
            for elem in findElements :
                print elem.get_attribute('href')
            assert len(findElements) > 0 ,"Search does not return anything"   
        finally:
            driver.close()