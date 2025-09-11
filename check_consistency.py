from tabulate import tabulate
from pathlib import Path
from os import listdir

# 'mar_gr.txt' => 'gr'

def extract_lang(filename):
    return filename.replace('.txt', '')[filename.find('_') + 1:]

# 'mar_gr.txt' => 'mar'

def extract_eva(filename):
    return filename[:filename.find('_')]

def get_nb_lines(filename):
    with open(Path('txt') / filename, 'r', encoding = 'utf-8') as f:
        return len(f.readlines())

def get_nb_chapters(filename):
    with open(Path('txt') / filename, 'r', encoding = 'utf-8') as f:
        last_line = f.readlines()[-1]
        return last_line[:last_line.find('|')]


if __name__ == '__main__':
    files = [file for file in listdir('txt') if file.endswith('.txt')]
    
    evas = set([extract_eva(file) for file in files])
    langs = set([extract_lang(file) for file in files])
    
    # display the number of chapters per language, per evangelist

    my_tab = []
    for lang in langs:
        chapter_stats = [lang]
        for eva in evas:
            chapter_stats.append(get_nb_chapters(f'{eva}_{lang}.txt'))
        my_tab.append(chapter_stats)
    
    print(tabulate(my_tab, headers = evas) + '\n')

    # display the number of lines per language, per evangelist

    my_tab = []
    for lang in langs:
        line_stats = [lang]
        for eva in evas:
            line_stats.append(get_nb_lines(f'{eva}_{lang}.txt'))
        my_tab.append(line_stats)
    
    print(tabulate(my_tab, headers = evas))
