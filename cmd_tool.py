#coding=utf-8
import sys,cmd
from xml2dict import xml2dict,dict2xml
reload(sys)
sys.setdefaultencoding('gb2312')

class MyCMD(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(cer)>'
        self.intro = u'''xml2dict使用说明：
        EOF 退出系统
        x2d xml ---> dict ,参数：path
        d2x dict ---> xml，参数：path'''
        self.path = r'weps2007_data_1.1\traininig\description_files\Abby_Watkins.xml'

    def help_EOF(self):
        print u"===退出程序==="
    def do_EOF(self,line):
        sys.exit()

    def help_x2d(self):
        print u"===xml ---> dict ,参数：path==="
    def do_x2d(self,path):
        # if path=="": path = raw_input(u"===输入源xml的路径===")
        if path=="": path = self.path
        # print path
        self.dict = xml2dict(path)
        print u"转换成功，字典保存在self.dict中"

    def help_d2x(self):
        print u"===dict ---> xml，参数：path==="
    def do_d2x(self,path):
        if path=="": path = raw_input(u"===输入xml的保存路径===\n>")
        if self.dict==None:self.dict = raw_input(u"===输入xml的保存路径===\n>")
        dict2xml(self.dict,path)
        print u"保存成功"

if __name__ == "__main__":
    mycmd = MyCMD()
    mycmd.cmdloop()