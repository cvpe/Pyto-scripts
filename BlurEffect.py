from rubicon.objc import *
import pyto_ui as ui
from mainthread import mainthread
from PIL import Image
from urllib.request import urlopen

class BlurView(ui.View):
    def __init__(self, style=1, *args, **kwargs):
        ui.View.__init__(self, **kwargs)
        self.title = 'UIBlurEffect'

        #pil = Image.open('mylocal.jpg')
        pil = Image.open(urlopen('https://i.imgur.com/CqdrpEb.jpg'))
        wi,hi = pil.size
        w = 500
        h = w * hi/wi
        self.frame = (0,0,w,h)
        
        iv = ui.ImageView()
        iv.name = 'img'
        iv.image = pil
        iv.frame = self.frame
        self.add_subview(iv)
        self._style = style
        self.effect_view = None
    
    @mainthread
    def did_appear(self):
        if self.effect_view is not None:
            self.effect_view.removeFromSuperview()
        UIVisualEffectView = ObjCClass('UIVisualEffectView')
        UIBlurEffect = ObjCClass('UIBlurEffect')
        frame = CGRect(CGPoint(self.width/4,self.height/4), CGSize(self.width/2, self.height/2))
        self.effect_view = UIVisualEffectView.alloc().initWithFrame_(frame).autorelease()
        effect = UIBlurEffect.effectWithStyle_(self._style)
        self.effect_view.effect = effect
        self.effect_view.setAutoresizingMask_(18)
        self['img'].__py_view__.managed.addSubview_(self.effect_view)
    
if __name__ == '__main__':
  # different styles, see https://developer.apple.com/documentation/uikit/uiblureffect/style
  blur_view = BlurView(style=16)
  ui.show_view(blur_view,ui.PRESENTATION_MODE_SHEET)
