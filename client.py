# -*- coding: UTF-8 -*-
import socket
import struct
import os
import thread
import random


class RequsetType:
    userReg = '00'
    userLogin = '01'
    userLogout = '02'
    shareFile = '10'
    getFile = '11'
class AnswerType:
    success = '00'
    failed = '01'

    
class Client:
    ServerIP = ''
    ServerPort = 0

    LocalIP = ''
    LocalPort = 0
    LocalListenPort = 0
    
    sock = None
    sockListen = None
    getFileSock = None

    sendDir = u'E:\\p2p\\send\\'
    downloadDir = u'E:\\p2p\\down\\'
    
    def __init__(self):
        thread.start_new_thread(self.__listenForOtherClient,())
        self.LocalIP = socket.gethostbyname(socket.gethostname())
        pass
    
    def __listenForOtherClient(self):
        ''' 监听等待其他Client的连接请求 '''
        self.sockListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.LocalListenPort = random.randint(7000, 7999)
        self.sockListen.bind((self.LocalIP, self.LocalListenPort))
        self.sockListen.listen(10)
        
        while True:
            connection,address = self.sockListen.accept()
            # 这里接收到文件名
            fileName = connection.recv(25)
            # 发送文件
            # 对文件分块，一次4K
            fp = open(self.sendDir + fileName,'rb')
            while 1:
                filedata = fp.read(1024 * 4)
                if not filedata:
                    break
                connection.send(filedata)
            connection.close()

        #thread.exit_thread()
        
    def __connectServer(self,ServerIP,ServerPort = 8000):
        ''' 连接服务器，每次请求就需要连接一次 '''
        self.ServerIP = ServerIP
        self.ServerPort = ServerPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ServerIP, self.ServerPort))
        self.LocalPort = self.sock.getsockname()[1]
        
    def __Request(self,reqType,reqContext):
        localIP = socket.gethostbyname(socket.gethostname())
        self.__connectServer(localIP)
        self.sock.send(reqType)
        self.sock.send(reqContext)
        ansType = self.sock.recv(2)
        asnContext = self.sock.recv(1024)
        return ansType,asnContext

    def userReg(self,Name,Passwd):
        ''' 用户注册 ''' 
        reqContext = struct.pack('!25s25s',str(Name),str(Passwd))
        ansType,asnContext = self.__Request(RequsetType.userReg,reqContext)
        if ansType != AnswerType.success:
            print 'userReg failed: %s' % asnContext
            return False
        else:
            print 'userReg success!'
            return True

    def userLogin(self,Name,Passwd):
        ''' 用户登录，返回值为用户ID '''
        reqContext = struct.pack('!25s25s25sI',str(Name),str(Passwd),self.LocalIP,self.LocalListenPort)
        ansType,ansContext = self.__Request(RequsetType.userLogin,reqContext)
        if ansType != AnswerType.success:
            print 'userLogin failed: %s' % ansContext
            return False
        else:
            ID, = struct.unpack('!I',ansContext)
            print 'userLogin success: ID = %s' % ID
            return ID

    def userLogout(self,Name,Passwd):
        ''' 用户注销 '''
        reqContext = struct.pack('!25s25s',str(Name),str(Passwd))
        ansType,asnContext = self.__Request(RequsetType.userLogout,reqContext)
        if ansType != AnswerType.success:
            print 'userLogout failed: %s' % asnContext
        else:
            print 'userLogout success!'

    def shareFile(self,Name,UploadUserID):
        ''' 分享文件 '''
        statinfo = os.stat(self.sendDir + Name)
        reqContext = struct.pack('!25s2I',str(Name),statinfo.st_size,UploadUserID)
        
        ansType,asnContext = self.__Request(RequsetType.shareFile,reqContext)
        if ansType != AnswerType.success:
            print 'shareFile failed: %s' % asnContext
        else:
            print 'shareFile success!'

    def getFile(self,Name,SaveDir = downloadDir):
        ''' 查找文件 '''
        reqContext = struct.pack('!25s',str(Name))
        ansType,asnContext = self.__Request(RequsetType.getFile,reqContext)
        if ansType != AnswerType.success:
            print 'getFile failed: %s' % asnContext
        else:
            Size,DisIP,DisPort = struct.unpack('!I25sI',asnContext)
            DisIP = DisIP.rstrip('\0')
            self.__getFile(Name,Size,DisIP,DisPort)
            print 'getFile success! %s' %Name 
            
    def __getFile(self,fileName,fileSize,DisIP,DisPort):
        self.getFileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.getFileSock.connect((DisIP, DisPort))
        # 发送文件名
        self.getFileSock.send(fileName)
        restsize = fileSize
        # 接受文件
        # 对文件分块，一次4K
        fp = open(self.downloadDir + fileName,'wb')
        while 1:
            if restsize > 1024 * 4:
                filedata = self.getFileSock.recv(1024 * 4)
            else:
                filedata = self.getFileSock.recv(restsize)
            fp.write(filedata)
            restsize = restsize-len(filedata)
            if restsize == 0:
                break

if __name__ == '__main__':
    client = Client()
    #client.listenForOtherClient()
    #client.Request('ddddd')
    #client.userReg('dc','123')
    ID = client.userLogin('dc','123')

    #client.shareFile('osrloaderv30.zip',ID)

    #os.system("pause")
    
    #client.getFile('osrloaderv30.zip')

    #client.userLogout('dc','123')


