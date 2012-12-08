# -*- coding: UTF-8 -*-
import wx
from MainForm import MainFrame
from client import Client

class LoginFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'登录',size=(270, 110))
        panel = wx.Panel(self) #创建画板

        # 控件
        wx.StaticText(panel, -1, u"用户名:", pos=(10, 12))
        self.userNameCtrl = wx.TextCtrl(panel, -1, "", pos=(60, 10))
        
        wx.StaticText(panel, -1, u"密码:", pos=(10, 42))
        self.userPasswdCtrl = wx.TextCtrl(panel, -1, "", pos=(60, 40))

        LoginButton = wx.Button(panel, label=u"登录", pos=(180, 10),size=(50, 50)) #将按钮添加到画板
        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.Login, LoginButton)

    def Login(self, event):
        userName = self.userNameCtrl.GetValue()
        userPasswd = self.userPasswdCtrl.GetValue()
        if not userName or not userPasswd:
            return
        print userName , userPasswd
        client = Client()
        #client.userReg('dc','123')
        ID = client.userLogin(userName,userPasswd)
        if not ID:
            dlg = wx.MessageDialog(None,u'登录失败，用户名或密码错误',u'错误',wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # 用户登录成功
            mainFrame = MainFrame(parent=None, id=-1)
            mainFrame.Show()
            mainFrame.UserID = ID
            self.Destroy()
            pass
            
    def OnCloseWindow(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = LoginFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
