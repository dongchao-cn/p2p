# -*- coding: UTF-8 -*-
import wx

from client import Client

class MainFrame(wx.Frame):
    UserID = 0
    def __init__(self, parent, id):
        self.client = Client()
        wx.Frame.__init__(self, parent, id, u'P2P分享',size=(600, 400))
        panel = wx.Panel(self) #创建画板
        # 控件
        shareFileButton = wx.Button(panel, label=u"分享文件", pos=(10, 8),size=(70, 25)) #将按钮添加到画板

        wx.StaticText(panel, -1, u"当前分享文件:", pos=(10, 40))

        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.shareFile, shareFileButton)

        self.shareFilelistCtl = wx.ListCtrl(panel,-1,pos=(10,60),size = (300,200),style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.shareFilelistCtl.InsertColumn(1,u"文件名")
        self.shareFilelistCtl.SetColumnWidth(0, 200)
        #listCtl.InsertStringItem(1,"1")
        #listCtl.InsertStringItem(2,"2")

        #listCtl.SetStringItem(1,0,"123")
        
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
        
    def OnCloseWindow(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
