#coding:utf-8
'''
 html代码补全
 "<tag>xxx</tag>"正常
 "<tag/>"正常
 "<tag>xxx"异常-没有关闭标签
 "xxx</tag>"异常-没有开始标签
'''
'''
这段代码在这里没有用上，html补全直接使用bs4的prettify()
'''
import re

html = '''
<h>xxx<a>xxx<b>xxx<b>xxx</c>xxx<b>xxx</a>xxx</h>
'''

def check(html):
    #tag栈
    tagStack = []
    tagDict = {}
    #匹配tag
    m = re.compile('<[^>,^<]*>')
    allTags =  m.findall(html)
    print allTags
    for index, tag in enumerate(allTags):
        if judgeValid(tag):
            tagName = getTagName(tag)
            if tagName[0] != '/':#是前标签
                tagStack.append(tagName)
            elif tagName[0] == '/':#是闭合标签
                #闭合标签和栈顶标签匹配
                if cmp(tagStack[-1],getCloseTagName(tagName)) == 0:
                    tagStack.pop()
                # 闭合标签和栈顶标签不匹配
                else :
                    tagCloseStack = getTagCloseStack(index, allTags)
                    # print "tagCloseStack:"
                    # print tagCloseStack
                    stackIndex = judgeStack(tagStack, tagCloseStack)
                    print index,tagName, tagStack, stackIndex
                    if stackIndex :
                        #关闭标签丢失
                        tmpCloseTag = ''
                        for i in xrange(stackIndex) :
                            tmptag = tagStack.pop()
                            tmpCloseTag += '</%s>'%tmptag
                        putTagDict(index, tmpCloseTag, tagDict, 1)
                        tagStack.pop()
                    else :
                        #没有开标签
                        putTagDict(index-1, '<%s>'%getCloseTagName(tagName), tagDict, 0)
        #print index,tag
    print tagDict
    return tagDict

'''''
  #返回标签栈与关闭标签栈首对应的位置
  #如果大于0,对应数量的关闭标签丢失
  #如果等于0当前关闭标签的开始标签丢失
'''
def judgeStack(tagStack, tagCloseStack):
    j = 0
    tmpi = 0
    for i,tmpTagName  in enumerate(tagStack[::-1]):
        if cmp(tmpTagName, getCloseTagName(tagCloseStack[j])) == 0 :
            if j == 0 :
                tmpi = i
            if j == len(tagCloseStack)-1 :
                return tmpi
            if i == len(tagStack)-1 :
                return tmpi
            j += 1
        else :
            if j > 0 :
                if cmp(tmpTagName, getCloseTagName(tagCloseStack[0])) == 0 :
                    j =1
                    tmpi = i
                else :
                    j = 0
                    tmpi = 0
    return 0

'''''得到关闭标签的名字'''
def getCloseTagName(closeTagName):
    return closeTagName[1:len(closeTagName)]

'''''
    #得到关闭标签的栈
    #这个栈是包含本关闭标签以及之后的连续的所有关闭标签
    #比如['<h>', '<a>', '<b>', '<b>', '</c>', '<b>', '</a>', '</h>']
    #index=4，即</c>
    #后面虽然有其他的关闭标签，但是不连续，所以返回['/c']'''
def getTagCloseStack(index,allTags):
    tagCloseStack = [getTagName(allTags[index])]
    i=1
    while True:
        if index+i < len(allTags):
            tmpTagName = getTagName(allTags[index+i])
            if tmpTagName[0] == '/':
                tagCloseStack.append(tmpTagName)
                i += 1
            else :
                return tagCloseStack
        else :
            return tagCloseStack

'''''
  #存入标签字典
  #static 1:缺少关闭标签,0:缺少开始标签
'''
def putTagDict(index, tag, tagDict, static):
    if index in tagDict :
        if static in tagDict[index]:
            if static :
                tagDict[index][static] += tagDict[index][static] + tag
            else :
                tagDict[index][static] +=  + tag + tagDict[index][static]
        else :
                tagDict[index][static] = tag
    else :
        tagDict[index] = {}
        tagDict[index][static] = tag

'''''是否是有效的标签'''
def judgeValid(tag):
    # 注释标签
    if cmp(tag[1], '!') == 0:
        return False
    # 单独结束标签
    if cmp(tag[-2], '/') == 0:
        return False
    return True

'''''得到标签名'''
def getTagName(tag):
    return tag[1:-1].split(' ')[0]

'''''找到标签在文件中的位置'''
def findTagBefore(number, html):
    m = re.compile('<[^>,^<]*>')
    allTags =  m.findall(html)
    start = 0

    for index, tag in enumerate(allTags) :
        tagIndex = html.find(tag, start)
        start = tagIndex + 1
        if index == number :
            return tagIndex

def findTagAfter(number,html):
    index = findTagBefore(number, html)
    return html.find('>', index) + 1

'''''在html中插入缺少的标签'''
def insert(original, new, pos):
    return original[:pos] + new + original[pos:]

'''''修复HTML'''
def fixHtml(html):
    tagDict = check(html)
    keys = tagDict.keys()
    keys.sort(reverse=True)
    for key in keys :
        if 1 in tagDict[key] :
            index = findTagBefore(key, html)
            html = insert(html, tagDict[key][1], index)
        if 0 in tagDict[key] :
            index = findTagAfter(key, html)
            html = insert(html, tagDict[key][0], index)

    return html

if __name__ == '__main__':
    '''
    #测试案例的输入是：
    <h>xxx<a>xxx<b>xxx<b>xxx</c>xxx<b>xxx</a>xxx</h>
    #测试案例的输出是：
    <h>xxx<a>xxx<b>xxx<b><c>xxx</c>xxx<b>xxx</b></b></b></a>xxx</h>
    '''
    print fixHtml(html)
