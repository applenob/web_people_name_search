#coding=utf-8
from parse_html import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

path = r"weps2007_data_1.1/training/web_pages/"
names = os.listdir(path)
for name in names:
    rank_num = len(os.listdir(path+name+r"/raw"))
    ranks = ["%03d" %i for i in range(rank_num)]
    for rank in ranks:
        file_name = path+name+r"/raw"+r"/"+rank+r"/index.html"
        # print file_name
        parse_html_and_save(file_name,name.replace("_"," "),rank)


