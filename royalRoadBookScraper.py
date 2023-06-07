import sys
import threading
from requests_html import HTMLSession


def fetchBook(urlString=None, book=None, session=None):
    if urlString is None:
        return book.close()

    try:
        if session is None:
            session = HTMLSession()

        response = session.get(urlString.strip())
        content = response.html.find('div.chapter-inner', first=True)
        text = content.text
        next = response.html.find('div.row.nav-buttons', first=True)
        if len(next.links) != 2:
            nextUrlString = None
        else:
            next_link = response.html.find('a.btn-primary', containing='Next', first=True)
            nextUrlString = 'https://www.royalroad.com' + next_link.attrs['href']

        if book is None:
            title = response.html.find('title', first=True).text
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)

        if nextUrlString:
            fetchBook(nextUrlString, book, session)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if book:
            book.close()

    finally:
        if session:
            session.close()


def main():
    print("only set up for royalroad atm")
    args = sys.argv[1:]

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
            print("You must provide a URL as a CLI Argument \n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
