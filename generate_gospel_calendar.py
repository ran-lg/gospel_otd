from extract_gospel import get_gospel_otd
from generate_urls import generate_urls_delta
from sys import argv


if __name__ == '__main__':
    try:
        delta = int(argv[1])
    except:
        delta = 5

    dict_list = generate_urls_delta(delta)
    for my_dict in dict_list:
        my_dict['gospel_otd'] = get_gospel_otd(my_dict['url'])

    for my_dict in dict_list:
        print(my_dict)
