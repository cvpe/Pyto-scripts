'''
Objectivec allows to use gif files without passing via update Pythonista method of ui.View.
'''
import io
from PIL import Image
from rubicon.objc import *
import pyto_ui as ui

class GifImageView(ui.ImageView):
  def __init__(self, pil, *args, **kwargs):
    ui.ImageView.__init__(self, *args, **kwargs)
    self.flex='wh'
    duration = pil.n_frames * pil.info['duration'] / 1000
    frames = []
    for i in range(pil.n_frames):
      pil.seek(i)
      frames.append(self.pil2ui(pil))
    UIImageView = self.__py_view__.managed
    UIImageView.animationImages = frames
    UIImageView.animationDuration = duration
    UIImageView.animationRepeatCount = 0
    UIImageView.startAnimating()
        
  def pil2ui(self,pilimage):
    with io.BytesIO() as bIO:
      pilimage.save(bIO, 'PNG')
      uiimage = ObjCClass('UIImage').alloc().initWithData_(bIO.getvalue())
    return uiimage

if __name__ == '__main__':
    v = ui.View()
    v.title = 'GifInImageView'
    v.frame = (0,0,200,200)
    v.background_color = ui.COLOR_WHITE
    gif = 'your_own.gif'
    pil = Image.open(gif)
    w,h = pil.size
    g = GifImageView(pil)
    g.frame = (50,50,100,100*h/w)
    v.add_subview(g)
    ui.show_view(v,ui.PRESENTATION_MODE_SHEET)