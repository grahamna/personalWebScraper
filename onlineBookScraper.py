import sys
import threading
import re
from requests_html import HTMLSession
from requests_html import HTML
import undetected_chromedriver as uc
import time


def fetchBook(urlString=None, book=None, session=None):
    if (str(urlString).find("royalroad.com") != -1):
        fetchBookRoyalRoad(urlString, book, session)
    elif (str(urlString).find("fanfiction.net") != -1):
        fetchBookFanfiction(urlString, book, session)

def fetchBookRoyalRoad(urlString=None, book=None, session=None):
    if urlString is None:
        return book.close()

    try:
        if session is None:
            session = HTMLSession()

        response = session.get(urlString.strip())
        content = response.html.find('div.chapter-inner', first=True)
        text = content.text
        next = response.html.find('div.row.nav-buttons', first=True)
        next_link = response.html.find('a.btn-primary', containing='Next', first=True)
        if (next_link is None and len(next.links) != 2) :
            nextUrlString = None
        else:
            nextUrlString = 'https://www.royalroad.com' + next_link.attrs['href']

        if book is None:
            title = response.html.find('title', first=True).text
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookRoyalRoad(nextUrlString, book, session)

    except Exception as e:
        print(f"An error occurred in fetchRoyal: {str(e)}")
        if book:
            book.close()

    finally:
        if session:
            session.close()
            
            
def fetchBookFanfiction(urlString=None, book=None, session=None):
    if urlString is None:
        session.quit()
        return book.close()
    tempString = urlString
    try:
        if session is None:
            session = uc.Chrome(headless=True, use_subprocess=False)
            session.get(urlString.strip())
            time.sleep(15)
        else:
            session.set_page_load_timeout(10)
            session.get(urlString.strip())

        response = HTML(html=session.page_source)
        content = response.find('div.storytext', first=True)
        text = content.text
        next = response.find('button.btn', containing="Next", first=True)
        if (next is None) :
            nextUrlString = None
        else:
            urlStr = re.search(r"self\.location='(.*?)'", next.html).group(1)
            nextUrlString = 'https://www.fanfiction.net' + urlStr

        if book is None:
            title = session.title
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookFanfiction(nextUrlString, book, session)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}\nTrying Again... hold ctrl C to stop")
        fetchBookFanfiction(tempString, book, None)


def main():
    
    print("fully set up for royalroad | fanfiction.net is rather buggy ")
    args = sys.argv[1:]
    args = ['https://www.fanfiction.net/s/11873195/1/I-m-Defying-Gravity', 'https://www.royalroad.com/fiction/51925/a-sith-during-the-fall/chapter/855731/1-not-the-korriban-i-know', 'https://www.royalroad.com/fiction/31514/the-menocht-loop/chapter/903696/the-trials-of-descent-261-ominous-promise', 'https://www.fanfiction.net/s/14205444/1/Enchanting-Melodies'] #for debugging, comment out for actual use
    try:
        if len(args) != 0:
            threads = []
            for url in args:
                print(url)
                t = threading.Thread(target=fetchBook, args=(url, None, None))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        else:
            print("You must provide a URL as a CLI Argument \n")

    except Exception as e:
        print(f"An error occurred in main: {str(e)}")


if __name__ == '__main__':
    main()
