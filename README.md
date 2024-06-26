# onlineBookScraper

This is a book scraper script that fetches chapters from a website via url and saves them into separate text files. I'm happy as to where this program is at for personal use.

## Description

The book scraper script is designed to scrape chapters from a specific website and save them as text files. It is currently set up to scrape chapters from common fanfiction websites (https://www.royalroad.com, https://forums.spacebattles.com, https://forums.sufficientvelocity.com, https://www.fanfiction.net), but it can be modified to work with other websites as well.

The script uses the `requests_html` and `undetected_chromedriver` library to fetch the HTML content of the web pages and extract the relevant data. It saves each chapter's content into separate text files, and it also supports navigating to the next chapter until there are no more chapters available.

## Usage

1. Make sure you have Python 3.x installed on your system.

2. Install the required dependencies by running the following command:
   pip install requests_html
   pip install undetected_chromedriver

3. Run the script with the following command:
   python royalRoadBookScraper.py [URL1] [URL2] ...

Replace `[URL1]`, `[URL2]`, etc., with the URLs of the book chapters you want to scrape. Separate multiple URLs with spaces. If no URLs are provided, the script will listen for urls to be entered.

4. The script will fetch the chapters one by one and save them as separate text files in the `book` directory.

5. Once the scraping process is complete, you will find the scraped chapters in the `book` directory. Each chapter will be saved in a separate text file.

## Customization

- **Website:** The script is currently set up to work with the Royal Road website. If you want to scrape chapters from a different website, you need to modify the script accordingly. Update the HTML element selectors, URL patterns, and any other necessary logic to match the structure of the target website.

- **Output Format:** By default, the script saves the chapters as text files. If you want to save them in a different format or modify the output in any other way, you can customize the `fetchBook` function according to your requirements.

- **Adding Urls:** You can add new URLs while the program is running by entering them when prompted. To stop the program, enter 'q' when prompted for a new URL. This can only be done when running the program without CLI args.

- **Passing Capchas:** You can manually pass the captcha by changing the uc.Chrome(headless=True, ...) to False, visa versa if uc is able to pass the capcha on it's own. This only applies to fanfiction.net atm.

- **Login Creds:** You can manually enter in login credentials (seen in the fetchBookQQ method, var name is payload). Note, you may need to add more than username and password. Check out the packet sent to login site for format and vars of the creds and whatnot.

## Disclaimer

Please note that scraping websites may be against the terms of service of some websites. Make sure you have the necessary permissions or rights to scrape content from the target website. Use this script responsibly and in compliance with the website's terms of service.

# <--------------->

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

# Contributors

  Nathan Graham
