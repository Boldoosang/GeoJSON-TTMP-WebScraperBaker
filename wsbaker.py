#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, json
import argparse
import subprocess

#scrape_url = "https://www.thepicongparty.com/politics/profiles/central"  
#geojson_url = "https://ebctt.com/constituencies.json"

class wsbaker:
    def __init__(self, inputFileLocation="mapIn.geojson", outputFileLocation="mapOut.geojson", scrape_url="https://www.thepicongparty.com/politics/profiles/central", geojson_url="https://ebctt.com/constituencies.json"):
        self.mapInLocation = inputFileLocation
        self.mapOutLocation = outputFileLocation
        self.scrape_url = scrape_url
        self.geojson_url = geojson_url

    def downloadJson(self, fileLocation):
        if (self.geojson_url == None or self.geojson_url == ()):
            return
        response = requests.get(self.geojson_url)
        with open(fileLocation, "w") as f:
            f.write(json.dumps(response.json()))
            print("Constituency GeoJSON map downloaded to '" + fileLocation + "' !")

    def load(self, fileLocation):
        try:
            return open(fileLocation)
        except:
            print("Unable to locate input file. Please ensure '" + fileLocation + "' exists and re-run.")
            exit()
        
    def save(self, fileLocation, geoJSONData):
        with open(fileLocation, "w") as f:
            f.write(json.dumps(geoJSONData))
            print("Information saved to '" + fileLocation + "' !")

    def correctMap(self, mapLocation):
        mapFile = self.load(mapLocation)
        map = json.load(mapFile)
        for i in range(0, len(map["features"])):
            if map["features"][i]["properties"]["Constituency"] == "TOBAGO EAST" or map["features"][i]["properties"]["Constituency"] == "DIEGO MARTIN WEST":
                map["features"][i]["geometry"]["type"] = "Polygon"
                map["features"][i]["geometry"]["coordinates"] = [max((map["features"][i]["geometry"]["coordinates"]), key=len)]

        return map
            

    def simplifyMap(self, inputFile, outputFile):
        mapshaper_command = "mapshaper " + inputFile + " -simplify 2.5% -o force " + outputFile + " format=geojson"
        try:
            subprocess.run(mapshaper_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running npm command: {e}")
            print(f"We will not attempt to get the required packages for installation provided that you have Node.js npm manager installed.")
            mapshaperInstallCommand = "npm install -g mapshaper"
            try:
                subprocess.run(mapshaperInstallCommand, shell=True, check=True)
                subprocess.run(mapshaper_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error installing mapshaper: {e}")
            except FileNotFoundError:
                print("NPM not found. Please make sure Node.js and npm are installed and in your system's PATH.")
        except FileNotFoundError:
            print("NPM not found. Please make sure Node.js and npm are installed and in your system's PATH.")


    def scrape(self, scrapeURL):
        constituencies = []
        try:
            driver = webdriver.Chrome() 
            driver.get(scrapeURL)

            _timeout = 10 
            WebDriverWait(driver, _timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ProfilePage_dropdownGroup__1RPML"))
            )

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
        except:
            print("ERROR: Please ensure the website is valid and the scraper is configured to gather data from this source.")

        return constituencies

    def bake(self, inputFileLocation, outputFileLocation, constituencies):
        mapFile = self.load(inputFileLocation)
        map = json.load(mapFile)

        for polygon in map["features"]:
            for constituency in constituencies:
                if polygon["properties"]["Constituency"].upper() == constituency["constituency_name"].upper():
                    polygon["properties"]["official"] = constituency["official"]

        self.save(outputFileLocation, map)

    def run(self):
        try:
            self.downloadJson(self.mapInLocation)
        except:
            print("Unable to download JSON file from " + str(self.geojson_url))

        correctedMap = self.correctMap(self.mapInLocation)
        self.save(self.mapOutLocation, correctedMap)

        #The output of the correction will be used as the input for the simplification, which would then overwrite the original file.
        self.simplifyMap(self.mapOutLocation, self.mapOutLocation)

        scrapedConstituencyData = self.scrape(self.scrape_url)
        self.bake(self.mapOutLocation, self.mapOutLocation, scrapedConstituencyData)

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='GeoJsonTTMPWebScraperBaker@Boldoosang')

    parser.add_argument('i', help='The input file that contains the GeoJSON data. Please include the extension.')
    parser.add_argument('o', help='The location where you would like the final GeoJSON file saved. Please include the extension.')
    parser.add_argument('--url', help='The website to be scraped for constituency information.')
    parser.add_argument('--json', help='Optional. The URL of the geojson file located on a website.')

    args = parser.parse_args()

    argList = []
    argList.append(args.i)
    argList.append(args.o)

    if args.url:
        argList.append(args.url)

    if args.json:
        argList.append(args.json)

    wsbaker(*argList).run()