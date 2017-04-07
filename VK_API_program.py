import urllib.request, json, re

def recursive(obj, file):
    if isinstance(obj, dict):
        for key, value in obj.items():
            file.write(str(key) + '\n')
            recursive(value, file)
    elif isinstance(obj, list):
        for item in obj:
            recursive(item, file)
    else:
        file.write(str(obj) + '\n')


def extract_info(wrt_file, rd_file, box, val1, val2):
    lines = rd_file.readlines()
    for i in range(len(lines)):
        newline = lines[i].strip()
        if str(newline) == str(val1):
            box.append(lines[i+1].strip())
        elif str(newline) == str(val2) and len(lines[i+1].strip()) > 3:
            wrt_file.write(lines[i+1].strip() + '\n')

def count_data(wrt_file, rd_file):
    lines = rd_file.readlines()
    for i in range(len(lines)):
        line = str(lines[i]).replace('<br>', ' ')
        qline = line.split(' ')
        qword = len(qline)
        wrt_file.write(str(qword) + '\n')

post_id, user_id, user_comm, user_comm_wrd = [], [], {}, {}

for i in [2, 102, 202, 302]:
    url = u'https://api.vk.com/method/wall.get?owner_id=-53845179&offset=' + str(i) + '&count=100'
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    with open('che_wall.txt', 'a', encoding='utf-8') as txtfile:
        recursive(data, txtfile)

with open('che_texts.txt', 'w', encoding='utf-8') as ch_txts:
    with open('che_wall.txt', encoding='utf-8') as che_info:
        extract_info(ch_txts, che_info, post_id, 'id', 'text')


with open('che_comments.txt', 'w', encoding='utf-8') as ch_comm:
    for i in post_id:
        url = u'https://api.vk.com/method/wall.getComments?owner_id=-53845179&post_id=' + str(i) + '&need_likes=0&count=100' \
            u'&sort=asc&preview_length=0'
        res = urllib.request.urlopen(url).read().decode('utf-8')
        data = json.loads(res)
        recursive(data, ch_comm)

with open('che_comm_texts.txt', 'w', encoding='utf-8') as ch_comm_txt:
    with open('che_comments.txt', encoding='utf-8') as ch_comm:
        extract_info(ch_comm_txt, ch_comm, user_id, 'uid', 'text')


with open('che_comments.txt', encoding='utf-8') as ch_comm:
    lines = ch_comm.readlines()
    for i in range(len(lines)):
        newline = lines[i].strip()
        if str(newline) == 'uid':
            usid = lines[i+1].strip()
            ustxt = str(lines[i+3]).strip()
            user_comm[usid] = ustxt

for key, values in user_comm.items():
    cmnt = str(values).replace('<br>', ' ')
    com_word = len(cmnt.split(' '))
    user_comm_wrd[key] = com_word
user_comm_wrd['1'] = ' '

with open('users_info.txt', 'w', encoding='utf-8') as us_info:
    for key in user_comm_wrd.keys():
        url = u'https://api.vk.com/method/users.get?user_ids=' + str(key) + '&fields=bdate,city'
        res = urllib.request.urlopen(url).read().decode('utf-8')
        data = json.loads(res)
        recursive(data, us_info)


with open('post_info.csv', 'w', encoding='utf-8') as che_post:
    with open('che_texts.txt', encoding='utf-8') as ch_txt:
        count_data(che_post, ch_txt)

with open('comm_info.csv', 'w', encoding='utf-8') as che_comm_data:
    with open('che_comm_texts.txt', encoding='utf-8') as ch_comm:
        count_data(che_comm_data, ch_comm)

with open('users_info.txt', encoding='utf-8') as us_info:
    with open('che_users_info.csv', 'w', encoding='utf-8') as che_us:
        lines = us_info.readlines()
        for i in range(len(lines)):
            newline = lines[i].strip()
            if str(newline) == 'response':
                city = str(lines[i+4]).strip()
                us_id = str(lines[i+6]).strip()
                bd_prev = str(lines[i+10]).strip()
                if re.search('[0-9]{4}', bd_prev[-4:]):
                    bd_date = bd_prev[-4:]
                    age = 2017 - int(bd_date)
                else:
                    bd_prev = str(lines[i+8]).strip()
                    if re.search('[0-9]{4}', bd_prev[-4:]):
                        bd_date = bd_prev[-4:]
                        age = 2017 - int(bd_date)
                    else:
                        age = ' '
                che_us.write(us_id + ',' + str(user_comm_wrd[us_id]) + ',' + str(age) + ',' + city + '\n')



with open('messages.txt', 'a', encoding='utf-8') as msgs:
    for i in [0, 201, 401, 601, 801, 1001, 1201, 1401, 1601]:
        url = u'https://api.vk.com/method/messages.getHistory?user_id=' + str('свой id') + '6&peer_id=' + str('беседа') + '&count=200' \
            u'&offset=' + str(i) + '&access_token=' + str('токен доступа') + '&v=5.38&rev=1'
        res = urllib.request.urlopen(url).read().decode('utf-8')
        data = json.loads(res)
        recursive(data, msgs)

with open('messages.txt', encoding='utf-8') as mess:
    with open('members_info.csv', 'w', encoding='utf-8') as members:
         lines = mess.readlines()
         for i in range(len(lines)):
             newline = lines[i].strip()
             if str(newline) == 'user_id' and str(lines[i+4]).strip() != 'emoji':
                 body = str(lines[i+9]).strip()
                 text = body.split(' ')
                 kolsl = len(text)
                 memb = str(lines[i+1]).strip()
                 members.write(memb + ',' + str(kolsl) + '\n')
             elif str(newline) == 'user_id' and str(lines[i+4]).strip() == 'emoji':
                 body = str(lines[i+11]).strip()
                 text = body.split(' ')
                 kolsl = len(text)
                 memb = str(lines[i+1]).strip()
                 members.write(memb + ',' + str(kolsl) + '\n')