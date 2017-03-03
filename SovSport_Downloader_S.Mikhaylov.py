import requests
import cssselect
import lxml.html
import re
import urllib.request
import os
import json
from pymystem3 import Mystem

authors_ids, listids = [], []
def getting_authors_id():
    htmltext = requests.get('http://www.sovsport.ru/authors/')
    tree = lxml.html.fromstring(htmltext.text)
    text = tree.cssselect('script')
    with open('sketchy_authors.txt', 'w') as file_with_authors_and_rubbish:
        for txt in text:
            file_with_authors_and_rubbish.write(txt.text_content().strip())
    with open('sketchy_authors.txt') as file_with_id_and_rubbish:
        lines = file_with_id_and_rubbish.readlines()
        for i in range(1, 29):
            for line in lines:
                a = "var letter_" + str(i)
                if a in line:
                    ids = re.split("],", re.split(a, line)[1])
                    for item in ids:
                        listids.append(re.split(",", item)[0])
    for elem in listids:
        a = elem.replace('0 = [ [', '')
        b = a.replace('[', '')
        c = b.replace('=  ', '')
        d = c.replace('9 ', '')
        e = d.replace('8 ', '')
        f = e.replace('7 ', '')
        g = f.replace('6 ', '')
        h = g.replace('5 ', '')
        i = h.replace('4 ', '')
        j = i.replace('3 ', '')
        k = j.replace('2 ', '')
        l = k.replace('1 ', '')
        m = l.replace(' ', '')
        authors_ids.append(m)
    return(authors_ids)
def getting_article_refs():
    with open('ref_database.txt', 'w') as rf_database:
        for id in authors_ids:
            author_page = urllib.request.urlopen('http://www.sovsport.ru/author-item/' + str(id))
            author_refs = author_page.read().decode("utf-8")
            links = re.findall('<h3><a href="(.+?)">', author_refs)
            for ref in links:
                rf_database.write(str(ref) + '\n')
            author_page.close()
def folders_creator():
    path = 'C:\\'
    project_name = 'SovSport'
    folders = [['plaintext', [['2015', [['июль', []], ['август', []], ['сентябрь', []], ['октябрь', []], ['ноябрь', []], ['декабрь', []]]],
            ['2016', [['январь', []], ['февраль', []], ['март', []], ['апрель', []], ['май', []], ['июнь', []], ['июль', []], ['август', []], ['сентябрь', []], ['октябрь', []], ['ноябрь', []], ['декабрь', []]]]]], ['My_stem', [['2015', [['июль', []], ['август', []], ['сентябрь', []], ['октябрь', []], ['ноябрь', []], ['декабрь', []]]],
            ['2016', [['январь', []], ['февраль', []], ['март', []], ['апрель', []], ['май', []], ['июнь', []], ['июль', []], ['август', []], ['сентябрь', []], ['октябрь', []], ['ноябрь', []], ['декабрь', []]]]]]]

    def create_folder(path):
        if not os.path.exists(path):
            os.mkdir(path)

    def build(root, data):
        if data:
            for d in data:
                name = d[0]
                path = os.path.join(str(root), str(name))
                create_folder(path)
                build(path, d[1])

    full_path = os.path.join(str(path), str(project_name))
    create_folder(full_path)
    build(full_path, folders)
def create_new_plain_and_my_stem_text(month, year):
    title = tree.xpath('.//title/text()')[0][:21]
    work_title = str(title).replace('*', '').replace('|', '').replace(':', '').replace('"', '').replace('<', '').replace('>', '').replace('?', '').replace(' ', '')
    try:
        author = tree.xpath('.//a[@class="article_header_author_name"]/text()')[0]
    except:
        author = '-----'
    file_path = 'C:/SovSport/plaintext/' + year + '/' + month + '/' + work_title + '.txt'
    with open('C:/SovSport/plaintext/' + year + '/' + month + '/' + work_title + '.txt', 'w', encoding='utf-8') as text_file:
        file_content = tree.cssselect('p')
        for txt in file_content:
            text_file.write(txt.text_content().strip() + '\n')
    with open('C:/SovSport/plaintext/' + year + '/' + month + '/' + work_title + '.txt', encoding='utf-8') as file:
        wordcount = 0
        for word in file.read().split():
            wordcount += 1
    metatable.write(str(file_path) + '|' + str(author) + '|' + str(date) + '|' + 'Советский спорт' + '|' + work_title + '...' + '|' + 'http://www.sovsport.ru' + str(line).replace('\n', '') + '| Число слов: ' + str(wordcount) + '\n')
    m = Mystem()
    with open(file_path, encoding='utf-8') as txt:
        text = txt.read()
        lemmas = m.lemmatize(text)
        with open('C:/SovSport/My_stem/' + year + '/' + month + '/' + work_title + '.txt', 'a', encoding='utf-8') as myst_txt:
            myst_txt.write('lemmas:' + '\n' + ''.join(lemmas) + '\r\n' + 'full info:' + '\n' + json.dumps(m.analyze(text), ensure_ascii=False))
    # print('file processed')

