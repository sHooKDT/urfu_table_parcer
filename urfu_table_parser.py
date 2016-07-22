import re
import psycopg2
import urllib.request
from bs4 import BeautifulSoup

def connect_db():
    try:
        conn = psycopg2.connect("dbname='urfu2016' user='postgres' host='46.101.8.217' password='postgres'")
        cursor = conn.cursor()
    except:
        print('Database connection failed.')
    return conn, cursor

def clear_db(conn, cursor):
    cursor.execute("DROP TABLE IF EXISTS applicants")
    cursor.execute("CREATE TABLE applicants (name varchar, id integer, is_prefer boolean, is_orig boolean, p_math integer, p_it integer, p_rus integer, p_extra integer, total integer, fac integer)")
    cursor.execute("DROP TABLE IF EXISTS facults")
    cursor.execute("CREATE TABLE facults (name varchar, id integer, comment varchar, places integer)")
    conn.commit()

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_facs(html):
    soup = BeautifulSoup(html, "html.parser")
    facs_list = []
    for fac in soup.findAll('table', id=True):
        try:
            expr = re.compile("""(.*) - план приема (\d*)""")
            parsed_string = re.match(expr, fac.find_next('div').string)
            facs_list.append({
                'name': fac.find('b').string,
                'id': fac.attrs['id'],
                'comment': parsed_string.group(1),
                'places': parsed_string.group(2)
            })
        except:
            print("Fail to parse some faculty")
    return facs_list

def insert_facs(conn, cursor, facs):
    for fac in facs:
        sql = "INSERT INTO facults VALUES('{name}',{id},'{comment}',{places})".format(**fac)
        cursor.execute(sql)
    conn.commit()

def get_applicants(html, _id):
    soup = BeautifulSoup(html, "html.parser")
    table_dir = soup.find('table', id=_id).find_next('table').find_next('table')
    raw_list = table_dir.find_all('tr', class_='tr-odd')
    applicants = []
    for row in raw_list:
        attrs = row.find_all('td')
        try:
            p_extra = int(attrs[7].text)
        except:
            p_extra = 0
        try:
            applicants.append({
                'name': " ".join(attrs[0].text.split(" ")[0:3]),
                'id': attrs[1].text,
                'is_prefer': attrs[2].text != "",
                'is_orig': attrs[3].text == "оригинал",
                'p_math': attrs[4].text.split()[0],
                'p_it': attrs[5].text.split()[0],
                'p_rus': attrs[6].text.split()[0],
                'p_extra': p_extra,
                'total': attrs[8].text,
                'fac': _id
            })
        except:
            applicants.append({
                'name': attrs[0].text,
                'id': attrs[1].text,
                'is_prefer': attrs[2].text != "",
                'is_orig': attrs[3].text == "оригинал",
                'p_math': 100,
                'p_it': 100,
                'p_rus': 100,
                'p_extra': 10,
                'total': 310,
                'fac': _id
            })
        print(applicants[-1])
    return applicants

def insert_applicants(conn, cursor, applicants):
    for applicant in applicants:
        sql = "INSERT INTO applicants VALUES('{name}',{id}, {is_prefer}, {is_orig}, {p_math}, {p_it}, {p_rus}, {p_extra}, {total}, {fac})".format(**applicant)
        cursor.execute(sql)
    conn.commit()


def main():
    global html
    global facs
    # Connect to db and clear 'applicants' table
    # Database scheme: name varchar, id integer, is_prefer boolean, is_orig boolean, p_math integer, p_it integer, p_rus integer, p_extra integer, total integer

    conn, cursor = connect_db()
    clear_db(conn, cursor)

    insts = [6, 8]

    for inst in insts:
        html = get_html("http://urfu.ru/ru/ratings/form-1/?d={0}&f=1".format(inst))
        facs = get_facs(html)
        insert_facs(conn, cursor, facs)
        for fac in facs:
            insert_applicants(conn, cursor, get_applicants(html, fac["id"]))



if __name__ == '__main__':
    main()
