# personalWebScraper
 python --version 3.11.2
 
# Description
 This Python script allows you to search for a product on eBay and Amazon, and compare the prices and ratings of the product across both websites. You can specify the keyword for the search and the maximum number of pages to scrape. The script stores the data in CSV files named after the searched keyword, for both Amazon and eBay.

 May work on expanding this project to include grocery stores to find the best deals.

# Dependencies
 tqdm
 pandas
 requests-html
 datetime
 
# Usage
 Install the required dependencies using the following command: pip install tqdm pandas requests-html datetime
 Run the script by typing python main.py in the terminal.
 The script will prompt you to enter the keyword for the product search.
 The script will then fetch the data from eBay and Amazon, and store it in separate CSV files.
 The CSV files will be named after the searched keyword, for both Amazon and eBay.
 You can modify the fetchEbay and fetchAmazon functions to customize the search parameters and URL.

# Contributors
 Nathan Graham
