import os
import sys
import httplib
import base64
import json
import new
import unittest
import sauceclient
from selenium import webdriver
from sauceclient import SauceClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose import with_setup # optional

# it's best to remove the hardcoded defaults and always get these values
# from environment variables
USERNAME = os.environ.get('SAUCE_USERNAME', "arpitach")
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', "a3cd4703-1e03-4eb5-9bfe-8c3e8e56a535")
sauce = SauceClient(USERNAME, ACCESS_KEY)

#caps = webdriver.DesiredCapabilities.IPAD
#caps = webdriver.DesiredCapabilities.ANDROID

browsers = [#{"platform": "Mac OS X 10.9",
            # "browserName": "chrome",
            # "version": "31"},
            #{"platform": "Windows 8.1",
            # "browserName": "internet explorer",
            # "version": "11"},
            #{"platform": "OS X 10.10",
            # "browserName": "firefox",
            # "version": "32"},
            {"platform": "OS X 10.9",
             "browserName": "iPad",
             "version": "7.1",
             "device-orientation": "portrait"},
            {"platform": "Linux",
             "browserName": "Android",
             "version": "4.4",
             "deviceName":"Google Nexus 7 HD Emulator",
             "device-orientation": "portrait"},
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
class SauceTabletTest(unittest.TestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        
        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(30)
    
    
    def test_browser(self):    
        self.driver.get("http://www.google.co.in")
        print "header title = " + self.driver.title
        assert "Google" in self.driver.title , "Could not found Google in driver title"
        elem = self.driver.find_element_by_name("q")
        elem.send_keys("aruba networks")
        if (self.desired_capabilities['browserName'] == 'iPad') or (self.desired_capabilities['browserName'] == 'Android') :
            elem.send_keys(Keys.ENTER)
        else:    
            self.driver.find_element_by_name("btnG").click()
        
        
        try:
            if (self.desired_capabilities['browserName'] == 'iPad') or (self.desired_capabilities['browserName'] == 'Android') :
                self.driver.implicitly_wait(30)
            else:    
                WebDriverWait(self.driver, 30).until(
                                                 
                                               EC.presence_of_element_located((By.ID, "resultStats"))
                                               )
                
                findElements = self.driver.find_elements(By.XPATH, "//*[@id='rso']//h3/a")
                for elem in findElements :
                    print elem.get_attribute('href')
                assert len(findElements) > 0 ,"Search does not return anything"   
        finally:
            #self.driver.close()
            print "\n"
    
        

    
    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()