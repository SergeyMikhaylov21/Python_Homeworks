import re
regularrussian = '[a-яёА-ЯЁ]'
regularlatin = '[a-zA-Z]'
regulartags = '[><]'
regularonlyrussian = '[йцгшщзъфыплджэячьбюёЙЦГШЩЗЪФЫПЛДЖЭЯЧЬБЮЁ]'
regularonlylatin = '[qwertisdfghjlzvQWRTISDFGHJLZV]'
f = open('#filename', 'r', encoding="utf-8")
lines = f.readlines()
Cntlines = 1
d = {'e':'е', 'y':'у', 'u':'и', 'o':'о', 'p':'р', 'a':'а', 'k':'к', 'x':'х', 'c':'с', 'b':'ь', 'E':'Е',
     'Y':'У', 'U':'И', 'O':'О', 'P':'Р', 'A':'А', 'K':'К', 'X':'Х', 'C':'С', 'M':'М', 'm':'м', 'n':'п'}
d1 = {'е':'e', 'у':'y', 'и':'u', 'о':'o', 'р':'p', 'а':'a', 'к':'k', 'х':'x', 'с':'c', 'ь':'b', 'Е':'E',
      'У':'Y', 'И':'U', 'О':'O', 'Р':'P', 'А':'A', 'К':'K', 'Х':'X', 'С':'C', 'М':'M', 'м':'m', 'п':'n'}
logfile = open("OpenedTom-log.txt", 'w', encoding = 'utf-8')
correctedfile = open("OpenedTom-corr.txt", 'w', encoding = 'utf-8')
for line in lines:
    words = line.split(' ')
    Cntwords = 1
    for word in words:
        russian = False
        latin = False
        onlyrussian = False
        onlylatin = False
        tags = False
        if(re.search(regularrussian, word)):
            russian = True
            if(re.search(regularonlyrussian, word)):
                onlyrussian = True
        if (re.search(regularlatin, word)):
            latin = True
        if (re.search(regularlatin, word)):
            latin = True
            if re.search(regularonlylatin, word):
                onlylatin = True
        if(re.search(regulartags, word)):
            tags = True
        if (onlyrussian and latin) or (onlylatin and russian):
            wt = []
            IsTagElement = False
            cnttagopen = 0
            cnttagclose = 0
            firstclosetagind = 0
            firstopentagind = 0
            for i in range(len(word)):
                if(word[i] == '>'):
                    firstclosetagind = i
                    break
            for i in range(len(word)):
                if(word[i] == '<'):
                    firstopentagind = i
                    break
            for i in range(len(word)):
                if(word[i] == '<'):
                    IsTagElement = True
                    cnttagopen += 1
                if(word[i] == '>'):
                    IsTagElement = False
                    cnttagclose += 1
                if (IsTagElement):
                    wt.append(1)
                else:
                    wt.append(0)
            if((firstclosetagind < firstopentagind) or ((cnttagclose > cnttagopen)and cnttagopen == 0)):
                for j in range(0, firstclosetagind):
                    wt[j] = 1
            if onlyrussian:
                dict = d
            else:
                dict = d1
            for i in range(len(word)):
                if((word[i] in dict.keys() and wt[i] == 0)):
                    list1 = list(word)
                    list1[i] = dict[word[i]]
                    word = ''.join(list1)
                    print ("В слове " + word + " на строке " + str(Cntlines) + " заменили букву " + word[i])
                    logfile.write("В слове " + word + " на строке " + str(Cntlines) + " заменили букву " + word[i] +"\n")
        Cntwords += 1
    linecorrected = " ".join(words)
    correctedfile.write(linecorrected + '\n')
    Cntlines += 1
f.close()
logfile.close()
correctedfile.close()