import sys
from requests_html import HTMLSession


def fetchBook(urlString='https://www.royalroad.com/fiction/36049/the-primal-hunter/chapter/998105/chapter-503-truly-evil-dungeon-design', book=None, session=None):
    if urlString is None:
        return book.close()

    if book is None:
        book = open('book/temp.txt', '+a')

    if session is None:
        session = HTMLSession()

    try:
        response = session.get(urlString.strip())
        content = response.html.find('div.chapter-inner', first=True)
        text = content.text
        next = response.html.find('div.row.nav-buttons', first=True)
        if len(next.links) != 2:
            nextUrlString = None
        else:
            next_link = response.html.find('a.btn-primary', containing='Next', first=True)
            nextUrlString = 'https://www.royalroad.com' + next_link.attrs['href']

        print(nextUrlString)
        book.write(text + '\n')

        if nextUrlString:
            fetchBook(nextUrlString, book, session)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

        
def main():
    print("only set up for royalroad atm")
    args = sys.argv[1:]
    session = HTMLSession()

    try:
        if len(args) != 0:
            for url in args:
                fetchBook(url, None, session)
        else:
            fetchBook()

    finally:
        session.close()


if __name__ == '__main__':
    main()