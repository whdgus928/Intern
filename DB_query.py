'''
csv파일에 수정해야하는 값을 불러와 DB 변경 쿼리문을 생성
ex) INSERT INTO column(col1,col2,col3,col4,col5) values(1,2,3,97,1);
'''

def read_file(file_path):
    i=0
    WFile = open("test.txt", "w")
    with open(f"{file_path}", "r",encoding='utf-8') as my_file:
        while True:
            line = my_file.readline().rstrip()
            if not line:
                break
            list_=line.split(',')
            list_[-4]="'"+df.loc[i,'영문스키마']+"'"
            list_[-3]="'"+df.loc[i,'한글스키마']+"'"
            i+=1
            text=','.join(list_)
            print(text, file=WFile)
    WFile.close()

import pandas as pd
df=pd.read_csv('C:\\Users\\user\\Downloads\\cs.csv',encoding='utf-8')
read_file('C:\\Users\\user\\Downloads\\aaaa.txt')
