import xbmcgui
 
try: Emulating = xbmcgui.Emulating
except: Emulating = False 
 
class Example(xbmcgui.WindowDialog): 
    """
        Example Showing Of Using Sub Buttons Module to Create
        Buttons on a Window
    """
    def __init__(self,):
        if Emulating: xbmcgui.WindowDialog.__init__(self)
        setupButtons(self,10,10,100,30,"Vert")
        self.h1 = addButon(self,"Click Me")
        self.something = addButon(self,"Something")
        self.btn_quit = addButon(self,"Quit")
    def onControl(self, c):
        if self.h1 == c:
            print "hey"
        if self.something == c:
            print "you press med"
        if self.btn_quit == c:
            self.close()

### The adding button Code (only really need this bit)
def setupButtons(self,x,y,w,h,a="Vert",f=None,nf=None):
    self.numbut  = 0
    self.butx = x
    self.buty = y
    self.butwidth = w
    self.butheight = h
    self.butalign = a
    self.butfocus_img = f
    self.butnofocus_img = nf
 
def addButon(self,text):
    #self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=10, textOffsetY=2, alignment=4, font=None, textColor=None, disabledColor=None, angle=0, shadowColor=None, focusedColor=None
    c =  xbmcgui.ControlButton(self.butx + (self.numbut * self.butwidth), self.buty, self.butwidth, self.butheight, text)
    self.addControl(c)
    self.numbut += 1
    return c
### The End of adding button Code 
 
Z = Example()
Z.doModal()
del Z
