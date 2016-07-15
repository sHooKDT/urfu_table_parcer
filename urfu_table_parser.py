import re
import psycopg2
import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_abi(html_soup):
    attrs = html_soup.find_all('td')
    abi0 = {}
    try:
        abi0 = {
            'name1': attrs[0].text.split()[0],
            'name2': attrs[0].text.split()[1],
            'name3': attrs[0].text.split()[2],
            'reg_num': attrs[1].text,
            'doc_type': attrs[3].text,
            'math': attrs[4].text.split()[0],
            'informatics': attrs[5].text.split()[0],
            'rus': attrs[6].text.split()[0],
            'sum': attrs[8].text
        }
    except:
        print(attrs)
        abi0 = {
            'name1': 'error',
            'name2': 'error',
            'name3': 'error',
            'reg_num': attrs[1].text,
            'doc_type': attrs[3].text,
            'math': attrs[4].text.split()[0],
            'informatics': attrs[5].text.split()[0],
            'rus': attrs[6].text.split()[0],
            'sum': attrs[8].text
        }
    return abi0


def get_cs(conn, cursor):
    html = get_html("http://urfu.ru/ru/ratings/form-1/?d=6&f=1&cHash=b54214732dd6be74e0b7cdf5e62efc9e")
    soup = BeautifulSoup(html, "html.parser")
    table_dir = soup.find('table', id='2127716394')
    table_main = table_dir.find_next('table').find_next('table')
    list_abi = table_main.find_all('tr', class_='tr-odd')
    for abi in list_abi:
        r = get_abi(abi)
        sql = "INSERT INTO cs VALUES('{0}','{1}','{2}',{3},'{4}',{5},{6},{7},{8})" \
            .format(r['name1'], r['name2'], r['name3'], r['reg_num'], r['doc_type'],
                    r['math'], r['informatics'], r['rus'], r['sum'])
        print(sql)
        cursor.execute(sql)
    conn.commit()


def get_info(conn, cursor):
    html = get_html("http://urfu.ru/ru/ratings/form-1/?d=6&f=1&cHash=b54214732dd6be74e0b7cdf5e62efc9e")
    soup = BeautifulSoup(html, "html.parser")
    table_dir = soup.find('table', id='203198546')
    table_main = table_dir.find_next('table').find_next('table')
    list_abi = table_main.find_all('tr', class_='tr-odd')
    for abi in list_abi:
        r = get_abi(abi)
        sql = "INSERT INTO info VALUES('{0}','{1}','{2}',{3},'{4}',{5},{6},{7},{8})" \
            .format(r['name1'], r['name2'], r['name3'], r['reg_num'], r['doc_type'],
                    r['math'], r['informatics'], r['rus'], r['sum'])
        print(sql)
        cursor.execute(sql)
    conn.commit()


def get_rtf(conn, cursor):
    html = get_html("http://urfu.ru/ru/ratings/form-1/?d=8&f=1&cHash=3db73675c26b0ab7d5fe7b85b345dd63")
    soup = BeautifulSoup(html, "html.parser")
    table_dir = soup.find('table', id='215849506')
    table_main = table_dir.find_next('table').find_next('table')
    list_abi = table_main.find_all('tr', class_='tr-odd')
    for abi in list_abi:
        r = get_abi(abi)
        sql = "INSERT INTO rtf VALUES('{0}','{1}','{2}',{3},'{4}',{5},{6},{7},{8})" \
            .format(r['name1'], r['name2'], r['name3'], r['reg_num'], r['doc_type'],
                    r['math'], r['informatics'], r['rus'], r['sum'])
        print(sql)
        cursor.execute(sql)
    conn.commit()


def main():
    try:
        conn = psycopg2.connect("dbname='urfu2016' user='postgres' host='localhost' password='postgres'")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS cs")
        cursor.execute("DROP TABLE IF EXISTS info")
        cursor.execute("DROP TABLE IF EXISTS rtf")
        cursor.execute("CREATE TABLE cs (name1 varchar, name2 varchar, name3 varchar, reg_num integer,"
                       "doc_type varchar, math integer, informatics integer, rus integer, sum integer)")
        cursor.execute("CREATE TABLE info (name1 varchar, name2 varchar, name3 varchar, reg_num integer,"
                       "doc_type varchar, math integer, informatics integer, rus integer, sum integer)")
        cursor.execute("CREATE TABLE rtf (name1 varchar, name2 varchar, name3 varchar, reg_num integer,"
                       "doc_type varchar, math integer, informatics integer, rus integer, sum integer)")
        conn.commit()
    except:
        print('cannot connect to database!')

    get_cs(conn, cursor)
    get_info(conn, cursor)
    get_rtf(conn, cursor)


if __name__ == '__main__':
    main()
