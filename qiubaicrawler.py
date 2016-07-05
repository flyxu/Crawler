# coding=utf-8

import urllib2
import re
import sys
from socket import error as SocketError
import errno
import csv
reload(sys)
sys.setdefaultencoding('utf8')
class QSBK:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent': self.user_agent}
        #self.stories=[]    #每个元素是一页段子
        self.enable=True
        self.pageindex=1
    def getPage(self,pageindex):
        try:
             url='http://www.qiushibaike.com/hot/page/'+str(pageindex)
             request=urllib2.Request(url,headers=self.headers)
             response=urllib2.urlopen(request)
             pagecode=response.read().decode('utf-8')
             return pagecode
        except urllib2.URLError, e:
             if hasattr(e,'code'):
                 print e.code
                 return None
             if hasattr(e,'reason'):
                 print u'链接失败，错误原因',e.reason
                 return None
        except SocketError as e:
            if e.errno!=errno.ECONNRESET:
                raise Exception('not value')
            pass
    def getPageItems(self,pageindex):
        pagecode=self.getPage(pageindex)
        if not pagecode:
            print 'page load error'
            return None
        pattern=re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        items=re.findall(pattern,pagecode)
        pagestories=[]
        for item in items:
            pagestories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pagestories
    def writefile(self,story,page):
        file_object=open('./qiushibaike.csv','a')
        file=csv.writer(file_object)
        file.writerow(['第%d页'%page,story[0],story[2],story[1]])
        file_object.close()


    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，Q退出'
        self.enable=True
        while self.enable:
            pageStories=self.getPageItems(self.pageindex)
            for story in pageStories:
                input=raw_input()
                if input=='Q':
                    self.enable=False
                    return
                print u"第%d页\t发布人：%s\t 赞：%s\n%s" % (self.pageindex,story[0], story[2], story[1])
                self.writefile(story,self.pageindex)
            self.pageindex+=1


qsbk=QSBK()
qsbk.start()





