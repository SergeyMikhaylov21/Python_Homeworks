import re
capital_lett = '[A-ZÚÉŠ]'
addit_signs = '[\[\]\(\)\d\'˹˺]'

filename = 'syllab.html'

with open(filename, encoding='utf-8') as file:
    k = file.read()
    f = list(k)
    for i in range(len(f)):
        if f[i] == '-':
            if re.search(capital_lett, f[i-1]) or re.search(capital_lett, f[i+1]) or f[i-1] == '>' and f[i+1] == '<':
                continue
            else:
                f[i] = f[i].replace('-', '')
    for i in range(len(f)):
        if f[i] == 'a' and f[i+2] == 'a' and f[i+4] == 'a':
            f[i+2] = f[i+2].replace('a', '')
            f[i+4] = f[i+4].replace('a', '')
            f[i] = f[i].replace('a', 'ā')
        elif f[i] == 'e' and f[i+2] == 'e' and f[i+4] == 'e':
            f[i+2] = f[i+2].replace('e', '')
            f[i+4] = f[i+4].replace('e', '')
            f[i] = f[i].replace('e', 'ē')
        elif f[i] == 'i' and f[i+2] == 'i' and f[i+4] == 'i':
            f[i+2] = f[i+2].replace('i', '')
            f[i+4] = f[i+4].replace('i', '')
            f[i] = f[i].replace('i', 'í')
        elif f[i] == 'u' and f[i+2] == 'u' and f[i+4] == 'u':
            f[i+2] = f[i+2].replace('u', '')
            f[i+4] = f[i+4].replace('u', '')
            f[i] = f[i].replace('u', 'ū')
        elif f[i] == 'a' and f[i+2] == 'a' and f[i+3] == '' or f[i] == 'a' and f[i+2] == 'a' and f[i-1] == '':
            f[i+2] = f[i+2].replace('a', '')
            f[i] = f[i].replace('a', 'ā')
        elif f[i] == 'e' and f[i+2] == 'e' and f[i+3] == '' or f[i] == 'e' and f[i+2] == 'e' and f[i-1] == '':
            f[i+2] = f[i+2].replace('e', '')
            f[i] = f[i].replace('e', 'ē')
        elif f[i] == 'i' and f[i+2] == 'i' and f[i+3] == '' or f[i] == 'i' and f[i+2] == 'i' and f[i-1] == '':
            f[i+2] = f[i+2].replace('i', '')
            f[i] = f[i].replace('i', 'í')
        elif f[i] == 'u' and f[i+2] == 'u' and f[i+3] == '' or f[i] == 'u' and f[i+2] == 'u' and f[i-1] == '':
            f[i+2] = f[i+2].replace('u', '')
            f[i] = f[i].replace('u', 'ū')
        elif f[i] == 'a' and f[i-2] == 'a' and f[i+1] == '':
            f[i] = f[i].replace('a', 'ā')
            f[i-2] = f[i-2].replace('a', '')
        elif f[i] == 'e' and f[i-2] == 'e' and f[i+1] == '':
            f[i] = f[i].replace('e', 'ē')
            f[i-2] = f[i-2].replace('e', '')
        elif f[i] == 'i' and f[i-2] == 'i' and f[i+1] == '':
            f[i] = f[i].replace('i', 'í')
            f[i-2] = f[i-2].replace('i', '')
        elif f[i] == 'u' and f[i-2] == 'u' and f[i+1] == '':
            f[i] = f[i].replace('u', 'ū')
            f[i-2] = f[i-2].replace('u', '')
        elif f[i] == 'a' or f[i] == 'u' or f[i] == 'e' and f[i-2] == 'i' or f[i-1] == 'i' and f[i-4] == 'i' or f[i-4] == 'a' or f[i-4] == 'u' or f[-4] == 'e':
            f[i-2] = f[i-2].replace('i', 'y')
        elif f[i] == 'a' and f[i+2] == 'a':
            f[i+2] = f[i+2].replace('a', '')
        elif f[i] == 'e' and f[i+2] == 'e':
            f[i+2] = f[i+2].replace('e', '')
        elif f[i] == 'u' and f[i+2] == 'u':
            f[i+2] = f[i+2].replace('u', '')
        elif f[i] == '!' or f[i] == '?':
            f[i] = f[i].replace('!', '')
            f[i] = f[i].replace('?', '')
        elif f[i] == 't' and f[i-1] == 'l' or f[i-1] == 'g' and f[i-2] == '&' and f[i+1] == ';':
            f[i] = f[i].replace('t', '')
            f[i-1] = f[i-1].replace('l', '').replace('g', '')
            f[i-2] = f[i-2].replace('&', '')
            f[i+1] = f[i+1].replace(';', '')
    for i in range(len(f)):
        if f[i] == 'y' and f[i-1] == '<' and f[i+1] == '>':
            f[i] = f[i].replace('y', 'i')
    for i in range(len(f)):
        if f[i] == '<' and f[i+3] == '>' and f[i+1] != '/':
            f[i] = f[i].replace('<', '')
            f[i+3] = f[i+3].replace('>', '')
    for i in range(len(f)):
        if re.search(addit_signs, f[i]):
            f[i] = ''
    for i in range(len(f)):
        if f[i] == '-' and f[i-1] == '>' and f[i+1] == '<':
            f[i] = f[i].replace('-', '')
    with open(filename[:-5] + '_changed.html', 'w', encoding='utf-8') as final:
        for i in f:
            final.write(i)