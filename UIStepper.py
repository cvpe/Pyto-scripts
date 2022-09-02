from rubicon.objc import *
import pyto_ui as ui

class Stepper(ui.View):
  
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    
    self._stepper = ObjCClass("UIStepper").new()
    self._stepper.minimumValue = 0
    self._stepper.maximumValue = 1
    self._stepper.stepValue = 0.1
    objcview = self.__py_view__.managed
    objcview.addSubview_(self._stepper)
    
    self.delegate = MyDelegateClass.alloc().init()
    self.delegate.view = self  # needed by delegate of stepper 
    
  def setDelegate(self):
    # addTarget does not work if called at delegate creation
        
    # 4096 (1<<12) is the value for UIControlEventValueChanged
    self._stepper.addTarget(self.delegate, action=SEL("didChange"), forControlEvents=4096)
    
# An Objective-C class for addTarget(_:action:forControlEvents:)
class MyDelegateClass(NSObject):
  @objc_method
  def didChange(self):
    self.view.slider.value = self.view._stepper.value

v = ui.View()
v.title = 'UIStepper'
v.background_color = ui.COLOR_SYSTEM_BACKGROUND
v.frame = (0,0,300,200)

sl = ui.Slider(0)
sl.frame = (100,66,100,50)
sl.user_interaction_enabled = False
v.add_subview(sl)

s = Stepper()
s.setDelegate()
s.frame = (100,134,100,50)
v.add_subview(s)
s.slider = sl # needed by delegate of stepper to set slider value

ui.show_view(v,ui.PRESENTATION_MODE_SHEET)
