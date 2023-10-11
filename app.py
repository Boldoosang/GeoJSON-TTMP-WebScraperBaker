from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, json


geojson_url = "https://ebctt.com/constituencies.json"
scrape_url = "https://www.thepicongparty.com/politics/profiles/central"  

#to be continued
# #response = requests.get(geojson_url)

# #with open("mapIn.geojson", "w") as f:
#     f.write(json.dumps(response.json()))
#     print("Constituency GeoJSON map downloaded to 'mapIn.geojson'!")

try:
    mapIn = open("mapIn.geojson")
except:
    print("Unable to locate input file. Please add a 'mapIn.geojson' file into the directory and re-run.")
    exit()

driver = webdriver.Chrome()  # For Chrome
constituencies = []


driver.get(scrape_url)

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
    
driver.quit()

polygonData = json.load(mapIn)

collection = polygonData["features"]

for polygon in collection:
    for constituency in constituencies:
        if polygon["properties"]["ID"] == constituency["constituency_code"]:
            polygon["properties"]["official"] = constituency["official"]

with open("mapOut.geojson", "w") as f:
    f.write(json.dumps(polygonData))
    print("Constituency official information added and saved to 'mapOut.geojson'!")