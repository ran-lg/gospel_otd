from extract_gospel import get_gospel_otd
from generate_urls import generate_urls_delta


if __name__ == '__main__':
    dict_list = generate_urls_delta(delta = 50)
    for my_dict in dict_list:
        my_dict['gospel_otd'] = get_gospel_otd(my_dict['url'])

    for my_dict in dict_list:
        print(my_dict)
