# based on
# https://github.com/tdamdouni/Pythonista/blob/master/omz/SKExample.py
# https://github.com/jbking/pythonista-misc/blob/master/spritekit/skview-demo.py
import random
import pyto_ui as ui
from rubicon.objc import *
from Foundation import NSBundle
from mainthread import mainthread

import photos
import io

def pil2ui(pilimage):
    with io.BytesIO() as bIO:
      pilimage.save(bIO, 'PNG')
      uiimage = ObjCClass('UIImage').alloc().initWithData_(bIO.getvalue())
    return uiimage

NSBundle.bundleWithPath_('/System/Library/Frameworks/SpriteKit.framework').load()

UIApplication = ObjCClass('UIApplication')
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKShapeNode = ObjCClass('SKShapeNode')
SKSpriteNode = ObjCClass('SKSpriteNode')
SKUniform = ObjCClass('SKUniform')
SKShader = ObjCClass('SKShader')
SKTexture = ObjCClass('SKTexture')
SKPhysicsBody = ObjCClass('SKPhysicsBody')
UIColor = ObjCClass('UIColor')

colors = [UIColor.redColor, UIColor.greenColor, UIColor.orangeColor, UIColor.cyanColor, UIColor.magentaColor, UIColor.purpleColor, UIColor.brownColor, UIColor.blackColor, UIColor.whiteColor]

def get_screen_size():				
  app = UIApplication.sharedApplication.keyWindow
  for window in UIApplication.sharedApplication.windows:
    ws = window.bounds.size.width
    hs = window.bounds.size.height
    break
  return ws,hs

def create_circle_shape(point):
  radius = random.randint(25, 45)
  node = SKShapeNode.shapeNodeWithCircleOfRadius_(radius)
  node.position = point
  node.physicsBody = SKPhysicsBody.bodyWithCircleOfRadius_(radius)
  return node

def create_box_shape(point):
  width = random.randint(42, 80)
  height = random.randint(42, 80)
  size = CGSize(width, height)
  node = SKShapeNode.shapeNodeWithRectOfSize_(size)
  node.position = point
  node.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(size)
  return node
  
def create_sprite(point):
  #uiimage = ui.image_with_system_name('person')
  size = uiimage.size
  tex = SKTexture.textureWithImage_(uiimage)
  node = SKSpriteNode.spriteNodeWithTexture_(tex)
  node.position = point
  node.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(size)
  #node.physicsBody = SKPhysicsBody.bodyWithTexture_size_(tex, size)
  
  spritew = SKUniform.uniformWithName_float_('spritew',size.width)
  spriteh = SKUniform.uniformWithName_float_('spriteh',size.height)
  shader_text5 = '''
    // pixelisation      
    void main() {
    float px = 20.;
    float dx = px*cos(u_time/4.)*(1./spritew);
    float dy = px*cos(u_time/4.)*(1./spriteh);
    vec2 coord = vec2(dx*floor(v_tex_coord.x/dx), dy*floor(v_tex_coord.y/dy));
    gl_FragColor = texture2D(u_texture,coord);
    }
    '''
  shader = SKShader.shaderWithSource(shader_text5)
  shader.uniforms = [spritew,spriteh]
  node.setShader_(shader)
    
  return node
    
# the boundaries to keep the shapes in
def addBorder(target_scene, x,y,w,h):
  size = CGSize(w,h)
  node = SKShapeNode.shapeNodeWithRectOfSize_(size)
  node.position = CGPoint(x,y)
  node.lineWidth = 2
  node.fillColor = UIColor.blueColor
	
  body = SKPhysicsBody.bodyWithRectangleOfSize_(size)
  body.dynamic = False
  node.physicsBody = body
  target_scene.addChild_(node)

def random_color():
  return colors[random.randint(1,len(colors))-1]

# We subclass SKScene
class MyScene(SKScene):
    
  # Overriding update_
  @objc_method
  def update_(self, current_time):
    scene = self
    for child in scene.children:
      if child.position.y < 0:
        child.removeFromParent()

  # Overriding touchesBegan_withEvent_
  @objc_method
  def touchesBegan_withEvent_(self, touches, event):
    scene = self
    #print(event)
    touch = touches.anyObject()

    point = touch.locationInNode_(scene)
    node = random.choice([
            create_circle_shape,
            create_box_shape,
            create_sprite
          ])(point)
    node.fillColor = random_color()
    scene.addChild_(node)

class DemoView(ui.View):
  debug = True

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
    # debug
    skview.showsFPS = self.debug
    skview.showsNodeCount = self.debug
    skview.showsPhysics = self.debug
    self.__py_view__.managed.addSubview(skview)
    self.skview = skview
    scene = MyScene.sceneWithSize_(rect.size)
    scene.backgroundColor = UIColor.yellowColor
        
    side_width = 10
    side_height = sz.height *0.8
    side_y = 0 + side_height/2
    side_x = 20
    addBorder(scene, side_x, side_y, side_width, side_height)
    addBorder(scene, sz.width-side_x, side_y, side_width, side_height)
    addBorder(scene, sz.width/2,side_width/2,sz.width,side_width)
        
    skview.presentScene_(scene)
    self.scene = scene

  def did_disappear(self):
    self.skview.paused = True


if __name__ == '__main__':
  pil = photos.pick_photo()
  w,h = pil.size
  pil = pil.resize((80,int(80*h/w)))
  uiimage = pil2ui(pil)
  view = DemoView()
  view.title = 'SpriteKit'
  ui.show_view(view,ui.PRESENTATION_MODE_FULLSCREEN)