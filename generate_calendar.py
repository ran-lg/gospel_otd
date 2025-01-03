import datetime
from extract_readings import get_readings

def generate_dates_d1_to_d150():
    my_list = []
    my_date = datetime.datetime.now() + datetime.timedelta(days=1)
    i = 1
    while (i<151):
        my_list.append(my_date.strftime("%Y") + "-" + my_date.strftime("%m") + "-" + my_date.strftime("%d"))
        my_date += datetime.timedelta(days=1)
        i += 1
    return my_list

def generate_urls_d0_to_d150():
    my_list = ["https://www.aelf.org/"]
    for d in generate_dates_d1_to_d150():
        my_list.append("https://www.aelf.org/" + d + "/romain/messe")
    return my_list


for url in generate_urls_d0_to_d150():
    print(url)
    print(get_readings(url)[1])