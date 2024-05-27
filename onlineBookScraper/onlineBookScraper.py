import random
import sys
import threading
import re
import time

from requests_html import HTMLSession
from requests_html import HTML
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def fetchBook(urlString=None, book=None, session=None):
    if urlString is None or urlString == '' or urlString == '\n':
        print("received empty or invalid input")
        return -1
    if (str(urlString).find("royalroad.com") != -1):
        return fetchBookRR(urlString, book, session) 
    elif (str(urlString).find("fanfiction.net") != -1):
        fetchBookFF(urlString, book, session)
        return 1
    elif (str(urlString).find("forums.spacebattles.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return fetchBookForum(urlString, book, session, 'https://forums.spacebattles.com')
    elif (str(urlString).find("forums.sufficientvelocity.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return fetchBookForum(urlString, book, session, 'https://forums.sufficientvelocity.com')
    elif (str(urlString).find("forum.questionablequesting.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return fetchBookQQ(urlString, book, session, 'https://forum.questionablequesting.com/')
    else:
        print("failed to parse URL")
        return -1
    

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
            title = trimTitle(title)
            book = open(f'onlineBookScraper/book/{title}.txt', 'w', encoding='utf-8')

        book.write(text + '\n')
        print(nextUrlString)

        if nextUrlString:
            fetchBookRR(nextUrlString, book, session)
            
    except Exception as e:
        print(f"An error occurred in fetchRoyal: {str(e)}")
        if book:
            book.close()
        return -1

    finally:
        if session:
            session.close()
        return 1
            
def fetchBookFF(urlString=None, book=None, session=None):
    if urlString is None:
        session.quit()
        return book.close()
    tempString = urlString
    try:
        if session is None:
            options = uc.ChromeOptions()
            options.add_argument('--disable-extensions')
            options.add_argument("--auto-open-devtools-for-tabs")
            options.add_argument('--disable-gpu')
            options.add_argument("--incognito")
            options.add_argument("--disable-plugins-discovery")
            options.add_argument("--start-maximized")
            options.add_argument('--no-sandbox')
            session = uc.Chrome(headless=True, options=options)
            session.delete_all_cookies()
            session.set_page_load_timeout(15)
            wait = WebDriverWait(session, 15)
            session.get(urlString.strip())
            time.sleep(5.153)
            # solveCaptcha(session, wait)
            wait = WebDriverWait(session, 15)
        else:
            session.set_page_load_timeout(15)
            wait = WebDriverWait(session, 15)
            session.get(urlString.strip())

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.storytext')))
        response = HTML(html=session.page_source)
        time.sleep(1.095)
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
            title = trimTitle(title)
            book = open(f'book/{title}.txt', 'w', encoding='utf-8')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookFF(nextUrlString, book, session)
        session.close()
        session.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if session is not None:
            rand = random.randint(0,1)
            if (rand == 0):
                print("assuming captcha")
                solveCaptcha(session, wait)
                print("trying again...")
                fetchBookFF(tempString, book, session)
            else:
                print("restarting and trying again...")
                session.close()
                session.quit()
                fetchBookFF(tempString, book, None)

def fetchBookForum(urlString=None, book=None, session=None, baseUrl=None):
    if urlString is None:
        return book.close()

    try:
        if session is None:
            session = HTMLSession()

        response = session.get(urlString.strip())
        content = response.html.find('div.bbWrapper')
        prev =  next = response.html.find('a.pageNav-jump--prev', first=True)
        if (prev is None):
            text = ''.join(block.text for block in content[1:])
        else:
            text = ''.join(block.text for block in content[0:])
        next = response.html.find('a.pageNav-jump--next', first=True)
        if (next is None) :
            nextUrlString = None
        else:
            next_link = next.attrs['href']
            nextUrlString = baseUrl + next_link

        if book is None:
            title = response.html.find('title', first=True).text
            title = trimTitle(title)
            book = open(f'onlineBookScraper/book/{title}.txt', 'w', encoding='utf-8')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookForum(nextUrlString, book, session, baseUrl)

    except Exception as e:
        print(f"An error occurred in fetchBookForum: {str(e)}")
        if book:
            book.close()
        return -1

    finally:
        if session:
            session.close()
        return 1

def fetchBookQQ(urlString=None, book=None, session=None, baseUrl=None, auth=None):
    if urlString is None:
        return book.close()

    try:
        if auth is None:
            QQUSERNAME = 'example.mail.com',
            QQPASSWORD = 'yourPassword'
            auth = {
                'login':QQUSERNAME,
                'register' : 0,
                'password':QQPASSWORD,
                'cookie_check':1,
                '_xfToken': '',
                'redirect':'https://forum.questionablequesting.com/'
                }
        if session is None:
            
            session = HTMLSession()
            payload = auth
            get = session.get('https://forum.questionablequesting.com/login')
            post = session.post('https://forum.questionablequesting.com/login/login', data = payload)

        response = session.get(urlString.strip())
        content = response.html.find('article')
        text = ''.join(block.text for block in content)
        next = response.html.find('a.text', containing='Next', first=True)
        if (next is None) :
            nextUrlString = None
        else:
            next_link = next.attrs['href']
            nextUrlString = baseUrl + next_link

        if book is None:
            title = response.html.find('title', first=True).text
            title = trimTitle(title)
            book = open(f'onlineBookScraper/book/{title}.txt', 'w', encoding='utf-8')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBookQQ(nextUrlString, book, session, baseUrl)

    except Exception as e:
        print(f"An error occurred in fetchBookQQ: {str(e)}")
        if book:
            book.close()
        return -1

    finally:
        if session:
            session.close()
        return 1

def solveCaptcha(session, wait):
    i = random.random()
    k = random.randint(1,2) + i*1.22
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe')))
    time.sleep(1.502 + k)
    session.switch_to.frame(session.find_element(By.CSS_SELECTOR, 'iframe'))
    time.sleep(.732 + k)
    session.find_element(By.CSS_SELECTOR, 'input').click()
    session.switch_to.default_content()
    time.sleep(4.232 + k)

def trimTitle(title):
    title = title.replace(" ", "")
    title = title.replace("/", "_")
    title = title.replace("|", "_")
    title = title.replace(":", "_")
    title = title.replace("{", "_")
    title = title.replace("}", "_")
    title = title.replace("[", "_")
    title = title.replace("]", "_")
    title = title.replace("=", "_")
    return title

def input_loop():
        while True:
            url = input("Enter a URL (or 'q' to stop listening):\n => ")
            if url.lower() == "q":
                break
            t = threading.Thread(target=fetchBook, args=(url, None, None))
            t.start()

def main():
    
    print("fully set up for royalroad | fanfiction.net is rather buggy, but works. You can manually pass the captcha by changing the uc.Chrome(headless=True, ...) to False, visa versa | forums. sites, ex. forums.spacebattles.com, forums.sufficientvelocity.com | works for sites where you've got login creds and how they're formatted")
    args = sys.argv[1:]
    # args = ['https://www.fanfiction.net//s/12952720/1/The-Crimson-Sorcerer'] #for debugging, comment out before actual use with CLI
    # print("Debugging Mode! CLI args not being used!") # debug statement

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
