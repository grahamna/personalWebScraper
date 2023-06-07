# personalWebScraper
 python --version 3.11.2
 
## Description
 This Python script allows you to search for a product on eBay and Amazon, and compare the prices and ratings of the product across both websites. You can specify the keyword for the search and the maximum number of pages to scrape. The script stores the data in CSV files named after the searched keyword, for both Amazon and eBay.

 May work on expanding this project to include grocery stores to find the best deals.

## Dependencies
 tqdm  
 pandas  
 requests-html  
 datetime  
 
## Usage
 Install the required dependencies using the following command: pip install tqdm pandas requests-html datetime
 Run the script by typing python main.py in the terminal.
 The script will prompt you to enter the keyword for the product search.
 The script will then fetch the data from eBay and Amazon, and store it in separate CSV files.
 The CSV files will be named after the searched keyword, for both Amazon and eBay.
 You can modify the fetchEbay and fetchAmazon functions to customize the search parameters and URL.

 ------------------------------------------------------

 # Book Scraper - In Progress

This is a book scraper script that fetches chapters from a website and saves them into separate text files.

## Description

The book scraper script is designed to scrape chapters from a specific website and save them as text files. It is currently set up to scrape chapters from the Royal Road website (https://www.royalroad.com), but it can be modified to work with other websites as well.

The script uses the `requests_html` library to fetch the HTML content of the web pages and extract the relevant data. It saves each chapter's content into separate text files, and it also supports navigating to the next chapter until there are no more chapters available.

## Usage

1. Make sure you have Python 3.x installed on your system.

2. Install the required dependencies by running the following command:
  pip install requests_html

3. Run the script with the following command:
  python royalRoadBookScraper.py [URL1] [URL2]
  
  Replace `[URL1]`, `[URL2]`, etc., with the URLs of the book chapters you want to scrape. Separate multiple URLs with spaces. If no URLs are provided, the script will use a default URL.

4. The script will fetch the chapters one by one and save them as separate text files in the `book` directory.

5. Once the scraping process is complete, you will find the scraped chapters in the `book` directory. Each chapter will be saved in a separate text file.

## Customization

- **Website:** The script is currently set up to work with the Royal Road website. If you want to scrape chapters from a different website, you need to modify the script accordingly. Update the HTML element selectors, URL patterns, and any other necessary logic to match the structure of the target website.

- **Output Format:** By default, the script saves the chapters as text files. If you want to save them in a different format or modify the output in any other way, you can customize the `fetchBook` function according to your requirements.

## Disclaimer

Please note that scraping websites may be against the terms of service of some websites. Make sure you have the necessary permissions or rights to scrape content from the target website. Use this script responsibly and in compliance with the website's terms of service.



# Contributors
 Nathan Graham
