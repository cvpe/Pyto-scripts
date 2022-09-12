from rubicon.objc import *
import pyto_ui as ui
from mainthread import mainthread

class MyView (ui.View):
  
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    
  @mainthread
  def did_appear(self):
    # AVRoutePickerView can only be created on a presented view
    frame = CGRect(CGPoint(10,10), CGSize(50,50))
    AVRoutePickerView = ObjCClass('AVRoutePickerView').alloc().initWithFrame_(frame)
    self_objc = self.__py_view__.managed
    self_objc.addSubview_(AVRoutePickerView)

if __name__ == '__main__':
  mv = MyView()
  mv.frame = (0,0,500,500)
  mv.background_color = ui.COLOR_WHITE
  mv.title = 'AVRoutePickerView'
  ui.show_view(mv,ui.PRESENTATION_MODE_SHEET)