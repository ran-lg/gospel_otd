import requests
from bs4 import BeautifulSoup

# returns the position of the string's first digit
#         -1 if there is no digit

def determine_pos_first_digit(my_str, char_nb = 0):
    i = char_nb
    while ((i<len(my_str)) and (ord(my_str[i]) < 48 or ord(my_str[i]) > 57)):
        i += 1

    if (i<len(my_str)):
        return i
    else:
        return -1

def extract_substr_right_of_comma(my_str):
    pos = my_str.find(",")
    return my_str[pos+1:len(my_str)-1]

def extract_substr_left_of_comma(my_str):
    pos = my_str.find(",")
    return my_str[0:pos]

def extract_substr_btw_end_brackets(my_str):
    pos = my_str.find("(")
    return my_str[pos+1:len(my_str)-1]

def delete_nbreaking_spaces(my_str):
    return my_str.replace(u"\xa0", u"")

# extracts the readings of url

def get_readings(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    my_list = []
    i = 1
    while (soup.find("div", id="messe1_lecture" + str(i)) is not None):
        div = soup.find("div", id="messe1_lecture" + str(i))
        my_list.append(div.find("h4").text + "*" + delete_nbreaking_spaces(extract_substr_btw_end_brackets(div.find("h5").text)))
        i += 1

    return my_list

print(get_readings("https://www.aelf.org/2025-04-20/romain/messe"))