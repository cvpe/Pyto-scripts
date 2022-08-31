from rubicon.objc import *
import pyto_ui as ui
from math import cos,sin,pi

class MyClass(ui.View):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    b = ui.Button()
    b.frame = (100,100,100,32)
    b.title = 'button'
    b.border_width = 1
    b.corner_radius = 10
    self.add_subview(b)
    o = b.__py_view__.managed
    a = -pi/4
    # no way found to create a CGAffineTransform structure in Pyto
    t = o.transform
    t.field_0 = cos(a)
    t.field_1 = -sin(a)
    t.field_2 = sin(a)
    t.field_3 = cos(a)
    t.field_4 = 0
    t.field_5 = 0
    o.transform = t

if __name__ == '__main__':
  w, h = 400,300
  f = (0, 0, w, h)
  mc = MyClass()
  mc.frame=f
  mc.background_color = ui.COLOR_WHITE
  ui.show_view(mc,ui.PRESENTATION_MODE_SHEET)