#coding=utf-8
import os
from xml2dict import xml2dict,dict2xml


def from_xml_2_dic():
    # path = r'weps2007_data_1.1\traininig\description_files'
    # file_name = r'\Abby_Watkins.xml'
    path = r'weps2007_data_1.1\traininig\truth_files'
    file_name = r'\Abby_Watkins.clust.xml'
    dic = xml2dict(path+file_name)
    print dic
    dict2xml(dic,'test2.xml')


if __name__ == '__main__':
    from_xml_2_dic()