folders_creator()
getting_authors_id()
getting_article_refs()

with open('ref_database.txt', encoding='utf-8') as refs:
    lines = refs.readlines()
    with open('C:/SovSport/meta_table.txt', 'w', encoding='utf-8') as metatable:
        for line in lines:
            html = requests.get('http://www.sovsport.ru' + str(line))
            tree = lxml.html.fromstring(html.text)
            try:
                date = tree.xpath('.//time[@class="article_header_info_time"]/text()')[0]
            except:
                # print('reference omitted')
                continue
            regexp1 = '(([0-9]+)\s(июля|августа|сентября|октября|ноября|декабря)\s2015)'
            regexp2 = '(([0-9]+)\s(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s2016)'
            if re.search(regexp1, str(date)[:-7]):
                if str(date)[2:-12] == 'июля' or str(date)[2:-12] == ' июля':
                    create_new_plain_and_my_stem_text('июль', '2015')
                elif str(date)[2:-12] == 'августа' or str(date)[2:-12] == ' августа':
                    create_new_plain_and_my_stem_text('август', '2015')
                elif str(date)[2:-12] == 'сентября' or str(date)[2:-12] == ' сентября':
                    create_new_plain_and_my_stem_text('сентябрь', '2015')
                elif str(date)[2:-12] == 'октября' or str(date)[2:-12] == ' октября':
                    create_new_plain_and_my_stem_text('октябрь', '2015')
                elif str(date)[2:-12] == 'ноября' or str(date)[2:-12] == ' ноября':
                    create_new_plain_and_my_stem_text('ноябрь', '2015')
                elif str(date)[2:-12] == 'декабря' or str(date)[2:-12] == ' декабря':
                    create_new_plain_and_my_stem_text('декабрь', '2015')
            elif re.search(regexp2, str(date)[:-7]):
                if str(date)[2:-12] == 'января' or str(date)[2:-12] == ' января':
                    create_new_plain_and_my_stem_text('январь', '2016')
                elif str(date)[2:-12] == 'февраля' or str(date)[2:-12] == ' февраля':
                    create_new_plain_and_my_stem_text('февраль', '2016')
                elif str(date)[2:-12] == 'марта' or str(date)[2:-12] == ' марта':
                    create_new_plain_and_my_stem_text('март', '2016')
                elif str(date)[2:-12] == 'апреля' or str(date)[2:-12] == ' апреля':
                    create_new_plain_and_my_stem_text('апрель', '2016')
                elif str(date)[2:-12] == 'мая' or str(date)[2:-12] == ' мая':
                    create_new_plain_and_my_stem_text('май', '2016')
                elif str(date)[2:-12] == 'июня' or str(date)[2:-12] == ' июня':
                    create_new_plain_and_my_stem_text('июнь', '2016')
                elif str(date)[2:-12] == 'июля' or str(date)[2:-12] == ' июля':
                    create_new_plain_and_my_stem_text('июль', '2016')
                elif str(date)[2:-12] == 'августа' or str(date)[2:-12] == ' августа':
                    create_new_plain_and_my_stem_text('август', '2016')
                elif str(date)[2:-12] == 'сентября' or str(date)[2:-12] == ' сентября':
                    create_new_plain_and_my_stem_text('сентябрь', '2016')
                elif str(date)[2:-12] == 'октября' or str(date)[2:-12] == ' октября':
                    create_new_plain_and_my_stem_text('октябрь', '2016')
                elif str(date)[2:-12] == 'ноября' or str(date)[2:-12] == ' ноября':
                    create_new_plain_and_my_stem_text('ноябрь', '2016')
                elif str(date)[2:-12] == 'декабря' or str(date)[2:-12] == ' декабря':
                    create_new_plain_and_my_stem_text('декабрь', '2016')
            else:
                continue
