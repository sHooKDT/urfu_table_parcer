import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_abi(html_soup):
    attrs = html_soup.find_all('td')
    return {
        'name': attrs[0].text,
        'reg_num': attrs[1].text,
        'doc_type': attrs[3].text,
        'math': attrs[4].text,
        'informatics': attrs[5].text,
        'rus': attrs[6].text,
        'sum': attrs[8].text
    }


def main():
    html = get_html("http://urfu.ru/ru/ratings/form-1/?d=6&f=1&cHash=b54214732dd6be74e0b7cdf5e62efc9e")
    soup = BeautifulSoup(html, "html.parser")
    table_dir = soup.find('table', id='2127716394')
    table_main = table_dir.find_next('table').find_next('table')
    list_abi = table_main.find_all('tr', class_='tr-odd')
    for abi in list_abi:
        print(get_abi(abi))


if __name__ == '__main__':
    main()
