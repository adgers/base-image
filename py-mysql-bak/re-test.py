import re

str = '/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;'

sql = '/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;'




CHARACTER = re.findall('/\*(.*?)\*/',str)
print(CHARACTER)
with open('accounting.sql','r',encoding='utf-8') as acc:
    str1 = re.findall('/\*(.*?)\*/', acc.read())
    print(str1)

for i in range(0,len(str1)):
    print(str1[i])

file_date = ""
with open('accounting.sql', 'r', encoding='utf-8')as a, open('accounting-bak.sql', 'w', encoding='utf-8') as f:
    for line in a.readlines():
        for i in range(0,len(str1)):
            if str1[i] == line:
                # line = line.replace(str1[i],"")
                print("line 的")
            # print(line)
    #     file_date += line
    # f.write(file_date)






