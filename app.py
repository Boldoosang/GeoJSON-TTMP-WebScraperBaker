from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, json
import subprocess

scrape_url = "https://www.thepicongparty.com/politics/profiles/central"  

#Comment these lines out if you already have a json map file
geojson_url = "https://ebctt.com/constituencies.json"
response = requests.get(geojson_url)
with open("mapIn.geojson", "w") as f:
    f.write(json.dumps(response.json()))
    print("Constituency GeoJSON map downloaded to 'mapIn.geojson'!")
#End Comment these lines out if you already have a json map file

try:
    mapIn = open("mapIn.geojson")
except:
    print("Unable to locate input file. Please add a 'mapIn.geojson' file into the directory and re-run.")
    exit()

mapInDict = json.load(mapIn)
for i in range(0, len(mapInDict["features"])):
    if mapInDict["features"][i]["properties"]["Constituency"] == "TOBAGO EAST":
        mapInDict["features"][i]["geometry"]["type"] = "Polygon"
        mapInDict["features"][i]["geometry"]["coordinates"] = [mapInDict["features"][i]["geometry"]["coordinates"][4]]
    if mapInDict["features"][i]["properties"]["Constituency"] == "DIEGO MARTIN WEST":
        mapInDict["features"][i]["geometry"]["coordinates"] = [mapInDict["features"][i]["geometry"]["coordinates"][5]]
        
with open("mapOut.geojson", "w") as f:
    f.write(json.dumps(mapInDict))
    print("Constituency official information added and saved to 'mapOut.geojson'!")


mapshaper_command = "mapshaper mapOut.geojson -simplify 2.5% -o force mapOut.geojson format=geojson"

try:
    subprocess.run(mapshaper_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running npm command: {e}")
except FileNotFoundError:
    print("NPM not found. Please make sure Node.js and npm are installed and in your system's PATH.")


try:
    mapIn = open("mapOut.geojson")
except:
    print("Unable to locate input file. Please add a 'mapIn.geojson' file into the directory and re-run.")
    exit()

updatedMapInDict = json.load(mapIn)

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
    constituency_name = elements[i].text
    elements[i].click()

    name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]").text.split(': ')[1]
    address = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]").text.split(': ')[1]
    number = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]").text.split(': ')[1]
    email = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[4]").text.split(': ')[1]
    
    constituency = { "constituency_name" : constituency_name, "official" : {
        "name" : name,
        "address" :  address,
        "number" : number,
        "email" : email
    }}

    constituencies.append(constituency)
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/select/option")
    
driver.quit()

for polygon in updatedMapInDict["features"]:
    for constituency in constituencies:
        if polygon["properties"]["Constituency"].upper() == constituency["constituency_name"].upper():
            polygon["properties"]["official"] = constituency["official"]

with open("mapOut.geojson", "w") as f:
    f.write(json.dumps(updatedMapInDict))
    print("Constituency official information added and saved to 'mapOut.geojson'!")