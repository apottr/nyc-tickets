from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test.html').read(),'html.parser')

one = soup.find_all('tr',class_='cellWhite')
two = soup.find_all('tr',class_='cellLightBlue')

def strip_whitespace(lst):
    out = []
    for item in lst:
        out.append(item.strip())
    return out

for item in one+two:
    for col in item.find_all('td',attrs={'width': '40'}):
        lst = col.find('a')['href'].split('\r\n')
        if len(lst) > 1:
            print strip_whitespace(lst)[4:]
