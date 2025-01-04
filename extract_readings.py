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

# "xyz (Gn 2, 18-25)" => "Gn 2, 18-25"

def extract_substr_btw_end_brackets(my_str):
    pos = my_str.find("(")
    return my_str[pos+1:len(my_str)-1]

def delete_nbreaking_spaces(my_str):
    return my_str.replace(u"\xa0", u"")

# extracts the lower case letter of a substring
# e.g. "16a" => "a"
#      "161" => ""

def extract_lc_letter(my_str):
    for c in my_str:
        if ord(c) > 96 and ord(c) < 122:
            return c
    return ""

# deletes the lower case letter of a substring
# e.g. "16a" => "16"
#      "161" => "161"

def delete_lc_letter(my_str):
    for c in my_str:
        if ord(c) > 96 and ord(c) < 122:
            return my_str.replace(c,"")
    return my_str

# "22a-25b" => "22a"
# "22KJ" => "22KJ"

def extract_leftof_dash(my_str):
    if (my_str.find("-") == -1) and (my_str.find("–") == -1):
        return my_str
    else:
        if my_str.find("-") > -1:
            return my_str[:my_str.find("-")]
        else:
            return my_str[:my_str.find("–")]

# "22a-25b" => "25b"
# "22KJ" => "22KJ"

def extract_rightof_dash(my_str):
    if (my_str.find("-") == -1) and (my_str.find("–") == -1):
        return my_str
    else:
        if my_str.find("-") > -1:
            return my_str[my_str.find("-")+1:]
        else:
            return my_str[my_str.find("–")+1:]

# creates a dict related to the fragments read, e.g.
# "Jn 3, 7b- 15"
#
# {book: "Jn",                   
#                                / i
#  beginning1_chapter: "3",      - 1
#  beginning1_verse: "7",        - 2
#  beginning1_letter: "b",       - 3
#  end1_chapter: "3",            - 4
#  end1_verse: "15",             - 5
#  end1_letter: "",              - 6
#  beginning2_chapter: "",       - 7
#  beginning2_verse: "",         - 8
#  beginning2_letter: "",        - 9
#  end2_chapter: "",             - 10
#  end2_verse: "",               - 11
#  end2_letter: "",              - 12
#  beginning3_chapter: "",       - 13
#  beginning3_verse: "",         - 14
#  beginning3_letter: "",        - 15
#  end3_chapter: "",             - 16
#  end3_verse: "",               - 17
#  end3_letter: ""}              - 18

def gospel_dict (my_str):
    gospel = my_str[0:2]
    my_str = my_str[3:]
    
    my_dict = {}
    my_dict["book"] = gospel

    my_str.replace(";", ",")
    my_str.replace(" ", "")
    segments = my_str.split(",")

    i = 1
    while (len(segments) > 0) and (i <= 18):
        match i:
            case 1 | 7 | 13:
                match i:
                    case 1:
                        my_dict["beginning1_chapter"] = segments[0]
                    case 7:
                        my_dict["beginning2_chapter"] = segments[0]
                    case 13:
                        my_dict["beginning3_chapter"] = segments[0]
                i += 1
            case 2 | 8 | 14:
                if "." in segments[0]:
                    verses_segment = segments[0].split(".")
                    for verses in verses_segment:
                        match i:
                            case 2:
                                my_dict["beginning1_verse"] = delete_lc_letter(extract_leftof_dash(verses))
                                my_dict["beginning1_letter"] = extract_lc_letter(extract_leftof_dash(verses))

                                my_dict["end1_chapter"] = my_dict["beginning1_chapter"]
                                my_dict["end1_verse"] = delete_lc_letter(extract_rightof_dash(verses))
                                my_dict["end1_letter"] = extract_lc_letter(extract_rightof_dash(verses))
                                i = 7
                            case 8:
                                my_dict["beginning2_verse"] = delete_lc_letter(extract_leftof_dash(verses))
                                my_dict["beginning2_letter"] = extract_lc_letter(extract_leftof_dash(verses))
                                
                                my_dict["end2_chapter"] = my_dict["beginning2_chapter"]
                                my_dict["end2_verse"] = delete_lc_letter(extract_rightof_dash(verses))
                                my_dict["end2_letter"] = extract_lc_letter(extract_rightof_dash(verses))
                                i = 13
                            case 14:
                                my_dict["beginning3_verse"] = delete_lc_letter(extract_leftof_dash(verses))
                                my_dict["beginning3_letter"] = extract_lc_letter(extract_leftof_dash(verses))

                                my_dict["end3_chapter"] = my_dict["beginning3_chapter"]
                                my_dict["end3_verse"] = delete_lc_letter(extract_rightof_dash(verses))
                                my_dict["end3_letter"] = extract_lc_letter(extract_rightof_dash(verses))
                                i = 19
                else:
                    match i:
                        case 2:
                            my_dict["beginning1_verse"] = delete_lc_letter(extract_leftof_dash(segments[0]))
                            my_dict["beginning1_letter"] = extract_lc_letter(extract_leftof_dash(segments[0]))

                            my_dict["end1_chapter"] = my_dict["beginning1_chapter"]
                            my_dict["end1_verse"] = delete_lc_letter(extract_rightof_dash(segments[0]))
                            my_dict["end1_letter"] = extract_lc_letter(extract_rightof_dash(segments[0]))
                            i = 7
                        case 8:
                            my_dict["beginning2_verse"] = delete_lc_letter(extract_leftof_dash(segments[0]))
                            my_dict["beginning2_letter"] = extract_lc_letter(extract_leftof_dash(segments[0]))
                                
                            my_dict["end2_chapter"] = my_dict["beginning2_chapter"]
                            my_dict["end2_verse"] = delete_lc_letter(extract_rightof_dash(segments[0]))
                            my_dict["end2_letter"] = extract_lc_letter(extract_rightof_dash(segments[0]))
                            i = 13
                        case 14:
                            my_dict["beginning3_verse"] = delete_lc_letter(extract_leftof_dash(segments[0]))
                            my_dict["beginning3_letter"] = extract_lc_letter(extract_leftof_dash(segments[0]))

                            my_dict["end3_chapter"] = my_dict["beginning3_chapter"]
                            my_dict["end3_verse"] = delete_lc_letter(extract_rightof_dash(segments[0]))
                            my_dict["end3_letter"] = extract_lc_letter(extract_rightof_dash(segments[0]))
                            i = 19
        segments.pop(0)
    return my_dict

# extracts the readings of url
# KISS: for now, only the gospel is considered

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


