from pkuseg import pkuseg
from flask import Flask, render_template, request
from flask import jsonify
import sys
sys.path.append('/home/ai/PycharmProjects/an_qu/an_qu/config')
from config import config
sys.path.append('/home/ai/PycharmProjects/an_qu/an_qu/tool')
from tools import *

app = Flask(__name__)

stop_path = config.stop_path
ans_path = config.ans_path
que_path = config.que_path
mydict = read_mydict()
# print(mydict)
seg = pkuseg(user_dict=mydict)
dictionary, texts = get_dictionary()
que_txt = [seg for seg in open(que_path, 'r', encoding='utf8').readlines()]
ans_txt = [seg for seg in open(ans_path, 'r', encoding='utf8').readlines()]


@app.route('/')
def hello_world():
    return '你好，欢迎访问自动问答系统。'


@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        question = request.form['question']
    else:
        question = request.args['question']
    answer = search(que_txt, ans_txt, dictionary, texts, question)
    return render_template("an_qu.html", question=question, answer=answer)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050,debug=False)
    print("链接已完成！恭喜")
