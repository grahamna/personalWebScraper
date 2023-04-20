import sys
from tqdm import tqdm
import pandas as pd
from requests_html import HTMLSession
import datetime

UserAgent = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",
    "Connection" : "close",
    "Upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
  }
timeStamp = datetime.date.today()
data = []


def fetchEbay(keyword, page_num_max=1, urlString='https://www.ebay.com/sch/i.html?_from=R40&_nkw="{keyword}"&_sacat=0&LH_TitleDesc=0&_fsrp=1&_sop=15&_pgn={page_num}'):
    session = HTMLSession()
    urls = []
    for page_num in range(1, page_num_max+1):
        urlString = urlString.format(keyword=keyword, page_num=page_num)
        urls.append(str(urlString))
    for url in tqdm(urls):
        response = session.get(url.strip())
        content = response.html.find('div.s-item__info.clearfix', first=False)
        count = 0
        for item in tqdm(content):
            count = count + 1
            title = item.find('div.s-item__title', first=True).text
            try:
                subtitle = item.find('div.s-item__subtitle', first=True).text
            except:
                subtitle = ''
            price = item.find('span.s-item__price', first=True).text
            price = price.replace(",", "")
            try:
                shipping = item.find('span.s-item__shipping.s-item__logisticsCost', first=True).text.replace("shipping", "").replace("Free", "")
                if (shipping == ' '):
                    shipping = "0"
            except:
                shipping = "0"
            finalPrice = float(price.replace("$", "")) + float(shipping.replace("+$", ""))
            if(count!=1):
                data.append([title, subtitle, price, shipping, finalPrice, timeStamp])
    toDfAndCsvEbay(keyword)
    

def fetchAmazon(keyword, page_num_max=1, urlString='https://www.amazon.com/s?k={keyword}&s=exact-aware-popularity-rank&dc&page={page_num}'):
    session = HTMLSession()
    urls = []
    for page_num in range(1, page_num_max + 1):
        urlString = urlString.format(keyword=keyword, page_num=page_num)
        urls.append(str(urlString))
    for url in tqdm(urls):
        response = session.get(url, headers=UserAgent)
        content = response.html.find('div.a-section.a-spacing-small.a-spacing-top-small', first=False)
        for item in tqdm(content):
            record = True
            if(item != content[0] and item != content[1]):
                title = item.find('span.a-size-medium', first=True).text
                try:
                    ratingCount = item.find('span.a-size-base.s-underline-text', first=True).text
                    ratingCount = int(ratingCount.replace(',',''))
                except AttributeError:
                    ratingCount = ''
                    record = False
                try:
                    price = item.find('span.a-offscreen', first=True).text
                except AttributeError:
                    price = ''
                    record = False
                if record and ratingCount >= 250:
                    price = float(price.replace("$", ""))
                    data.append([title, ratingCount, price, timeStamp])
    toDfAndCsvAmazon(keyword)
    
def quickSearchAndCompare(keyword):
    fetchEbay(keyword, 1)
    fetchAmazon(keyword, 1)
    
    
def toDfAndCsvEbay(keyword):
    df = pd.DataFrame(data, columns=['Title', 'Subtitle', 'Price', 'Shipping', 'Final Price', 'Date'])
    df.to_csv('./output/{keyword}Ebay.csv'.format(keyword=keyword), index=False,mode="a+")
    print("Done")
    data.clear()
    
def toDfAndCsvAmazon(keyword):
    df = pd.DataFrame(data, columns=['Title', 'Rating Count', 'Price', 'Date'])
    df.to_csv('./output/{keyword}Amazon.csv'.format(keyword=keyword), index=False,mode="a+")
    print("Done")
    data.clear()
        
        
def main():
    fetchEbay("ultimate+hacking+keyboard", 1, 'https://www.ebay.com/sch/i.html?_from=R40&_nkw="{keyword}"&_sacat=0&LH_TitleDesc=0&_fsrp=1&_sop=15&_pgn={page_num}')
    fetchAmazon("ultimate+hacking+keyboard", 1, 'https://www.amazon.com/s?k={keyword}&s=exact-aware-popularity-rank&dc&page={page_num}')
    # fetchEbay("graphics+card", 1, 'https://www.ebay.com/sch/i.html?_from=R40&_nkw="{keyword}"&_sacat=0&LH_TitleDesc=0&_fsrp=1&_sop=15&_pgn={page_num}')
    args = sys.argv[1:]
    if len(args) != 0:
        for arg in args:
            quickSearchAndCompare(args)
    
        
if __name__ == '__main__':
    main()
