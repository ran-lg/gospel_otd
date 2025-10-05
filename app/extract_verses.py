from sys import argv
from pathlib import Path
import re

lang_list = ['lat', 'pl', 'gr']

def extract_lines(lang, eva, chapter, verses):
    source_filename = Path('app/txt') / f'{eva}_{lang}.txt'

    with open(source_filename, 'r', encoding = 'utf-8') as f:
        return [line.replace(f'{str(chapter)}|{str(verse)}|', '')
                    .replace('\n', '')
                     for line in f.readlines()
                     for verse in verses
                     if line.startswith(f'{str(chapter)}|{str(verse)}|')]

def get_lines_gotd(fragment):
    # parse fragment = 'Lc 4, 31-73'
    #                = 'Lc 4, 14.31-73'
   
    match fragment[:fragment.find(' ')]:
        case 'Lc':
            eva = 'luk'
        case 'Mc':
            eva = 'mar' 
        case 'Mt':
            eva = 'mat'
        case 'Jn':
            eva = 'ioa'
    
    regex_chapter = '[MLJ][tcn] ([1-9][0-9]?),'
    chapter = re.search(regex_chapter, fragment).group(1)

    regex_verses = ', (.*)$'
    pre_verses = re.search(regex_verses, fragment).group(1).replace(' ', '')
    verses = []

    for pre_verse in pre_verses.split('.'):
        pre_verse = pre_verse.replace(',', '').replace(' ', '')
        if not '-' in pre_verse:
            verses.append(int(pre_verse))
        else:
            pos_score = pre_verse.find('-')
            verses += list(range(int(pre_verse[:pos_score]), int(pre_verse[pos_score + 1:]) + 1))
    
    # generate {'lat': [...], 'gr': [...], 'pl': [...]}
    
    multilingual_verses = {}
    for lang in lang_list:
        multilingual_verses[lang] = extract_lines(lang, eva, chapter, verses)
          
    # generate [{'lat': '...', 'gr': '...', 'pl': '...'},    
    #           {'lat': '...', 'gr': '...', 'pl': '...'},
    #           {'lat': '...', 'gr': '...', 'pl': '...'}]
    
    nb_verses = len(multilingual_verses[lang_list[0]])
    reformatted_multilingual_verses = []
    for i in range(nb_verses):
        temp = {}
        for lang in multilingual_verses:
            temp[lang] = multilingual_verses[lang][i]
        reformatted_multilingual_verses.append(temp)
    
    return reformatted_multilingual_verses
        
if __name__ == '__main__':
    print(f"""Lc 17, 5-10

{get_lines_gotd("Lc 17, 5-10")}""")