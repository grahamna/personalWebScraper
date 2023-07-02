import sys
import threading
import re
from requests_html import HTMLSession
from requests_html import HTML
import undetected_chromedriver as uc
import time


def fetchBook(urlString=None, book=None, session=None):
    if (str(urlString).find("royalroad.com") != -1):
        fetchBookRR(urlString, book, session)
    elif (str(urlString).find("fanfiction.net") != -1):
        fetchBookFF(urlString, book, session)
    elif (str(urlString).find("forums.spacebattles.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        fetchBookForum(urlString, book, session, 'https://forums.spacebattles.com')
    elif (str(urlString).find("forums.sufficientvelocity.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        fetchBookForum(urlString, book, session, 'https://forums.sufficientvelocity.com')

def fetchBookRR(urlString=None, book=None, session=None):
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
            title = title.replace(" ", "")
            title = title.replace("/", "-")
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookRR(nextUrlString, book, session)

    except Exception as e:
        print(f"An error occurred in fetchRoyal: {str(e)}")
        if book:
            book.close()

    finally:
        if session:
            session.close()
            
def fetchBookFF(urlString=None, book=None, session=None):
    if urlString is None:
        session.quit()
        return book.close()
    tempString = urlString
    try:
        if session is None:
            session = uc.Chrome(headless=True, use_subprocess=True)
            session.set_page_load_timeout(15)
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
            title = title.replace(" ", "")
            title = title.replace("/", "-")
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookFF(nextUrlString, book, session)
        session.quit()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if session is not None:
            session.quit()
            print("session closed for restart")
        print("Trying Again... press ctrl C to stop")
        fetchBookFF(tempString, book, None)

def fetchBookForum(urlString=None, book=None, session=None, baseUrl=None):
    if urlString is None:
        return book.close()

    try:
        if session is None:
            session = HTMLSession()

        response = session.get(urlString.strip())
        content = response.html.find('div.bbWrapper')
        text = ''.join(block.text for block in content[1:])
        next = response.html.find('a.pageNav-jump--next', first=True)
        if (next is None) :
            nextUrlString = None
        else:
            next_link = next.attrs['href']
            nextUrlString = baseUrl + next_link

        if book is None:
            title = response.html.find('title', first=True).text
            title = title.replace(" ", "")
            title = title.replace("/", "-")
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookForum(nextUrlString, book, session, baseUrl)

    except Exception as e:
        print(f"An error occurred in fetchBookForum: {str(e)}")
        if book:
            book.close()

    finally:
        if session:
            session.close()

def input_loop():
        while True:
            url = input("Enter a URL (or 'q' to stop listening): ")
            if url.lower() == "q":
                break
            t = threading.Thread(target=fetchBook, args=(url, None, None))
            t.start()

def main():
    
    print("fully set up for royalroad | fanfiction.net is rather buggy, but works. You can manually pass the captcha by changing the uc.Chrome(headless=True, ...) to False, visa versa | forums. sites, ex. forums.spacebattles.com, forums.sufficientvelocity.com | ")
    args = sys.argv[1:]
    args = ['https://www.fanfiction.net/s/14227295/1/Os-Marotos-O-Livro-das-Sombras','https://www.fanfiction.net/s/14051246/1/Hermione-s-Trip-to-the-Past-Creating-A-New-Future'] #for debugging, comment out before actual use with CLI
    print("Debugging Mode! CLI args not being used!") # debug statement

    try:
        if len(args) != 0:
            threads = []
            for url in args:
                t = threading.Thread(target=fetchBook, args=(url, None, None))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        else:
            print("No CLI args detected")
            input_thread = threading.Thread(target=input_loop)
            input_thread.start()
            input_thread.join()

    except Exception as e:
        print(f"An error occurred in main: {str(e)}")


if __name__ == '__main__':
    main()
