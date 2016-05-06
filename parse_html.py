#coding=utf-8
'''
#提取html中与关键人名有关的语料，存在Corpus_Base目录下
#@author:cer
'''
import os
import re
import bs4
from bs4 import BeautifulSoup

def parse_html_and_save(final_path,key_name,rank):
    print final_path,key_name,rank
    assert re.match('.+\.html', final_path)
    if os.path.exists(final_path):
        h_file = open(final_path)
        # h_file = io.open(plus_name,encoding='utf-8')
        h_string = h_file.read()
        soup = BeautifulSoup(h_string,'lxml')
        #补全html代码
        h_fixed =  soup.prettify()
        keys = key_name.split()
        # print u"html文件中是否包含目标人名？"
        # print key_name in h_fixed
        if key_name in h_fixed:
            res_set = set()
            for key in keys:
                res_set |= set(soup.find_all(name=True,text=re.compile(key)))
                # print type( soup.find_all(name=True, text=re.compile(key))[0] )
            res_list = list(res_set)
            text = ""
            p_tag_set = set()
            for tag in res_list:
                #标签节点类型属于h1~h6，只选取该标签的文本
                if re.match('h\d+',tag.name):
                    # print u"这是一个h标签"
                    # print tag.text.encode("GBK", 'ignore')
                    text += "\n"+tag.text
                #标签类型属于p或div，选取所有与该节点同一级别的p标签的文本
                elif tag.name == "p" or tag.name == "div":
                    # print u"这是一个p标签或者div标签"
                    # print tag
                    for sib in tag.parent.children:
                        if type(sib) == bs4.element.Tag:
                            if sib.name == "p":
                                p_tag_set.add(sib)
                                # print sib.text.strip()
                #标签类型属于td，选取当前td所在tr的文本
                elif tag.name == "td":
                    # print u"这是一个td标签"
                    # print tag
                    for sib in tag.parent.children:
                        if type(sib) == bs4.element.Tag:
                            if sib.name == "p":
                                text += "\n"+sib.text.strip()
            p_tag_list = list(p_tag_set)
            for p_tag in p_tag_list:
                text += "\n"+p_tag.text.strip()
            # print "text:"
            # print text.encode("GBK", 'ignore')
            save_corpus(text,key_name,rank)


def save_corpus(text,name,rank):
    corpus_path = "Corpus_Base"
    dir = corpus_path + "/" + name.replace(" ", "_")
    if not os.path.exists(dir):
        os.mkdir(dir)
    c_file = open(dir+"/"+rank,"w+")
    c_file.write(text)
    c_file.close()

if __name__=="__main__":
    path = r"weps2007_data_1.1/training/web_pages/Gregory_Brennan/raw/"
    rank = "095"
    file_name = r"/index.html"
    final_path = path + rank + file_name
    key_name = "Gregory Brennan"

    parse_html_and_save(final_path,key_name,rank)