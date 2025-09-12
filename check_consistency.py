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

def get_nb_verses_per_chapter(filename, chapter):
    nb_verses = 0
    with open(Path('txt') / filename, 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            if line[:line.find('|')] == str(chapter):
                nb_verses += 1
    return nb_verses
                

if __name__ == '__main__':
    files = [file for file in listdir('txt') if file.endswith('.txt')]
    
    evas = set([extract_eva(file) for file in files])
    langs = set([extract_lang(file) for file in files])
    
    print('\nNumber of chapters per language, per evangelist\n')

    my_tab = []
    nb_chapter_max = 0
    for lang in langs:
        chapter_stats = [lang]
        for eva in evas:
            nb_chapters = get_nb_chapters(f'{eva}_{lang}.txt')
            chapter_stats.append(nb_chapters)
            
            if int(nb_chapters) > nb_chapter_max:
                nb_chapter_max = int(nb_chapters)
        my_tab.append(chapter_stats)
    
    print(tabulate(my_tab, headers = evas) + '\n')

    print('\nNumber of lines per language, per evangelist\n')

    my_tab = []
    for lang in langs:
        line_stats = [lang]
        for eva in evas:
            line_stats.append(get_nb_lines(f'{eva}_{lang}.txt'))
        my_tab.append(line_stats)
    
    print(tabulate(my_tab, headers = evas))

    print('\nNumber of lines per language/chapter, per evangelist\n')

    my_tab = []
    for chapter in range(1, nb_chapter_max + 1):
        for lang in langs:
            line_stats = [f'{lang}_{chapter}']
            for eva in evas:
                    line_stats.append(get_nb_verses_per_chapter(f'{eva}_{lang}.txt', chapter))
            my_tab.append(line_stats)
        my_tab.append(['-'] * 5)
    
    print(tabulate(my_tab, headers = evas))
