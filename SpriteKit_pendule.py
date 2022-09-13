from math import *
import pyto_ui as ui
from rubicon.objc import *
from Foundation import NSBundle
from mainthread import mainthread

NSBundle.bundleWithPath_('/System/Library/Frameworks/SpriteKit.framework').load()

UIApplication = ObjCClass('UIApplication')
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKLabelNode = ObjCClass('SKLabelNode')
UIColor = ObjCClass('UIColor')

def get_screen_size():				
  app = UIApplication.sharedApplication.keyWindow
  for window in UIApplication.sharedApplication.windows:
    ws = window.bounds.size.width
    hs = window.bounds.size.height
    break
  return ws,hs
    
# We subclass SKScene
class MyScene(SKScene):
    
  # Overriding update_
  @objc_method
  def update_(self, current_time):
    self.ang = self.ang + self.delta*cos(radians(2*self.ang)) +.05*self.delta
    if abs(self.ang) > self.ang_max:
      self.delta = -self.delta
    self.ang = self.ang + self.delta
    self.node.rotation = radians(self.ang)
    r = self.size.height/2
    x = self.size.width/2+r*sin(radians(-self.ang))
    y = r*cos(radians(self.ang))
    self.node.position = (x,y)

class DemoView(ui.View):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
  @mainthread
  def did_appear(self):
    # SKView can only be created on a presented view
    # Setup SKView
    screen_size = get_screen_size()
    sz = CGSize(screen_size[0], screen_size[1]-100)
    rect = CGRect(CGPoint(0, 0), sz)
    skview = SKView.alloc().initWithFrame_(rect)
    skview.preferredFramesPerSecond = 30
    self.__py_view__.managed.addSubview(skview)
    self.skview = skview
    
    scene = MyScene.sceneWithSize_(rect.size)
    scene.backgroundColor = UIColor.blackColor
    
    node = SKLabelNode.alloc().init()
    node.text = 'Pyto is good for you'
    node.fontColor = UIColor.whiteColor
    node.fontName = 'Helvetica'
    node.fontSize = 20
    node.position = CGPoint(sz.width/2, sz.height/2)
    #node.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(size)
    scene.addChild_(node)
    scene.node = node
    
    scene.ang_max = 45
    scene.ang = -scene.ang_max
    scene.delta = 1

    skview.presentScene_(scene)
    self.scene = scene

  def did_disappear(self):
    self.skview.paused = True

if __name__ == '__main__':
  view = DemoView()
  view.title = 'SpriteKit Pendule'
  ui.show_view(view,ui.PRESENTATION_MODE_FULLSCREEN)
