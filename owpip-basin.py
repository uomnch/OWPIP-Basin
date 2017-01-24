import subprocess
import os
import wx
import commands

class LabelViewerPanel(wx.Panel):
    '''Class to create panel on the frame'''
    
    def __init__(self, parent, image, name, panel_size):
        wx.Panel.__init__(self, parent, size=panel_size)
        self.frame = parent
        self.name = name
        self.Bind(wx.EVT_CHAR, self.on_keypress)
        self.cursor = wx.StockCursor(wx.CURSOR_BLANK)
        self.BackgroundColour = wx.BLACK
        self.widgets = []
        self.image = image
        
        # Uncomment the following line on wxpython 2.x
        # self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.draw_image)
        
                
    def hide_cursor(self):
        for widget in self.widgets:
            widget.SetCursor(self.cursor)

    def on_keypress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.frame.close()

    def draw_image(self, event):
        """ Draws the image to the panel's background. """
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Bitmap(self.image)
        dc.DrawBitmap(image, 0, 0)
        self.SetFocus()

    def switch_panel(self, event):
        self.frame.switch_panel(self.name, event.GetEventObject().GetName())
    
    def add_button(self, image_path, img_name, position):
        image_path = './images/buttons/' + image_path
        bmp = wx.Bitmap(image_path, wx.BITMAP_TYPE_PNG)
        widget = wx.StaticBitmap(self, name=img_name, pos=position, bitmap=bmp)
        widget.Bind(wx.EVT_LEFT_DOWN, self.switch_panel)
        self.widgets.append(widget)
        
class MainPanel(LabelViewerPanel):
    '''   Main home screen. '''
    def __init__(self, parent, image, name, panel_size):
        LabelViewerPanel.__init__(self, parent, image, name, panel_size)
        self.add_button('HomePage/Diorama.png', 'Diorama', (0, 0))
        self.add_button('HomePage/Archaeology.png', 'Archaeology', (520, 0))
        self.add_button('HomePage/GoSeeIt.png', 'GoSeeIt', (1052, 0))
        self.hide_cursor()
        self.SetFocus()

class LabelPanel(LabelViewerPanel):
    '''Add Buttons on other screen except Main'''
    def __init__(self, parent, background, name, panel_size, level, back_level):
        LabelViewerPanel.__init__(self, parent, background, name, panel_size)

        if(level==1.1):
            self.add_button('home.png', 'main', (22, 800))
        elif(level==1.2):
            self.add_button('home.png', 'main', (22, 800))
            self.add_button('Diorama/Chubs.png', 'Chubs', (722, 780))
            self.add_button('Diorama/Hawk.png', 'Hawk', (30, 70))
            self.add_button('Diorama/Jackrabbit.png', 'Jackrabbit', (695, 580))
            self.add_button('Diorama/Marsh.png', 'Marsh', (892, 298))
            self.add_button('Diorama/Rabbitbrush.png', 'Rabbitbrush', (906, 658))
            self.add_button('Diorama/Sagebrush.png', 'Sagebrush', (20, 562))
            self.add_button('Diorama/Wikiup.png', 'Wikiup', (179, 348))
            self.add_button('artist.png', 'Artist', (1362, 798))
        elif(level==1.3):
            self.add_button('home.png', 'main', (22, 800))
            self.add_button('more.png', 'GoSeeItAshfall', (1122, 558))
            self.add_button('more.png', 'GoSeeItHistory', (1122, 646))
        elif(level==2):
            self.add_button('home.png', 'main', (22, 800))
            self.add_button('back.png', back_level, (250, 800))

        self.hide_cursor()
        
            
class MainFrame(wx.Frame):
    """    Create Background Frame and create panels for each page   """

    def __init__(self, parent, image_size):
        wx.Frame.__init__(self, parent, wx.ID_ANY, size=image_size)
        self.size = image_size
        self.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
        self.panels = []
        self.panel_dict = {}

        main_panel = MainPanel(self, './images/pages/HomePage.png', 'main', image_size)
        self.panel_dict['main'] = main_panel

        self.add_panel('Archaeology', 1.1)
        self.add_panel('Diorama', 1.2)
        self.add_panel('GoSeeIt', 1.3)
        self.add_panel('Artist', 2, 'Diorama')
        self.add_panel('Chubs', 2, 'Diorama')
        self.add_panel('Hawk', 2, 'Diorama')
        self.add_panel('Jackrabbit', 2, 'Diorama')
        self.add_panel('Marsh', 2, 'Diorama')
        self.add_panel('Rabbitbrush', 2, 'Diorama')
        self.add_panel('Sagebrush', 2, 'Diorama')
        self.add_panel('Wikiup', 2, 'Diorama')
        self.add_panel('GoSeeItAshfall', 2, 'GoSeeIt')
        self.add_panel('GoSeeItHistory', 2, 'GoSeeIt')

        # Timer to switch back to main shelf
        self.timeout = 600000  # 10 min
        self.timeout_timer = wx.Timer(self, wx.ID_ANY)
        self.start_timeout_timer()

    def add_panel(self, name, level, back_level='None'):
        bg = './images/pages/'+ name +'.png'
        panel = LabelPanel(self, bg, name, self.size, level, back_level)
        panel.Hide()
        self.panel_dict[name] = panel
        
    def switch_panel(self, src_id, dest_id):
        print src_id +'->'+ dest_id
        self.panel_dict[src_id].Hide()
        self.panel_dict[dest_id].Show()
        self.panel_dict[dest_id].SetFocus()
        self.current_panel = dest_id
        self.Layout()
        self.restart_timeout_timer()

    def start_timeout_timer(self):
        self.Bind(wx.EVT_TIMER, self.switch_on_timeout, self.timeout_timer)
        self.timeout_timer.Start(self.timeout)

    def restart_timeout_timer(self):
        self.timeout_timer.Stop()
        self.start_timeout_timer()

    def switch_on_timeout(self, event):
        self.switch_panel(self.current_panel, 'main')
        self.restart_timeout_timer()

    def close(self):
        self.Destroy()


        
if __name__ == '__main__':
    app = wx.App(False)
    MainFrame(None, (1900, 900))
    app.MainLoop()

