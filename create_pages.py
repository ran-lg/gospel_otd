from generate_gospel_calendar import get_gospel_alpha, get_gospel_delta
from sys import argv
from pathlib import Path
import re

lang_list = ['lat', 'gr', 'pl']

def extract_lines(lang, eva, chapter, verses):
    source_filename = Path('txt') / f'{eva}_{lang}.txt'

    with open(source_filename, 'r', encoding = 'utf-8') as f:
        return [line.replace(f'{str(chapter)}|{str(verse)}|', '')
                    .replace('\n', '')
                     for line in f.readlines()
                     for verse in verses
                     if line.startswith(f'{str(chapter)}|{str(verse)}|')]

def create_html(day):
    target_filename = Path('html') / f'{day['date'].strftime('%Y%m%d')}_gospel.html'

    # parse expression = 'Lc 4, 31-73'
    #                  = 'Lc 4, 14.31-73'

    expression = day['gospel_otd']
    
    match expression[:expression.find(' ')]:
        case 'Lc':
            eva = 'luc'
        case 'Mc':
            eva = 'mar' 
        case 'Mt':
            eva = 'mat'
        case 'Jn':
            eva = 'ioa'
    
    regex_chapter = '[MLJ][tcn] ([1-9][0-9]?),'
    chapter = re.search(regex_chapter, expression).group(1)

    regex_verses = ', (.*)$'
    pre_verses = re.search(regex_verses, expression).group(1).replace(' ', '')
    verses = []
    for pre_verse in pre_verses.split('.'):
        pre_verse = pre_verse.replace(',', '').replace(' ', '')
        if not '-' in pre_verse:
            verses.append(int(pre_verse))
        else:
            pos_score = pre_verse.find('-')
            verses += list(range(int(pre_verse[:pos_score]), int(pre_verse[pos_score + 1:]) + 1))
    
    multilingual_verses = {}
    for lang in lang_list:
        multilingual_verses[lang] = extract_lines(lang, eva, chapter, verses)

    html = f'''<html>
<body>
    <h1>{day['date'].strftime('%d/%m/%Y')}</h1>'''
    for i in range(len(verses) - 1):
        html += f'''
    <p>
        <table>'''
        for lang in multilingual_verses.keys():
            html += f'''
                <tr>
                    <td>{multilingual_verses[lang][i]}</td>
                </tr>'''
        html += f'''
        </table>
    </p>'''
    html += '''
</body>
'''
    with open(target_filename, 'w') as f:
        f.write(html)
        print(f'{target_filename} created')

if __name__ == '__main__':
    try:
        mode = argv[1]
    except:
        mode = '-d'

    try:
        nb = int(argv[2])
    except:
        nb = 5

    if mode == '-d':
        days = get_gospel_delta(nb)
        for day in days:
            create_html(day)
    elif mode == '-a':
        days = get_gospel_alpha(nb)
        for day in days:
            create_html(day)
    else:
        print('Choose a mode: -d (delta) or -a (alpha).')
