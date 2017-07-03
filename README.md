# RugScraper
Scrapes Rugs

## Setup
You'll need to install beautifulsoup4 and requests with pip

``` bash
pip install beautifulsoup4 requests
```

also create a csv to use with 

``` bash
touch rugs.csv
```

## Current Functionality
Given a hardcoded range of id's, will scape a given base_url for name of rug, valid id of rug, and a link to a picture of the rug. It will put this information into a csv file called rugs.csv. 

## Future features
Cleaner csv output
Image renaming and file information cleanup
