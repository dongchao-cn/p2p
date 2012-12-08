# -*- coding: UTF-8 -*-
import wx
from client import Client

class RegFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'注册用户',size=(270, 110))
        panel = wx.Panel(self) #创建画板

        # 控件
        wx.StaticText(panel, -1, u"用户名:", pos=(10, 12))
        self.userNameCtrl = wx.TextCtrl(panel, -1, "", pos=(60, 10))
        
        wx.StaticText(panel, -1, u"密码:", pos=(10, 42))
        self.userPasswdCtrl = wx.TextCtrl(panel, -1, "", pos=(60, 40))

        LoginButton = wx.Button(panel, label=u"注册", pos=(180, 10),size=(50, 50)) #将按钮添加到画板
        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.Reg, LoginButton)

    def Reg(self, event):
        userName = self.userNameCtrl.GetValue()
        userPasswd = self.userPasswdCtrl.GetValue()
        if not userName or not userPasswd:
            return
        client = Client()
        if not client.userReg(userName,userPasswd):
            dlg = wx.MessageDialog(None,u'注册失败',u'错误',wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # 用户注册成功
            dlg = wx.MessageDialog(None,u'注册成功',u'成功',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.Destroy()
            
    def OnCloseWindow(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = RegFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
