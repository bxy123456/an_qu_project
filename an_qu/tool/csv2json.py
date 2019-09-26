import csv
import  os
import json
from 做测试.an_qu.config.config import config
csv_path=config.csv_path
json_path=config.json_save_path
files=os.listdir(csv_path)
s = []  # 创建一个空列表
# 读取文件夹下的每一个文件
for file_ in files:  # 循环读取每个文件名
    file=csv_path+"/"+file_
    s.append(file)  # 把当前文件名返加到列表里
# 将每一个文件中的csv通过字典转换为json
for i in s:
    with open(i,"r",encoding="utf8") as f:
        text=csv.reader(f)
        for line in text:
            list = []
            dict2={}
            for j in line:
                list.append(j)
            dict2["问题"]=list[1]
            dict2["答案"] = list[2]
            json_dic=json.dumps(dict2,ensure_ascii=False)
            with open(json_path, "a", encoding='utf-8') as f1:
                f1.write(json_dic+"\n")