#Step 1: Import
from wsbaker import wsbaker

#Step 2: Configure using wsbaker(inputFileLocation.geojson, outputFileLocation.geojson, scrape_url, *geojson_url)
wb = wsbaker()

#Step 3: Run
wb.run()