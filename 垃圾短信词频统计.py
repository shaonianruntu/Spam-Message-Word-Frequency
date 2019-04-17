# encoding=utf-8
import jieba
import re
from collections import Counter
import json


#输入输出文件信息
origanword_file = "spam.txt"
stopword_file = "stopwords.dat" 
outputword_file = "sorted_words.json"

#按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


#将content内容保存在对应的file_name文件
def save_file(file_name, content):
    fp = open(file_name, "w", encoding="utf-8")
    fp.write(content)
    fp.close()


#对短信中的用户名前缀和内部的url链接进行过滤删除
def regex_change(line):
    #前缀的正则
    username_regex = re.compile(r"^\d+::")
    #URL，为了防止对中文的过滤，所以使用[a-zA-Z0-9]而不是\w
    url_regex = re.compile(r"""
        (https?://)?
        ([a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)*
        (/[a-zA-Z0-9]+)*
    """, re.VERBOSE|re.IGNORECASE)
    #剔除日期
    data_regex = re.compile(u"""
        年 |
        月 |
        日 |
        (周一) |
        (周二) | 
        (周三) | 
        (周四) | 
        (周五) | 
        (周六)
    """, re.VERBOSE)
    #剔除所有数字
    decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    #剔除空格
    space_regex = re.compile(r"\s+")

    line = username_regex.sub(r"", line)
    line = url_regex.sub(r"", line)
    line = data_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)

    return line


#剔除停用词
def delete_stopwords(lines):
    stopwords = read_file(stopword_file)
    all_words = []

    for line in lines:
        all_words += [word for word in jieba.cut(line) if word not in stopwords]

    dict_words = dict(Counter(all_words))

    return dict_words


#主函数
if __name__ == "__main__":
    lines = read_file(origanword_file)
    
    for i in range(len(lines)):
        lines[i] = regex_change(lines[i])
    
    bow_words = delete_stopwords(lines)

    sorted_bow = sorted(bow_words.items(), key=lambda d:d[1], reverse=True)

    with open(outputword_file, "w") as output_file:
        json.dump(sorted_bow, output_file, ensure_ascii=False)
        print("加载数据完成...")

    for words in sorted_bow[:100]:
        print(words)

    
    

    



