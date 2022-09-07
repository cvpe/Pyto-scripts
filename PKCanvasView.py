from rubicon.objc import *
import pyto_ui as ui
from mainthread import mainthread
import photos
from __image__ import __pil_image_from_ui_image__

class MyView(ui.View):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    b_clear = ui.ButtonItem()
    b_clear.title = 'clear'
    b_clear.action = self.b_clear_action
    
    b_save = ui.ButtonItem()
    b_save.title = 'save'
    b_save.action = self.b_save_action
    self.button_items = [b_clear, b_save]
	
  def did_disappear(self):
    del self.toolPicker

  def b_clear_action(self,sender):
    self.canvasView.drawing = ObjCClass('PKDrawing').alloc().init()
      
  def b_save_action(self,nsender):
    uiimage = self.canvasView.drawing.imageFromRect_scale_(self.canvasView.frame,1.0)
    pilimage = __pil_image_from_ui_image__(uiimage)
    photos.save_image(pilimage)

  @mainthread
  def did_appear(self):
    # PKCanvasView can only be created on a presented view
    view = self.__py_view__.managed
    self.canvasView = ObjCClass('PKCanvasView').alloc().initWithFrame_(view.frame)
    view.addSubview_(self.canvasView)
    self.toolPicker = ObjCClass('PKToolPicker').alloc().init()
    self.toolPicker.setVisible_forFirstResponder_(True, self.canvasView)
    self.toolPicker.addObserver_(self.canvasView)
    self.canvasView.becomeFirstResponder()

if __name__ == '__main__':
  mv = MyView()
  mv.frame = (0,0,500,600)
  mv.title = 'PKCanvasView + PKToolPicker'
  ui.show_view(mv,ui.PRESENTATION_MODE_SHEET)
