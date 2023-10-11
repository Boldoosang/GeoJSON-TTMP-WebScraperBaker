from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import timeunit, json

driver = webdriver.Chrome()  # For Chrome
constituencies = []

url = "https://www.thepicongparty.com/politics/profiles/central"  
driver.get(url)

_timeout = 10  # ⚠ don't forget to set a reasonable timeout
WebDriverWait(driver, _timeout).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ProfilePage_dropdownGroup__1RPML"))
)

# Interact with the page (e.g., click buttons, fill out forms)
dropdown = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/select")
dropdown.click()
driver.implicitly_wait(3)
elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/select/option[position() > 1]")
for i in range(0 , len(elements)+1):
    driver.implicitly_wait(3)
    constituency_code = elements[i].get_attribute("value")
    elements[i].click()

    name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]").text.split(': ')[1]
    address = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]").text.split(': ')[1]
    number = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]").text.split(': ')[1]
    email = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[4]").text.split(': ')[1]
    
    constituency = { "constituency_code" : constituency_code, "official" : {
        "name" : name,
        "address" :  address,
        "number" : number,
        "email" : email
    }}

    constituencies.append(constituency)
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/select/option")
    

with open("constituencies.json", "w") as f:
    f.write(json.dumps(constituencies))
    print("Exported to constituencies.json!")

driver.quit()
exit()



