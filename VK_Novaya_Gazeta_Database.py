import urllib.request, json, sqlite3, time, requests

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



for i in [0, 100, 200, 300, 400]:
    url = u'https://api.vk.com/method/wall.get?owner_id=-6726778&offset=' + str(i) + '&count=100'
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    with open('novgaz_wall.txt', 'a', encoding='utf-8') as txtfile:
        recursive(data, txtfile)

post_id = []

with open('novgaz_wall.txt', encoding='utf-8') as ng_w:
    lines = ng_w.readlines()
    for i in range(len(lines)):
        newline = lines[i].strip()
        if str(newline) == 'id':
            post_id.append(lines[i+1].strip())

con = sqlite3.connect('comments_database.db')
cur = con.cursor()
cur.execute('create table comments_database(id integer primary key, public_id integer, comm_id integer, to_post_id integer, user_id integer, reply_to_id integer, comm_date varchar(100), birthdate varchar(100), city integer, comm_txt varchar(500))')
con.commit()


number = 1
for k in post_id:
    indx = int(k)
    url = u'https://api.vk.com/method/wall.getComments?owner_id=-6726778&post_id=' + str(indx) + '&need_likes=0&count=100' \
            u'&sort=asc&preview_length=0'
    response = requests.get(url)
    for i in range(1, len(response.json()['response'])):
        comid = int(response.json()['response'][i]['cid'])
        commdate = time.ctime(int(response.json()['response'][i]['date']))
        text = response.json()['response'][i]['text']
        userid = int(response.json()['response'][i]['uid'])
        try:
            repl_to = int(response.json()['response'][i]['reply_to_cid'])
        except:
            repl_to = 0
        url2 = u'https://api.vk.com/method/users.get?user_ids=' + str(userid) + '&fields=bdate,city'
        response2 = requests.get(url2)
        try:
            gorod = int(response2.json()['response'][0]['city'])
        except:
            gorod = 0
        try:
            datarozh = response2.json()['response'][0]['bdate']
        except:
            datarozh = 'Not specified'
        cur.execute('insert into comments_database values (?,?,?,?,?,?,?,?,?,?)', (number, 6726778, comid, indx, userid, repl_to, commdate, datarozh, gorod, text))
        con.commit()
        number += 1