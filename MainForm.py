# -*- coding: UTF-8 -*-
import wx

from client import Client

class MainFrame(wx.Frame):
    UserID = 0
    def __init__(self, parent, id, uid):
        
        self.UserID = uid
        self.client = Client()
        wx.Frame.__init__(self, parent, id, u'P2P分享',size=(800, 400))
        panel = wx.Panel(self) #创建画板

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        # 分享文件
        shareFileButton = wx.Button(panel, label=u"分享文件", pos=(10, 8),size=(70, 25))
        wx.StaticText(panel, -1, u"当前分享文件:", pos=(10, 40))

        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.shareFile, shareFileButton)
        
        self.shareFilelistCtl = wx.ListCtrl(panel,-1,pos=(10,60),size = (200,200),style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.shareFilelistCtl.InsertColumn(1,u"文件名")
        self.shareFilelistCtl.SetColumnWidth(0, 190)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnShareItemRClick, self.shareFilelistCtl)
        
        # 搜索文件
        self.searchCtrl = wx.TextCtrl(panel, -1, "", pos=(250, 10))
        searchButton = wx.Button(panel, label=u"搜索文件", pos=(360, 10),size=(60, 25))
        self.Bind(wx.EVT_BUTTON, self.searchFile, searchButton)
        wx.StaticText(panel, -1, u"右键下载！", pos=(250, 40))

        self.searchFilelistCtl = wx.ListCtrl(panel,-1,pos=(250,60),size = (500,200),style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.searchFilelistCtl.InsertColumn(1,u"文件名")
        self.searchFilelistCtl.InsertColumn(2,u"文件大小")
        self.searchFilelistCtl.InsertColumn(3,u"上传文件用户ID")
        self.searchFilelistCtl.InsertColumn(3,u"上传文件用户名")
        self.searchFilelistCtl.InsertColumn(4,u"当前是否在线")
        self.searchFilelistCtl.InsertColumn(5,u"对方IP")
        self.searchFilelistCtl.InsertColumn(6,u"对方端口")
        self.searchFilelistCtl.SetColumnWidth(0, 100)
        self.searchFilelistCtl.SetColumnWidth(1, 80)
        self.searchFilelistCtl.SetColumnWidth(2, 100)
        self.searchFilelistCtl.SetColumnWidth(3, 100)
        self.searchFilelistCtl.SetColumnWidth(4, 100)
        self.searchFilelistCtl.SetColumnWidth(5, 100)
        self.searchFilelistCtl.SetColumnWidth(6, 100)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnSearchItemRClick, self.searchFilelistCtl)
        
        #listCtl.InsertStringItem(1,"1")
        #listCtl.InsertStringItem(2,"2")

        #listCtl.SetStringItem(1,0,"123")

        # 获得共享文件
        fileList = self.client.getMyShareFile(self.UserID)
        if fileList:
            for item in fileList:
                self.shareFilelistCtl.InsertStringItem(0,item)
        
    def shareFile(self, event):
        getFileDlg = wx.FileDialog(self,u"选择需要分享的文件")
        getFileDlg.SetDirectory(self.client.sendDir)
        getFileDlg.ShowModal()
        #fileName = getFileDlg.GetDirectory() + getFileDlg.GetFilename()
        # 这里文件路径固定为Client.sendDir,选择其他路径下的文件肯定会出错。。。
        assert getFileDlg.GetDirectory()+'\\' == self.client.sendDir
        
        fileName = getFileDlg.GetFilename()
        assert self.UserID != 0
        self.client.shareFile(fileName,self.UserID)
        dlg = wx.MessageDialog(None,u'分享成功！','',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.shareFilelistCtl.InsertStringItem(1,fileName)


    def OnShareItemRClick(self,evt):
        itemID = evt.GetIndex()
        item = self.shareFilelistCtl.GetItem(itemID)
        dlg = wx.MessageDialog(None,u"是否取消分享文件:'%s'?" % str(item.GetText()),'',wx.YES_NO)
        ret = dlg.ShowModal()
        dlg.Destroy()
        if (ret == wx.ID_YES):
            fileName = item.GetText()
            UploadUserID = self.UserID
            self.client.stopShareFile(fileName,UploadUserID)
            self.shareFilelistCtl.DeleteItem(itemID)
            dlg = wx.MessageDialog(None,u"取消分享！",'',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            print 'No'
    
    def searchFile(self, event):
        fileName = self.searchCtrl.GetValue()
        fileName,fileSize,UploadUserID,UploadUserName,Online,IP,ListenPort = self.client.searchFile(fileName)
        if fileName == '':
            dlg = wx.MessageDialog(None,u'未找到此文件！','',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        self.searchFilelistCtl.InsertStringItem(0,fileName)
        self.searchFilelistCtl.SetStringItem(0,1,str(fileSize))
        self.searchFilelistCtl.SetStringItem(0,2,str(UploadUserID))
        self.searchFilelistCtl.SetStringItem(0,3,UploadUserName)
        if Online == 1:
            self.searchFilelistCtl.SetStringItem(0,4,'True')
            self.searchFilelistCtl.SetStringItem(0,5,IP)
            self.searchFilelistCtl.SetStringItem(0,6,str(ListenPort))
        else:
            self.searchFilelistCtl.SetStringItem(0,4,'False')

    def OnSearchItemRClick(self, evt):
        itemID = evt.GetIndex()
        item = self.searchFilelistCtl.GetItem(itemID)
        dlg = wx.MessageDialog(None,u"是否下载文件:'%s'?" % str(item.GetText()),'',wx.YES_NO)
        ret = dlg.ShowModal()
        dlg.Destroy()
        if (ret == wx.ID_YES):
            fileName = self.searchFilelistCtl.GetItem(itemID,0).GetText()
            fileSize = int(self.searchFilelistCtl.GetItem(itemID,1).GetText())
            DisIP = self.searchFilelistCtl.GetItem(itemID,5).GetText()
            DisPort = int(self.searchFilelistCtl.GetItem(itemID,6).GetText())
            self.client.getFile(fileName,fileSize,DisIP,DisPort)
            dlg = wx.MessageDialog(None,u"下载完成！",'',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            print 'No'
        
        
 
    def OnCloseWindow(self, event):
        self.client.userLogout(self.UserID)
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
