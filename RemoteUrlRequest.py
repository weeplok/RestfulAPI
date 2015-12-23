__author__ = 'neptunese'

import os
import urllib
import urllib2
import cookielib

import json


class RemoteUrlRequest(object):

    def __init__(self, ip='172.16.42.7', port=5000, protocol='http', label=None):
        self.ip = ip
        self.port = port
        self.protocol = protocol

        cookie = cookielib.CookieJar()
        self.cookie = urllib2.HTTPCookieProcessor(cookie)
        self.label = None or label

    def get(self, url='http://172.16.42.7:5000'):
        print '-'*20 + 'get method' + '-'*20
        command = 'curl -i ' + self.protocol + '://' + self.ip + ':' + str(self.port) + url
        # print "get command is: %s" % command
        opener = urllib2.build_opener(self.cookie)
        header = {'User-Agent': 'windows7'}
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        resdata = urllib2.urlopen(req)
        print resdata.read()
        print '-'*23 + 'end' + '-'*23 + '\n'

    def post(self, data={}, url='http://172.16.42.7:5000/todo/api/v1.0/tasks/upload'):
        print '-'*20 + 'post method' + '-'*20
        if not isinstance(data, dict):
            print "Data type Error raised..exit"
            print '-'*23 + 'end' + '-'*23 + '\n'
            exit()

        jdata = json.dumps(data)
        req = urllib2.Request(url, jdata)
        req.add_header('Content-Type', 'application/json')
        print req
        resdata = urllib2.urlopen(req)
        print resdata.read()
        print '-'*23 + 'end' + '-'*23 + '\n'

    def put(self, url='http://172.16.42.7:5000/todo/api/v1.0/tasks/download'):
        print '-'*20 + 'put method' + '-'*20
        req = urllib2.Request(url)
        # req.add_header('Content-Type', 'application/json')
        resdata = urllib2.urlopen(req)
        print resdata.read()
        print '-'*23 + 'end' + '-'*23 + '\n'

    @staticmethod
    def createdata(num=100):
        dd = {}
        import datetime
        import random
        import uuid
        for i in range(num):
            index = '0x00' + str(i)
            pdate = datetime.date(2015, 1, 1) + datetime.timedelta(days=random.randint(1, 50))
            date = pdate.strftime('%Y-%m-%d')
            amount = 1000*random.randrange(0, 100)
            em = {'index': index, 'date': date, 'amount': amount}
            uid = uuid.uuid4()
            dd[str(uid)] = em

        return dd


# os.system(r'curl -i http://172.16.42.7:5000/todo/api/v1.0/tasks url -i http://172.16.42.7:5000/todo/api/v1.0/tasks')

if __name__ == '__main__':

    request = RemoteUrlRequest()
    request.get()
    data_dic = RemoteUrlRequest.createdata()
    data_tmp = {'name': 'anamemout',  'code': '0x1111121'}
    request.post(data=data_dic)
    request.put()
