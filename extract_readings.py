import requests
import re
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

# creates a dict related to the fragments read, e.g.
# "Jn 3, 7b- 15"
#
# {book: "Jn",
#  beginning1_chapter: "3",
#  beginning1_verse: "7",
#  beginning1_letter: "b",
#  end1_chapter: "3",
#  end1_verse: "15",
#  end1_letter: "",
#  beginning2_chapter: "",
#  beginning2_verse: "",
#  beginning2_letter: "",
#  end2_chapter: "",
#  end2_verse: "",
#  end2_letter: "",
#  beginning3_chapter: "",
#  beginning3_verse: "",
#  beginning3_letter: "",
#  end3_chapter: "",
#  end3_verse: "",
#  end3_letter: ""}

def gospel_dict (my_str):
    gospel = my_str[0:2]
    my_str = my_str[3:]
    
    my_dict = {}
    my_dict["book"] = gospel

    segments = my_str.split(",")

    i = 1
    while len(segments) > 0:
        match i:
            case 1:
                my_dict["beginning1_chapter"] = segments[0]
            case 2:
                my_dict["beginning1_verse"] = segments[0]
            case 3:
                my_dict["beginning1_letter"] = segments[0]
                
        segments.pop(0)

    return my_dict



# extracts the readings of url

def get_readings(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    my_list = []
    i = 1
    while (soup.find("div", id="messe1_lecture" + str(i)) is not None):
        div = soup.find("div", id="messe1_lecture" + str(i))

        if "Évangile" in div.find("h4").text:
            my_list.append([div.find("h4").text, gospel_dict(delete_nbreaking_spaces(extract_substr_btw_end_brackets(div.find("h5").text)))])
        
        i += 1

    return my_list

for d in get_readings("https://www.aelf.org/"):
    print(d)