# GeoJSON - Trinidad and Tobago Member of Parliament Web Scraper & Baker
Welcome to the GeoJSON baker for TTMP information! This project was designed to "bake"/embed information regarding the general election members of parliament. As future elections occur, there is a need to produce this GeoJSON file with all of the information included. Initially designed as a utility tool for [SpotDPothole Frontend](https://github.com/Boldoosang/NAV-spotDPothole-frontend).


## IMPLEMENTED FEATURES
The following features have been implemented:
* Automatic downloading of general election map.
* Automatic gathering of general election constituency leaders.
* Automatic baking of constituency leaders into election map.


## CONFIGURATION
The application can be initialized and configured as follows:
(Optional) Create a virtual environment for the project and activate it.
```
$ python -m venv "venv"
$ venv/Scripts/Activate.bat
```
Install the requirements for the application using pip3.
```
$ pip install -r requirements.txt
```
Install the mapshaper npm package.
```
$ npm install -g mapshaper
```
Place your input GeoJSON file into the directory and rename it to "mapIn.geojson" OR edit the geojson_url to include the URL to the geojson file.
Run the baker using the following command:
```
$ python app.py
```
Make use of your new baked GeoJSON file, "mapOut.geojson"!

## THE RESULTS
The following show the differences in the stucture of the GeoJSON file to reflect the addition of the MP information.
![Outcome](images/output.png)


## DEPENDENCIES AND FRAMEWORKS
* [Python 3.12](https://www.python.org/downloads/) - Python as main programming language.
* [EBC Constituency Map Overlay](https://ebctt.com/constituencies.json) - Used as the GeoJSON file for elections.
* [Selenium Web Driver](https://www.selenium.dev/documentation/webdriver/) - Selenium used for web-browser automating.
* [Picong Party Election](https://www.thepicongparty.com/politics/profiles/central) - Picong Party for MP Data.
