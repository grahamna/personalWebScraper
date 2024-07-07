import sys
import threading

import sampleScrapers

def fetchBook(urlString=None, book=None, session=None):
    # It's possible that I should swap this to a case: statement instead... scope has grown
    
    if urlString is None or urlString == '' or urlString == '\n':
        print("received empty or invalid input")
        return -1
    if (str(urlString).find("royalroad.com") != -1):
        return sampleScrapers.fetchBookRR(urlString, book, session) 
    elif (str(urlString).find("fanfiction.net") != -1):
        sampleScrapers.fetchBookFF(urlString, book, session)
        return 1
    elif (str(urlString).find("forums.spacebattles.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return sampleScrapers.fetchBookForum(urlString, book, session, 'https://forums.spacebattles.com')
    elif (str(urlString).find("forums.sufficientvelocity.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return sampleScrapers.fetchBookForum(urlString, book, session, 'https://forums.sufficientvelocity.com')
    elif (str(urlString).find("forum.questionablequesting.com") != -1):
        if (str(urlString).find("#post") != -1 or str(urlString).find("/reader") == -1):
            urlPart = urlString.split('#post')
            urlString = urlPart[0]+ 'reader'
        return sampleScrapers.fetchBookQQ(urlString, book, session)
    elif (str(urlString).find("lightnovelworld.co") != -1):
        return sampleScrapers.fetchLightNovel(urlString, book, session, 'https://www.lightnovelworld.co')
    else:
        print("failed to parse URL")
        return -1

def inputLoop():
        while True:
            url = input("Enter a URL (or 'q' to stop listening):\n => ")
            if url.lower() == "q":
                break
            thread = threading.Thread(target=fetchBook, args=(url, None, None))
            thread.start()

def main():
    
    print("You can manually pass the captcha by changing the uc.Chrome(headless=True, ...) to False, visa versa | forums. sites, ex. forums.spacebattles.com, forums.sufficientvelocity.com | works for sites where you've got login creds and how they're formatted. For other sites, you must create the particular scraper yourself using browser development tools.")
    args = sys.argv[1:]
    # args = ['https://www.fanfiction.net//s/12952720/1/The-Crimson-Sorcerer'] #for debugging, comment out before actual use with CLI
    # print("Debugging Mode! CLI args not being used!") # debug statement
    
    # Default recursive calls' limits are at ~1000, but often online fanfiction has over 1000 chapters, this increases the depth limit for these loops to 10,000
    sys.setrecursionlimit(10**4)

    try:
        if len(args) != 0:
            threads = []
            for url in args:
                singleThread = threading.Thread(target=fetchBook, args=(url, None, None))
                threads.append(singleThread)
                singleThread.start()

            for singleThread in threads:
                singleThread.join()
        else:
            print("No CLI args detected")
            inputThread = threading.Thread(target=inputLoop)
            inputThread.start()
            inputThread.join()

    except Exception as e:
        print(f"An error occurred in main: {str(e)}")


if __name__ == '__main__':
    main()
