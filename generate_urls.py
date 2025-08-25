import datetime
from sys import argv


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


if __name__ == '__main__':
    try:
        delta = int(argv[1])
    except:
        delta = 10

    for my_dict in generate_urls_delta(delta = delta):
        print(my_dict)
