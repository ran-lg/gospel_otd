import requests
import re
from bs4 import BeautifulSoup


# extracts the gospel for a given day url, e.g. 'Mt 23, 13-22'

def get_gospel_otd(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for li in soup.find_all('li'):
        if '>Évangile<' in str(li):

            regex1 = r'ref">(.*)<'
            result = re.search(regex1, str(li))
            my_str = result.group(1)
            my_str = my_str.replace(u'\xa0', ' ')
            my_str = my_str.replace('...', ' ')
            my_str = my_str.replace('–', '-')

           
            my_str = my_str.replace(' - ', '-')
            
            while '  ' in my_str:
                my_str = my_str.replace('  ', ' ')

            regex2 = r' \(.*| \[.*'
            for occurrence in re.findall(regex2, my_str):
                my_str = my_str.replace(occurrence, '')

            return my_str
    return ''

if __name__ == '__main__':
    gospel_otd = get_gospel_otd('https://www.aelf.org/2025-08-26/romain/messe')
    print(gospel_otd)
