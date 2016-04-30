#coding=utf-8
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import xml.etree.cElementTree as ET
import os
import re

def xml2dict(path):
    assert os.path.exists(path)
    assert re.match('.+\.xml',path)
    parsed = ET.parse(path)
    # root代表根标签“sentences”
    root = parsed.getroot()
    # print root.tag
    # print type(root)
    return trans(root)


def trans(element):
    '''递归实现xml元素转换到字典类型'''
    assert isinstance(element, ET.Element)
    ret = {}
    attr = dict(element.attrib)
    # print element
    if len(element) != 0:
        value = []
        for child in element:
            value.append(trans(child))
    else: value = element.text

    if attr != None :
        ret[element.tag] = attr
    if value != None :
        if attr == None:
            ret[element.tag] = {}
        ret[element.tag]["value"] = value
    return ret

def dict2xml(dic,path):
    assert isinstance(dic,dict)
    root = dic.keys()[0]
    e = ET.Element(root)
    e = back(e,dic)
    # for child in e:
        # print child
    tree = ET.ElementTree(e)
    tree.write(path, 'utf8')

def back(e,dic):
    '''递归实现字典类型转换到xml元素
    e:当前节点的element
    dic:当前节点对应的字典'''

    #如果此节点有值（或者子节点），dic[dic.keys()[0]]代表字典的第一个key对应的值
    if dic[dic.keys()[0]].has_key('value'):
        if isinstance(dic[dic.keys()[0]]['value'], list):
            # print "list"
            for child in dic[dic.keys()[0]]['value']:
                # print child.keys()[0]
                e_child = ET.Element(child.keys()[0])
                e.append(back(e_child, child))
        else:
            e.text = dic[dic.keys()[0]]['value']
    #获取此节点所有属性值
    for key in (dic[dic.keys()[0]]).keys():
        if key != "value":
            e.attrib[key] = dic[dic.keys()[0]][key]
    return e


if __name__ == '__main__':
    path = r'weps2007_data_1.1\traininig\description_files'
    file_name = r'\Abby_Watkins.xml'
    dic = xml2dict(path+file_name)
    dict2xml(dic,'test.xml')