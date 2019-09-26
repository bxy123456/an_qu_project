import json
from an_qu.config.config import config
json_path=config.json_save_path
que_path=config.que_path
ans_path=config.ans_path
json_data=open(json_path,"r",encoding="utf8").read().split("\n")
data=list(filter(None,json_data))
que=open(que_path,"w",encoding="utf8")
ans=open(ans_path,"w",encoding="utf8")
#将json文件分别存放到两个txt文件下
for line in data:
    line=json.loads(line)
    ans_line=line["答案"]
    ans.write(ans_line)
    ans.write("\n")
    que_line=line["问题"]
    que.write(que_line)
    que.write("\n")
