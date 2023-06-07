import sys
from requests_html import HTMLSession


def fetchBook(urlString=None, book=None, session=None):
    if urlString is None:
        return book.close()

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

        if book is None:
            title = response.html.find('title', first=True).text
            book = open(f'book/{title}.txt', 'w')

        book.write(text + '\n')

        print(nextUrlString)
        
        if nextUrlString:
            fetchBook(nextUrlString, book, session)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.close()
        if book:
            book.close()

        
def main():
    print("Only set up for Royal Road at the moment.")
    args = sys.argv[1:]
    session = HTMLSession()

    if len(args) != 0:
        try:
            for url in args:
                fetchBook(url, None, session)
        except:
            print("An error occurred while processing the URLs.")
    else:
        print("You must provide a URL as a CLI argument.\n")

    session.close()


if __name__ == '__main__':
    main()
