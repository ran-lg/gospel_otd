import requests
import re
from os.path import isfile
from os import listdir, mkdir
from time import sleep
from random import randint

patterns = [r' <P><a name="...">..<\/A>&nbsp;', r' <P><a name="...">.<\/A>&nbsp;', r'<BR></P>', r'</P>']


# get all text lines in a given page, e.g. 'https://sacred-texts.com/bib/vul/luk001.htm'

def get_lines(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    if r.status_code == '404':
        return []
    else:
        lines = r.text.replace('</H3>', '</H3>\n ').replace('\n </P>\n', '</P>\n').replace('[', '').replace(']', '').split('\n')
        lines = [line for line in lines if line.startswith(' <P><a name=')]

        new_lines = []
        for line in lines:
            for pattern in patterns:
                for occurrence in re.findall(pattern, line):
                    if occurrence != '<BR>':
                        line = line.replace(occurrence, "")
                    else:
                        line = line[::-1].replace('>RB<', '', 1)[::-1]
            new_lines.append(line)
        return new_lines

# add the new_lines related to chapter to the file, whether it already exists or not

def write_to_file(filename, new_lines, chapter):
    if isfile(filename):
        with open(filename, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    else:
        lines = []

    lines += [f'{chapter}|{new_lines.index(line) + 1}|{line}\n' for line in new_lines]

    with open(filename, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    urls = {"mar" : 'https://sacred-texts.com/bib/vul/mar0',
            "ioa" : 'https://sacred-texts.com/bib/vul/joh0',
			"mat" : 'https://sacred-texts.com/bib/vul/mat0',
			"luc" : 'https://sacred-texts.com/bib/vul/luk0'}

    if not 'txt' in listdir():
        mkdir('txt')

    for evangelist in urls.keys():
        filename = f'txt/{evangelist}_lat.txt'
        i = 1
        if i < 10:
            i_str = f'0{str(i)}'
        else:
            i_str = str(i)

        file_created = False
        while get_lines(urls[evangelist] + f'{i_str}.htm') != []:
            url = urls[evangelist] + f'{i_str}.htm'
            print(url)
            lines = get_lines(url)
            sleep(randint(2, 10))
            write_to_file(filename, lines, i)
            i += 1
            if i < 10:
                i_str = f'0{str(i)}'
            else:
                i_str = str(i)

            if not file_created:
                print(f'{filename} created.')
                file_created = True

        if file_created == False:
            print(f'{filename} not created.')
