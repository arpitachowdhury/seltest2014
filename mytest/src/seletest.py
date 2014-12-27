from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import nltk


binary = FirefoxBinary("C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
driver = webdriver.Firefox()
driver.get("http://www.google.co.in")
print "header title = " + driver.title
assert "Google" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("aruba networks")
driver.find_element_by_name("btnG").click()


try:
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "resultStats"))
    )
    findElements = driver.find_elements(By.XPATH, "//*[@id='rso']//h3/a")
    for elem in findElements :
        print elem.get_attribute('href')
finally:
    driver.close()