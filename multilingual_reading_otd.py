import requests
from bs4 import BeautifulSoup

url = "https://www.aelf.org/"

def extract_substr_btw_end_brackets(my_str):
    pos = my_str.find("(")
    return my_str[pos+1:len(my_str)-1]

def reading_otd():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    my_dict = {}
    i = 1
    while (soup.find("div", id="messe1_lecture" + str(i)) is not None):
        div = soup.find("div", id="messe1_lecture" + str(i))
        my_dict[div.find("h4").text] = extract_substr_btw_end_brackets(div.find("h5").text)
        i += 1

    return my_dict

print(reading_otd())