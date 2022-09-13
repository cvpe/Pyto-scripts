#.... does not work
from rubicon.objc import *
import pyto_ui as ui
from mainthread import mainthread

UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIBarButtonItemGroup = ObjCClass('UIBarButtonItemGroup')

class ActionTarget(NSObject):

  @objc_method
  def btnAction(self, btn):
    global tv
    #print('btnAction')
    #print(self)
    #print(btn)
    tv.text = ''

#@mainthread
def main():
  global tv
  tv = ui.TextView()
  tv.title = 'UIBarButtonItemGroup'
  tv.frame = (0, 0, 200,200)
  tv.become_first_responder()

  target = ActionTarget.new().autorelease()
  #b1 = UIBarButtonItem.alloc().initWithTitle_style_target_action_('clear', 0, target, SEL('btnAction')).autorelease()
  uiimage = ui.image_with_system_name('clear')
  b1 = UIBarButtonItem.alloc().initWithImage_style_target_action_(uiimage, 0, target, SEL('btnAction')).autorelease()
  group = UIBarButtonItemGroup.alloc().initWithBarButtonItems_representativeItem_([b1], None).autorelease()
  tv.__py_view__.managed.inputAssistantItem.trailingBarButtonGroups = [group]
  ui.show_view(tv,ui.PRESENTATION_MODE_SHEET)
  b1.field = tv.__py_view__.managed

if __name__ == '__main__':
  main()