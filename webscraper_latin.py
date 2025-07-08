import requests
import re
from os.path import isfile

patterns = [r' <P><a name="...">..<\/A>&nbsp;', r' <P><a name="...">.<\/A>&nbsp;', r'<BR></P>', r'</P>']

def get_list(url):
    r = requests.get(url)
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

def write_to_file(filename, my_list, chapter):
    if isfile(filename):
        with open(filename, 'r', encoding = 'utf-8') as f:
            my_lines = f.readlines()
    else:
        my_lines = []
        
    my_lines += [f'{chapter},{my_list.index(line) + 1},{line}\n' for line in my_list]
    
    with open(filename, 'w', encoding = 'utf-8') as f:
        f.writelines(my_lines)
    
    
urls = {"lucas" : 'https://sacred-texts.com/bib/vul/luk0',
       "matthaeus" : 'https://sacred-texts.com/bib/vul/mat0',
       "marcus" : 'https://sacred-texts.com/bib/vul/mar0',
       "ioannes" : 'https://sacred-texts.com/bib/vul/joh0'}

for evangelist in urls.keys():
    filename = f'txt\\{evangelist[0:3]}_lat.txt'
    i = 1
    if i < 10:
        i_str = f'0{str(i)}'
    else:
        i_str = str(i)
        
    while get_list(urls[evangelist] + f'{i_str}.htm') != []:
        my_lines = get_list(urls[evangelist] + f'{i_str}.htm')
        write_to_file(filename, my_lines, i)
        
        i += 1
        if i < 10:
            i_str = f'0{str(i)}'
        else:
            i_str = str(i)
    
    print(f'{filename} created.')