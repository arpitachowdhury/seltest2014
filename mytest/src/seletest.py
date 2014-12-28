import os
import sys
import httplib
import base64
import json
import new
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose import with_setup # optional

#import nltk

browsers = [{ "browserName": "chrome"},
            #{ "browserName": "internet explorer"},
            { "browserName": "firefox"}
           ]
def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator


@on_platforms(browsers)
class TestMe(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        #self.desired_capabilities['name'] = self.id()
        
        if self.desired_capabilities['browserName'] == 'firefox':
            self.driver=webdriver.Firefox()
        elif self.desired_capabilities['browserName'] == 'internet explorer':
            self.driver=webdriver.Ie()
            
        elif self.desired_capabilities['browserName'] == 'chrome':
            self.driver=webdriver.Chrome()
        else:
            self.skipTest("Unsupported Browser")
        self.driver.implicitly_wait(30)

 
    @classmethod
    def tearDown(self):
        print ("\nteardown_class() cleanup method for TestMe\n")
        print("Session Id:%s" % self.driver.session_id)
        self.driver.quit()
        
    
    def test_browser(self):    
        driver = self.driver
        driver.get("http://www.google.co.in")
        driver.maximize_window()
        print "header title = " + driver.title
        #assert "Google" in driver.title , "Could not found Google in driver title"
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
            #driver.close()
            print "Ending session"
          
