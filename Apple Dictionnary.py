# even without wifi, thus local 
from UIKit import *
from rubicon.objc import *
import pyto_ui as ui
from mainthread import mainthread

UIReferenceLibraryViewController = ObjCClass('UIReferenceLibraryViewController')

class MyView(ui.View):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.background_color = ui.COLOR_LIGHT_GRAY
    self.frame = (0,0,600,700)
    self.title = 'Dictionary'
    
    tf = ui.TextField(placeholder='word to search')
    tf.frame = (10,10,self.width-20,32)
    tf.autocapitalization_type = ui.AUTO_CAPITALIZE_NONE
    tf.become_first_responder()
    tf.did_end_editing = self.did_end_editing
    self.add_subview(tf)
    
  def did_end_editing(self, sender):
    if sender.text:
      self.dict(sender.text)
    
  @mainthread	
  def dict(self, input):
    try:
      referenceViewController = UIReferenceLibraryViewController.alloc().initWithTerm_(input).autorelease()
      referenceViewController.setTitle_('Definition: {0}{1}{0}'.format('\'', input))
      referenceViewController.setPreferredContentSize_(CGSize(540, 540))
      referenceViewController.setModalPresentationStyle_(2)       
      #ui.show_view_controller(referenceViewController)
      
      # an UIViewController has to be presented in an other UIViewController
      # let us search UIViewController of the presented UiView
      # code from https://forum.omz-software.com/topic/2060/presenting-viewcontroller
      viewobj = self.__py_view__.managed
      root_view_controller=viewobj.nextResponder
      try:
        while not root_view_controller.isKindOfClass_(ObjCClass('UIViewController')):
          #print(root_view_controller)
          root_view_controller=root_view_controller.nextResponder
      except AttributeError:
        root_view_controller = None #if view is not being presented for example
        

      root_view_controller.presentViewController_animated_completion_(referenceViewController, True, None)
      
    except Exception as e:
      print(e)
        
v = MyView()
ui.show_view(v,ui.PRESENTATION_MODE_SHEET)
