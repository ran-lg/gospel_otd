from sys import argv
import re
from bs4 import BeautifulSoup
import requests
import datetime


# if delta = 2 and today's date is 25/08/2025,
#
#   generate [{'date': 2025-08-23, 'url': 'https://www.aelf.org/2025-08-23/romain/messe'}, 
#             {'date': 2025-08-24, 'url': 'https://www.aelf.org/2025-08-24/romain/messe'}, 
#             {'date': 2025-08-25, 'url': 'https://www.aelf.org/2025-08-25/romain/messe'}, 
#             {'date': 2025-08-26, 'url': 'https://www.aelf.org/2025-08-26/romain/messe'}, 
#             {'date': 2025-08-27, 'url': 'https://www.aelf.org/2025-08-27/romain/messe'}] 

def generate_urls_delta(delta = 10):
    today = datetime.datetime.now()
    days = [{'date': today, 'url': 'https://www.aelf.org/'}]
    
    for i in range(1, delta + 1):
        day_x = today + i * datetime.timedelta(days = 1)
        day_y = today - i * datetime.timedelta(days = 1)
        
        url_x = 'https://www.aelf.org/' + day_x.strftime('%Y-%m-%d') + '/romain/messe'
        url_y = 'https://www.aelf.org/' + day_y.strftime('%Y-%m-%d') + '/romain/messe'
        
        days.append({'date': day_x, 'url': url_x})
        days.append({'date': day_y, 'url': url_y})
    
    return days

# if alpha = 2 and today's date is 25/08/2025,
#
#   generate [{'date': 2025-08-25, 'url': 'https://www.aelf.org/2025-08-25/romain/messe'}, 
#             {'date': 2025-08-26, 'url': 'https://www.aelf.org/2025-08-26/romain/messe'}, 
#             {'date': 2025-08-27, 'url': 'https://www.aelf.org/2025-08-27/romain/messe'}] 

def generate_urls_alpha(alpha = 10):
    today = datetime.datetime.now()
    days = [{'date': today, 'url': 'https://www.aelf.org/'}]
    
    for i in range(1, alpha + 1):
        day_x = today + i * datetime.timedelta(days = 1)
        url_x = 'https://www.aelf.org/' + day_x.strftime('%Y-%m-%d') + '/romain/messe'
        days.append({'date': day_x, 'url': url_x})
    
    return days

# extracts the gospel for a given day url, e.g. 'Mt 23,13-22'

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

# if delta = 2 and today's date is 25/08/2025,
#
#   generate [{'date': 2025-08-23, 'gospel_otd': 'Lc 4, 31-37'}, 
#             {'date': 2025-08-24, 'gospel_otd': 'Mt 1, 20-30'}, 
#             {'date': 2025-08-25, 'gospel_otd': 'Jn 5, 10-29'}, 
#             {'date': 2025-08-26, 'gospel_otd': 'Mc 3, 10-15'}, 
#             {'date': 2025-08-27, 'gospel_otd': 'Lc 16, 21-25'}] 

def get_gospel_delta(delta = 10):
    dict_list = generate_urls_delta(delta)

    for my_dict in dict_list:
        my_dict['gospel_otd'] = get_gospel_otd(my_dict['url'])
        my_dict.pop('url')

    return dict_list

# if delta = 2 and today's date is 25/08/2025,
#
#   generate [{'date': 2025-08-25, 'gospel_otd': 'Lc 4, 31-37'}, 
#             {'date': 2025-08-26, 'gospel_otd': 'Mt 1, 20-30'}, 
#             {'date': 2025-08-27, 'gospel_otd': 'Jn 5, 10-29'}, 

def get_gospel_alpha(alpha = 10):
    dict_list = generate_urls_alpha(alpha)

    for my_dict in dict_list:
        my_dict['gospel_otd'] = get_gospel_otd(my_dict['url'])
        my_dict.pop('url')

    return dict_list


if __name__ == '__main__':
    try:
        delta = int(argv[1])
    except:
        delta = 5

    for my_dict in get_gospel_delta():
        print(my_dict)
