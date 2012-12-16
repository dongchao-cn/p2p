# -*- coding: UTF-8 -*-
import socket
import sys
import MySQLdb as mdb
import string
import struct

class RequsetType:
    userReg = '00'
    userLogin = '01'
    userLogout = '02'
    shareFile = '10'
    searchFile = '11'
class AnswerType:
    success = '00'
    failed = '01'

class Server():

    # 数据库的设置
    dbHost = ''
    dbPort = 0
    dbUser = ''
    dbPasswd = ''
    dbName = ''
    
    AliveUserID = [];

    def __init__(self,dbHost = '127.0.0.1',dbPort = 3306,dbUser = 'root',dbPasswd = '1129',dbName = 'p2p'):
        self.dbHost = dbHost
        self.dbPort = dbPort
        self.dbUser = dbUser
        self.dbPasswd = dbPasswd
        self.dbName = dbName
        
    def initServer(self,dbName = 'p2p'):
        ''' 初始化Server数据库，会重置数据库内所有表 '''
        try:
            con = None
            self.dbName = dbName;
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 删除原表
            cur.execute("DROP TABLE IF EXISTS File;")
            cur.execute("DROP TABLE IF EXISTS User;")
            
            # 创建新表
            cur.execute("CREATE TABLE User(ID INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR(25) NOT NULL UNIQUE,\
                Passwd VARCHAR(25) NOT NULL,IP VARCHAR(25),ListenPort INT);")
            cur.execute("CREATE TABLE File(ID INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR(25) NOT NULL,Size INT NOT NULL,\
                UploadUserID INT,FOREIGN KEY(UploadUserID) REFERENCES User(ID) ON DELETE SET NULL ON UPDATE CASCADE);")

            print "initServer Success,All Table Reset!"
        finally:
            if con:
                con.close()
                
    def addUser(self,userName,passwd):
        ''' 添加新用户 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 添加新用户
            val = [userName,passwd]
            cur.execute("INSERT INTO User(Name,Passwd) VALUES(%s,%s);",val)
            con.commit()
            print "addUser Success,Name = %s,Passwd = %s!" % (userName,passwd)
            return True
        except:
            return False
        finally:
            if con:
                con.close()

    def delUser(self,userName):
        ''' 删除用户 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 删除用户
            val = [userName]
            cur.execute("DELETE FROM User WHERE Name = %s;",val)
            con.commit()
            print "delUser Success,Name = %s!" % userName
            return True
        except:
            return False
        finally:
            if con:
                con.close()
    def userLogin(self,userName,passwd,IP,listenPort):
        ''' 用户登陆 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 用户登陆
            val = [userName,passwd]
            cur.execute("SELECT * FROM User WHERE Name = %s AND Passwd = %s;",val)
            user = cur.fetchone()
            val = [IP,listenPort,user[0]]
            cur.execute("UPDATE User SET IP = %s ,ListenPort = %s WHERE ID = %s;",val)
            con.commit()
            print "userLogin Success,Name = %s,passwd = %s,IP = %s,ListenPort = %s!" % (userName,passwd,IP,listenPort)
            return user[0]
        except:
            return False
        finally:
            if con:
                con.close()

    def userLogout(self,UserID):
        ''' 用户注销 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 用户注销
            #val = [UserID]
            #cur.execute("SELECT * FROM User WHERE ID = %s;",val)
            #user = cur.fetchone()
            val = ['NULL','0',UserID]
            print val
            cur.execute("UPDATE User SET IP = %s ,ListenPort = %s WHERE ID = %s;",val)
            con.commit()
            print "userLogout Success,ID = %s!" % (UserID)
            return True
        #except:
            #return False
        finally:
            if con:
                con.close()
                
    def getUser(self,UserID):
        ''' 获得一个用户信息 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 获得用户信息
            val = [UserID]
            cur.execute("SELECT * FROM User WHERE ID = %s;",val)
            user = cur.fetchone()
            print "getUser Success,Name = %s,Passwd = %s,IP = %s,listenPort = %s!" % (user[1],user[2],user[3],user[4])
            return user[1],user[2],user[3],user[4]
        finally:
            if con:
                con.close()
                
    def addFile(self,fileName,fileSize,uploadUserID):
        ''' 共享一个文件 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 共享文件
            val = [fileName,fileSize,uploadUserID]
            cur.execute("INSERT INTO File(Name,Size,UploadUserID) VALUES(%s,%s,%s);",val)
            con.commit()
            print "addFile Success,Name = %s,Size = %s,uploadUserID = %s!" % (fileName,fileSize,uploadUserID)
            return True
        except:
            return False
        finally:
            if con:
                con.close()

    def delFile(self,fileName,uploadUserID):
        ''' 删除一个文件 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 删除文件
            val = [fileName,uploadUserID]
            cur.execute("SELECT * FROM File WHERE Name = %s AND UploadUserID = %s;",val)
            thefile = cur.fetchone()
            val = [thefile[0]]
            cur.execute("DELETE FROM File WHERE ID = %s;",val)
            con.commit()
            print "delFile Success,Name = %s,uploadUserID = %s!" % (fileName,uploadUserID)
        finally:
            if con:
                con.close()
                
    def getFile(self,fileName):
        ''' 获得一个文件 '''
        try:
            con = None
            con = mdb.connect(host = self.dbHost,port = self.dbPort,user = self.dbUser,\
                              passwd = self.dbPasswd,db = self.dbName,charset='utf8')
            cur = con.cursor()

            # 获得文件
            val = [fileName]
            cur.execute("SELECT * FROM File WHERE Name = %s;",val)
            thefile = cur.fetchone()
            if cur.rowcount == 0:
                return '',0,0
            print "getFile Success,Name = %s,Size = %s,uploadUserID = %s!" % (thefile[1],thefile[2],thefile[3])
            return thefile[1],thefile[2],thefile[3]
        except:
            return '',0,0
        finally:
            if con:
                con.close()
                
    def startServer(self,ip,port = 8000,maxlisten = 10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(maxlisten)
        while True:
            connection,address = sock.accept()
            reqType = connection.recv(2)
            reqContext = connection.recv(1024)
            ansType,ansContext = self.doRequest(reqType,reqContext)
            connection.send(ansType)
            connection.send(ansContext)
            connection.close()
                
    def doRequest(self,reqType,reqContext):
        #print reqType
        #print reqContext
        if reqType == RequsetType.userReg:
            # 注册用户
            Name,Passwd = struct.unpack('!25s25s',reqContext)
            Name = Name.rstrip('\0')
            Passwd = Passwd.rstrip('\0')
            #print Name,Passwd
            ansContext = ''
            if self.addUser(Name,Passwd):
                ansType = AnswerType.success
            else:
                ansType = AnswerType.failed
                ansContext = struct.pack('!100s','RegUser Failed!!!!!!!')
            return ansType, ansContext
        
        if reqType == RequsetType.userLogin:
            # 登录用户
            Name,Passwd,IP,listenPort = struct.unpack('!25s25s25sI',reqContext)
            Name = Name.rstrip('\0')
            Passwd = Passwd.rstrip('\0')
            IP = IP.rstrip('\0')
            ansContext = ''
            ret = self.userLogin(Name,Passwd,IP,listenPort)
            if ret:
                ansType = AnswerType.success
                ansContext = struct.pack('!I',ret)
            else:
                ansType = AnswerType.failed
                ansContext = struct.pack('!100s','userlogin Failed!!!!!!!')
            return ansType, ansContext

        if reqType == RequsetType.userLogout:
            # 注销用户
            UserID, = struct.unpack('!I',reqContext)
            ansContext = ''
            ret = self.userLogout(UserID)
            if ret:
                ansType = AnswerType.success
            else:
                ansType = AnswerType.failed
                ansContext = struct.pack('!100s','userLogout Failed!!!!!!!')
            return ansType, ansContext

        if reqType == RequsetType.shareFile:
            # 分享文件
            Name,Size,UploadUserID = struct.unpack('!25s2I',reqContext)
            Name = Name.rstrip('\0')
            ansContext = ''
            ret = self.addFile(Name,Size,UploadUserID)
            if ret:
                ansType = AnswerType.success
            else:
                ansType = AnswerType.failed
                ansContext = struct.pack('!100s','shareFile Failed!!!!!!!')
            return ansType, ansContext

        if reqType == RequsetType.searchFile:
            # 查找文件
            Name, = struct.unpack('!25s',reqContext)
            Name = Name.rstrip('\0')
            ansContext = ''
            (a,Size,UploadUserID) = self.getFile(Name)
            if UploadUserID == 0:
                ansType = AnswerType.failed
                ansContext = struct.pack('!100s','No Such File!!!!!!!')
            else:
                (UploadUserName,b,IP,ListenPort) = self.getUser(UploadUserID)
                if IP:
                    # 当前用户在线
                    ansType = AnswerType.success
                    ansContext = struct.pack('!25s2I25sI',Name,Size,UploadUserID,str(UploadUserName),1)
                else:
                    ansType = AnswerType.success
                    ansContext = struct.pack('!25s2I25sI',Name,Size,UploadUserID,str(UploadUserName),0)
            return ansType, ansContext
        
if __name__ == '__main__':
    server = Server()
    server.initServer()
    server.addUser('dc','123')
    #print server.getUser(1)
    #server.delUser('dc')
    #server.userLogin('dc','ddd','127.0.0.1',8888,7000)
    #server.getUser(1)
    #server.addFile('1.txt',20,1)
    #server.addFile('3.txt',20,1)
    #server.addFile('2.txt',20,1)
    #server.delFile('3.txt',1)
    #info = server.getFile(1)
    localIP = socket.gethostbyname(socket.gethostname())
    server.startServer(localIP)
    
    
